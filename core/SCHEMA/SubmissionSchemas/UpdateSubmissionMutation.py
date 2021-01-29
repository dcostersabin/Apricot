from submission.models import Submission
import graphene
from graphql_jwt.decorators import login_required
from SCHEMA.SubmissionSchemas.SubmissionType import SubmissionType
from users.models import User


class UpdateSubmissionMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        language_type = graphene.Int(required=True)
        repo_url = graphene.String(required=True)

    prev_submission = graphene.Field(SubmissionType)

    @classmethod
    @login_required
    def mutate(cls, root, info, language_type, repo_url, email):
        if language_type == 1 or language_type == 2:
            user = User.objects.get(email=email)
            prev_submission = Submission.objects.get(user_id=user)
            prev_submission.language_type = language_type
            prev_submission.repo_url = repo_url
            prev_submission.save()
            return UpdateSubmissionMutation(prev_submission=prev_submission)
        else:
            raise ValueError("Invalid Language Selected")
