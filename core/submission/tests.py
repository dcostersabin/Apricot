from django.test import TestCase
from users.models import User
from questions.models import Question
from submission.models import Submission

__USERNAME__ = "test123"
__PASSWORD_1__ = "testing123"
__EMAIL__ = "test@test.com"
__DETAILS__ = "this a test details"
__INPUTS__ = "this is a test input"
__OUTPUT__ = "this is a test output"
__URL__ = "apple.com"


# Create your tests here.

class TestSubmissionModel(TestCase):

    @staticmethod
    def create_user():
        # test user with valid inputs
        new_user = User()
        new_user.email = __EMAIL__
        new_user.password = __PASSWORD_1__
        new_user.username = __USERNAME__
        new_user.save()
        get_last_user = User.objects.last()
        return get_last_user

    @staticmethod
    def create_question():
        new_question = Question()
        new_question.inputs = __INPUTS__
        new_question.output = __OUTPUT__
        new_question.details = __DETAILS__
        new_question.save()
        get_last_question = Question.objects.last()
        return get_last_question

    def test_submission_with_valid_data(self):
        # insert user with valid data
        user = self.create_user()
        question = self.create_question()
        submission = Submission()
        submission.user_id = user
        submission.questions_id = question
        submission.repo_url = "apple.com"
        submission.save()
        get_last = Submission.objects.last()
        self.assertEqual(submission, get_last)


if __name__ == "__main__":
    TestSubmissionModel.main()
