from graphene_django import DjangoObjectType
from submission.models import Submission
import graphene


class SubmissionType(DjangoObjectType):
    class Meta:
        model = Submission
        fields = ("id","user_id", "question_id", "repo_url", "checked_status", "language_type")

    id = graphene.ID()
    user_id = graphene.Int()
    question_id = graphene.Int()
    repo_url = graphene.String()
    checked_status = graphene.Boolean()
    language_type = graphene.Int()

    def resolve_id(self, info):
        return self.id

    def resolve_user_id(self, info):
        return self.user_id.id

    def resolve_question_id(self, info):
        return self.question_id.id

    def resolve_repo_url(self, info):
        return self.repo_url

    def resolve_checked_status(self, info):
        return self.checked_status

    def resolve_language_type(self, info):
        return self.language_type
