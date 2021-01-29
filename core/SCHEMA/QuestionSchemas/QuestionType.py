from graphene_django import DjangoObjectType
from questions.models import Question
import graphene


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("id", "details", "inputs", "output")

    id = graphene.ID()
    details = graphene.String()
    inputs = graphene.String()
    output = graphene.String()

    def resolve_id(self, info):
        return self.id

    def resolve_details(self, info):
        return self.details

    def resolve_inputs(self, info):
        return self.inputs

    def resolve_output(self, info):
        return self.output
