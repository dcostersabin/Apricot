from submission.models import Submission
import graphene
from benchmark.models import Benchmark as BenchmarkModel
from questions.models import Question
from graphql_jwt.decorators import superuser_required
from SCHEMA.BenchmarkSchemas.BenchmarkType import BenchmarkType
from users.models import User
from codeAnalyzer.AllBenchmark.Benchmark import Benchmark
import math
import pandas as pd


class AddBenchmarMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)

    benchmark = graphene.Field(BenchmarkType)

    @classmethod
    @superuser_required
    def mutate(cls, root, info, email):
        user = User.objects.get(email=email)
        prev_submission = Submission.objects.get(user_id=user)
        prev_bench = BenchmarkModel.objects.filter(submission_id=prev_submission).exists()
        if not prev_bench:
            question = Question.objects.get(pk=prev_submission.questions_id_id)
            code_type = 'python'
            if prev_submission.language_type == 2:
                code_type = 'ruby'
            # starting the benchmarking process
            benchmark_model = BenchmarkModel()
            bench = Benchmark(url=prev_submission.repo_url, expected_output=question.output,
                              params=question.inputs, code_type=code_type)
            score = bench.start(visualize=False)
            if not score:
                benchmark_model.submission_id = prev_submission
                prev_submission.checked_status = True
                prev_submission.save()
                benchmark_model.save()
                raise ValueError("System Failed To Validate")
            total_score = 0
            uniformity_breaker = 0.001
            benchmark_model.completeness = score["complete"]
            if score["complete"]:
                total_score += 10
            benchmark_model.correctness = score["correctness"]
            if score["correctness"]:
                total_score += 10
                average_time = sum(score["time"]) / 5
                total_score += (10 / (1 / (1 + math.exp(-average_time))))
                benchmark_model.time_complexity = average_time
                benchmark_model.space_complexity = score["memory"]
                total_score += (10 / score["memory"])
                benchmark_model.cprofile = score["detailed_profiling"].to_dict()
                detailed_profiling = score["detailed_profiling"].iloc[:, 0]
                # adding small number with respect to function call to break uniformity
                uniformity_breaker += (sum(detailed_profiling) * uniformity_breaker)

            total_score = round(total_score, -2)
            total_score = total_score + uniformity_breaker
            benchmark_model.score = total_score
            benchmark_model.submission_id = prev_submission
            prev_submission.checked_status = True
            prev_submission.save()
            benchmark_model.save()
            return AddBenchmarMutation(benchmark_model)
        raise ValueError("The User's Code Has Already Been Benchmarked")
