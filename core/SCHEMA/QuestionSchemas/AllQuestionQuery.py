import graphene
from SCHEMA.QuestionSchemas.QuestionType import QuestionType
from questions.models import Question
from graphql_jwt.decorators import superuser_required, login_required
from users.models import User
from random import randint
from submission.models import Submission
from graphql_auth.schema import MeQuery


class AllQuestion(graphene.ObjectType):
    all_questions = graphene.List(QuestionType)

    one_question = graphene.Field(QuestionType, id=graphene.ID())

    get_question = graphene.Field(QuestionType, email=graphene.String())

    get_assigned_question = graphene.Field(QuestionType, email=graphene.String())

    @superuser_required
    def resolve_all_questions(self, root, info):
        return Question.objects.all()

    @superuser_required
    def resolve_one_question(self, root, info, id):
        one_question = Question.objects.get(pk=id)
        return one_question

    @login_required
    def resolve_get_question(root, info, email):
        auth_user = MeQuery.resolve_me(root, info)
        user = User.objects.get(email=email)
        if auth_user.email == user.email:
            # check if the user exists
            user = User.objects.get(email=email)
            # check if the user has already submitted
            submission_check = Submission.objects.filter(user_id=user.id).exists()
            if not submission_check:
                # getting no of available questions
                no_question = Question.objects.all().count()
                if no_question > 0:
                    # getting all question
                    question = Question.objects.all()
                    # selecting random question from the questio array
                    random_question = randint(0, no_question - 1)
                    get_question = question[random_question]
                    # set the question to the user
                    submission = Submission(user_id=user, questions_id=get_question)
                    submission.save()
                    return get_question
                else:
                    raise ValueError("No Questions Added")
            else:
                raise ValueError("User Already Has Question Assigned")
        else:
            raise PermissionError("You Are Not Authorized")

    @login_required
    def resolve_get_assigned_question(self, info, email):
        auth_user = MeQuery.resolve_me(self, info)
        user = User.objects.get(email=email)
        if auth_user.email == user.email:
            submission = Submission.objects.get(user_id=user)
            return submission.questions_id
        raise PermissionError("You Are Not Authorized")
