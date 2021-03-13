from codeAnalyzer.Ruby.RubyChecker import RubyChecker
import os
import shutil
from os import path
import subprocess
import tracemalloc
import timeit
from codeAnalyzer.Ruby.TimeitExecuter import Testing
import pandas as pd
import io
import matplotlib.pyplot as plt

__REPEAT__ = 5
__NUMBER__ = 1
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
__SAVE_PATH__ = BASE_DIR


class RubyBenchmark:

    def __init__(self, url, username, access_token, repo_name, expected_output, params):
        """
        :param url: Url to be cloned or github repository HTTPS link SSH is not supported
        :param expected_output: actual output generated by the algorithm
        :param params: parameters for function testing
        """
        self.url = url
        self.target_output = str(expected_output)
        self.params = params
        self.repo_validity = RubyChecker(url=self.url, username=username, access_token=access_token,
                                         repo_name=repo_name).clone_check()
        self.benchmark_score = {"complete": False, "correctness": False, "time": None, "memory": None,
                                "detailed_profiling": None}
        self.calculated_output = None

    def start(self):
        """
        Function to start the evaluation of Ruby code
        :return: Benchmark score of the code if no error occurs otherwise false
        """
        if self.repo_validity:
            self.__completeness__()
            self.remove_temp()
            return self.benchmark_score
        else:
            self.remove_temp()
            return False

    def __completeness__(self):
        """
        Checks if the given module provide any output or not
        :return: None
        """
        try:

            var = subprocess.run(["ruby", BASE_DIR + "/Ruby/RubyOutputGenerator.rb", str(self.params)],
                                 check=True,
                                 stdout=subprocess.PIPE,
                                 text=True).stdout
            if var == '':
                return self.benchmark_score
            else:
                self.benchmark_score['complete'] = True
                try:
                    assert str(var) == str(self.target_output)
                    print("correct start")
                    self.benchmark_score["correctness"] = True
                    print("space")
                    self.__space_complexity__()
                    print("time")
                    self.__time_complexity__()
                    print("detailed")
                    self.__detailed_profiling__()
                    print("end")
                except (AssertionError, Exception) as e:
                    print(e)
                    self.benchmark_score["correctness"] = False
        except subprocess.CalledProcessError:
            pass

    def __space_complexity__(self):
        """
        Measures the peak memory used by the defined module
        :return: None
        """
        tracemalloc.start()
        var = subprocess.run(["ruby", BASE_DIR + '/Ruby/RubyOutputGenerator.rb', str(self.params)], check=True,
                             stdout=subprocess.PIPE,
                             text=True).stdout
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.benchmark_score['memory'] = peak / 10 ** 6

    def __time_complexity__(self):
        """
        Measures the time taken by the code to execute for __REPEAT__ times
        :return:
        """
        setup_code = 'from codeAnalyzer.Ruby.TimeitExecuter import Testing'
        stmt_code = "Testing.setup(" + "'" + str(self.params) + "'" + ")"
        time = timeit.repeat(stmt=stmt_code, setup=setup_code, repeat=__REPEAT__, number=__NUMBER__)
        self.benchmark_score['time'] = time

    def __detailed_profiling__(self):
        """
        Using cProfile to aggregate the resources used by the module
        :return:
        """
        import cProfile, pstats
        profiler = cProfile.Profile()
        profiler.enable()
        Testing.setup(self.params)
        profiler.disable()
        stream = io.StringIO()
        pstats.Stats(profiler, stream=stream).sort_stats('ncalls').strip_dirs().print_stats()
        stream = stream.getvalue()
        self.__convert_to_csv__(stream)
        self.benchmark_score['detailed_profiling'] = pd.read_csv(BASE_DIR + '/temp/stat.csv')

    @staticmethod
    def __convert_to_csv__(stream):
        """
        Converting crpofile output to csv
        :param stream: IOStram for the cprofile output
        :return: None
        """
        result = 'ncalls' + stream.split('ncalls')[-1]
        result = '\n'.join([','.join(line.rstrip().split(None, 5)) for line in result.split('\n')])
        f = open(BASE_DIR + '/temp/stat'.rsplit('.')[0] + '.csv', 'w')
        f.write(result)
        f.close()

    def remove_temp(self):
        """
        Removes the temporary files after results are calculated
        :return: None
        """
        if path.exists(BASE_DIR + '/temp/'):
            shutil.rmtree(BASE_DIR + '/temp/')

    def visualize(self, params='time', save=False):
        """
        Visualize the analyzed data
        :param params: the item needed to be visualized
        :param save: save the image as png if True
        :return:  None
        """
        if self.benchmark_score['complete'] is True:
            if params == 'time':
                self.__visualize_time__(save)
            elif params == 'cprofile':
                self.__visualize_cprofile__()
            elif params == 'all':
                self.__visualize_time__(save)
                self.__visualize_cprofile__(save)

    def __visualize_time__(self, save=False):
        """
        Visualize the time complexity
        :param save: saves png if True
        :return: None
        """
        plt.bar(range(1, 6), self.benchmark_score['time'])
        plt.title('Time Complexity for 5 Iterations')
        plt.ylabel('Time In Seconds')
        plt.xlabel('No Of Iterations')
        if save:
            plt.savefig(__SAVE_PATH__ + '/time.png')
        plt.show()

    def __visualize_cprofile__(self, save=False):
        """
        cProfile analysis of the algorithm
        :param save: saves png if True
        :return: None
        """
        score = pd.DataFrame(self.benchmark_score['detailed_profiling'])
        ncalls = score.iloc[:, 0]
        functions = score.iloc[:, -1]
        plt.bar(functions, ncalls)
        plt.title('No Of Functions Calls')
        plt.xticks(rotation=45, ha="right")
        for index, data in enumerate(ncalls):
            plt.text(x=index, y=data + 1, s=f"{data}", fontdict=dict(fontsize=8))
        plt.tight_layout()
        if save:
            plt.savefig(__SAVE_PATH__ + '/function_calls.png')
        plt.show()
