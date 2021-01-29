from questions.models import Question
import graphene
from graphql_jwt.decorators import superuser_required
from SCHEMA.QuestionSchemas.QuestionType import QuestionType


class RemoveQuestionMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    question = graphene.Field(QuestionType)

    @classmethod
    @superuser_required
    def mutate(cls, root, info, id):
        question = Question.objects.get(pk=id)
        question.delete()
        return
