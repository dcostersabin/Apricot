from django.test import TestCase
from users.models import User
from questions.models import Question
from submission.models import Submission
from benchmark.models import Benchmark

__USERNAME__ = "test123"
__PASSWORD_1__ = "testing123"
__EMAIL__ = "test@test.com"
__DETAILS__ = "this a test details"
__INPUTS__ = "this is a test input"
__OUTPUT__ = "this is a test output"
__URL__ = "apple.com"


# Create your tests here.

class TestBenchmarkModel(TestCase):

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

    @staticmethod
    def create_submission():
        # insert user with valid data
        user = TestBenchmarkModel.create_user()
        question = TestBenchmarkModel.create_question()
        submission = Submission()
        submission.user_id = user
        submission.questions_id = question
        submission.repo_url = "apple.com"
        submission.save()
        get_last = Submission.objects.last()
        return get_last

    def test_benchmark(self):
        submission = self.create_submission()
        bench = Benchmark()
        bench.correctness = True
        bench.completeness = True
        bench.time_complexity = str(0.02)
        bench.space_complexity = str(0.01)
        bench.cprofile = "random string"
        bench.score = 1200
        bench.submission_id = submission
        bench.save()
        get_last = Benchmark.objects.last()
        self.assertEqual(get_last, bench)
        self.assertEqual(get_last.score, 1200)
        self.assertEqual(get_last.submission_id, submission)


if __name__ == "__main__":
    TestBenchmarkModel.main()
