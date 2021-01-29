import graphene
from SCHEMA.QuestionSchemas.QuestionType import QuestionType
from questions.models import Question
from graphql_jwt.decorators import superuser_required, login_required
from users.models import User
from random import randint
from submission.models import Submission


class AllQuestion(graphene.ObjectType):
    all_questions = graphene.List(QuestionType)

    one_question = graphene.Field(QuestionType, id=graphene.ID())

    get_question = graphene.Field(QuestionType, email=graphene.String())

    @superuser_required
    def resolve_all_questions(root, info):
        return Question.objects.all()

    @superuser_required
    def resolve_one_question(root, info, id):
        one_question = Question.objects.get(pk=id)
        return one_question

    @login_required
    def resolve_get_question(root, info, email):
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
                random_question = randint(0, no_question)
                get_question = question[random_question]
                # set the question to the user
                submission = Submission(user_id=user, questions_id=get_question)
                submission.save()
                return get_question
            else:
                raise ValueError("No Questions Added")
        else:
            raise ValueError("User Already Has Question Assigned")
