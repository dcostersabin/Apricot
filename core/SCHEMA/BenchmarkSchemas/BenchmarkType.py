from graphene_django import DjangoObjectType
from benchmark.models import Benchmark
import graphene


class BenchmarkType(DjangoObjectType):
    class Meta:
        model = Benchmark
        fields = (
            "submission_id", "correctness", "completeness", "time_complexity", "space_complexity", "cprofile", "score")

    submission_id = graphene.Int()
    correctness = graphene.Boolean()
    completeness = graphene.Boolean()
    time_complexity = graphene.String()
    space_complexity = graphene.String()
    cprofile = graphene.String()
    score = graphene.Float()
    url = graphene.String()
    email = graphene.String()
    question_detail = graphene.String()
    question_input = graphene.String()
    question_output = graphene.String()
    question_id = graphene.Int()

    def resolve_id(self, info):
        return self.id

    def resolve_submission_id(self, info):
        return self.submission_id.id

    def resolve_correctness(self, info):
        return self.correctness

    def resolve_completeness(self, info):
        return self.completeness

    def resolve_time_complexity(self, info):
        return self.time_complexity

    def resolve_space_complexity(self, info):
        return self.space_complexity

    def resolve_cprofile(self, info):
        return self.cprofile

    def resolve_score(self, info):
        return self.score

    def resolve_url(self, info):
        return self.submission_id.repo_url

    def resolve_email(self, info):
        return self.submission_id.user_id.email

    def resolve_question_detail(self, info):
        return self.submission_id.questions_id.details

    def resolve_question_input(self, info):
        return self.submission_id.questions_id.inputs

    def resolve_question_output(self, info):
        return self.submission_id.questions_id.output

    def resolve_question_id(self, info):
        return self.submission_id.questions_id.id
