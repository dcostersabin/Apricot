from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from benchmark.models import Benchmark
from submission.models import Submission
from allauth.socialaccount.models import SocialToken
from repodetails.models import RepoDetail
from codeAnalyzer.AllBenchmark.Benchmark import Benchmark as CodeAnalyzer
import math
from questions.models import Question


# Create your views here.

@api_view(['GET'])
def benchmark(request):
    if request.user.is_staff or request.user.is_superuser:
        # get all benchmarks
        bench = Benchmark.objects.all()
        serialized_data = [data.serialized() for data in bench]
        return Response(serialized_data)
    else:
        return Response("Not Allowed", status=HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def benchmark_submission(request, submission_id):

    if request.method == 'POST':
        if request.user.is_staff or request.user.is_superuser:
            try:
                sub = Submission.objects.get(pk=submission_id)
                benchmark_check = Benchmark.objects.filter(submission_id=sub).exists()
                if benchmark_check:
                    return Response("Benchmark Already Exists", status=HTTP_400_BAD_REQUEST)
                else:
                    submission_user_id = sub.user_id
                    # token details
                    submission_user_token = SocialToken.objects.get(account__user=submission_user_id)
                    access_token = submission_user_token.token
                    username = sub.user_id.username
                    # repo details
                    repo_details = RepoDetail.objects.get(clone_url=sub.repo_url)
                    repo_name = repo_details.repo_name
                    clone_url = repo_details.clone_url
                    language = repo_details.language
                    # question details
                    inputs = sub.question_id.inputs
                    outputs = sub.question_id.output
                    # benchmark
                    bench = Benchmark()
                    bench_details = CodeAnalyzer(url=clone_url, username=username, access_token=access_token,
                                                 repo_name=repo_name, expected_output=outputs, code_type=language,
                                                 params=inputs)
                    benchmark_score = bench_details.start(visualize=False)
                    if not benchmark_score:
                        bench.submission_id = sub
                        sub.checked_status = True
                        sub.save()
                        bench.save()
                        return Response("Submission Failed To Meet The Guidelines")
                    total_score = 0
                    uniformity_breaker = 0.001
                    bench.completeness = benchmark_score['complete']
                    if benchmark_score["complete"]:
                        total_score += 10

                    bench.correctness = benchmark_score['correctness']
                    if benchmark_score['correctness']:
                        total_score += 10
                        average_time = sum(benchmark_score["time"]) / 5
                        total_score += (10 / (1 / (1 + math.exp(-average_time))))
                        bench.time_complexity = average_time
                        bench.space_complexity = benchmark_score['memory']
                        total_score += (10 / benchmark_score['memory'])
                        bench.cprofile = benchmark_score['detailed_profiling'].to_dict()
                        detailed_profiling = benchmark_score["detailed_profiling"].iloc[:, 0]
                        detailed_profiling = [int(str(i).split("/")[0]) for i in detailed_profiling]
                        # adding small number with respect to function call to break uniformity
                        uniformity_breaker += (sum(detailed_profiling) * uniformity_breaker)
                        print(total_score)
                    if total_score > 1000:
                        total_score = round(total_score, -2)
                    else:
                        total_score = round(total_score, -1)
                    total_score = total_score + uniformity_breaker
                    bench.score = total_score
                    bench.submission_id = sub
                    sub.checked_status = True
                    sub.save()
                    bench.save()
                    return Response("Code Benchmarked Successfully")

            except Submission.DoesNotExist:
                return Response("Invalid Submission Id", status=HTTP_400_BAD_REQUEST)
        else:
            return Response("Not Allowed", status=HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        if request.user.is_staff or request.user.is_superuser:
            try:
                bench = Benchmark.objects.get(submission_id_id=submission_id)
                return Response(bench.serialized())
            except Benchmark.DoesNotExist:
                return Response("Invalid Key", status=HTTP_400_BAD_REQUEST)
        else:
            return Response("Not Allowed", status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def highest(request, question_id):
    if request.user.is_staff or request.user.is_superuser:
        try:
            question_check = Question.objects.get(pk=question_id)
            bench = Benchmark.objects.filter(submission_id__question_id_id=question_id).order_by('score')
            bench = bench.last()
            data = {'highest': bench.score}
            return Response(data)
        except Question.DoesNotExist:
            return Response("Invalid Key", status=HTTP_400_BAD_REQUEST)
    else:
        return Response("Not Allowed", status=HTTP_400_BAD_REQUEST)
