from questions.models import Question
import graphene
from graphql_jwt.decorators import superuser_required
from SCHEMA.QuestionSchemas.QuestionType import QuestionType


class AddQuestionMutation(graphene.Mutation):
    class Arguments:
        details = graphene.String(required=True)
        inputs = graphene.String(required=True)
        output = graphene.String(required=True)

    question = graphene.Field(QuestionType)

    @classmethod
    @superuser_required
    def mutate(cls, root, info, details, inputs, output):
        question = Question(details=details, inputs=inputs, output=output)
        question.save()
        return AddQuestionMutation(question=question)
