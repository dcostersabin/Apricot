import graphene
from SCHEMA.BenchmarkSchemas.BenchmarkType import BenchmarkType
from graphql_jwt.decorators import superuser_required
from submission.models import Submission
from users.models import User
from benchmark.models import Benchmark


class AllBenchmark(graphene.ObjectType):
    all_benchmark = graphene.List(BenchmarkType)
    user_benchmark = graphene.Field(BenchmarkType, email=graphene.String())

    @superuser_required
    def resolve_all_benchmark(root, info):
        return Benchmark.objects.all()

    @superuser_required
    def resolve_user_benchmark(root, info, email):
        user = User.objects.get(email=email)
        prev_submission = Submission.objects.get(user_id=user)
        prev_bench = Benchmark.objects.get(submission_id=prev_submission)
        return prev_bench
