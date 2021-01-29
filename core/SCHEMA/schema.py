import graphene
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
from SCHEMA.QuestionSchemas.AddQuestionMutation import AddQuestionMutation
from SCHEMA.QuestionSchemas.RemoveQuestionMutation import RemoveQuestionMutation
from SCHEMA.QuestionSchemas.AllQuestionQuery import AllQuestion
from SCHEMA.SubmissionSchemas.UpdateSubmissionMutation import UpdateSubmissionMutation


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()


class QuestionMutation(graphene.ObjectType):
    add_question = AddQuestionMutation.Field()
    remove_question = RemoveQuestionMutation.Field()


class SubmissionMutation(graphene.ObjectType):
    update_submission = UpdateSubmissionMutation.Field()


class Query(UserQuery, AllQuestion, MeQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, QuestionMutation, SubmissionMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
