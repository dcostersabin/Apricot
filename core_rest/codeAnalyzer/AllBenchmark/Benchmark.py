from codeAnalyzer.Python.PythonBenchmark import PythonBenchmark
from codeAnalyzer.Ruby.RubyBenchmark import RubyBenchmark


class Benchmark:
    """
    Combines both python code analysis and Ruby code analysis
    """

    def __init__(self, url, username, access_token, repo_name, expected_output, params, code_type='Python'):
        self.url = url
        self.expected_output = expected_output
        self.params = params
        self.code_type = code_type
        self.username = username
        self.access_token = access_token
        self.repo_name = repo_name
        self.benched_object = None

    def start(self, visualize=True, params='all', save=False):
        """
        High level interface for both python and ruby code analyzer
        :param visualize: if set to True it provides a pyplot of the analyzed data
        :param params: parameters for visualizing the data i.e all , time , cprofile
        :param save: if true it saves the result into png
        :return: Score metric of the analyzed function
        """
        if self.code_type == 'Python':
            self.benched_object = PythonBenchmark(url=self.url, expected_output=self.expected_output,
                                                  params=self.params, username=self.username,
                                                  access_token=self.access_token, repo_name=self.repo_name)

        elif self.code_type == 'Ruby':
            self.benched_object = RubyBenchmark(url=self.url, expected_output=self.expected_output,
                                                params=self.params, username=self.username,
                                                access_token=self.access_token, repo_name=self.repo_name)

        score = self.benched_object.start()
        if visualize:
            self.benched_object.visualize(params=params, save=save)
        return score
