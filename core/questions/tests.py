from django.test import TestCase
from questions.models import Question

# Create your tests here.
__DETAILS__ = "this a test details"
__INPUTS__ = "this is a test input"
__OUTPUT__ = "this is a test output"


class TestQuestions(TestCase):

    def test_insert_valid_question(self):
        # insert question with valid parameters
        new_question = Question()
        new_question.inputs = __INPUTS__
        new_question.output = __OUTPUT__
        new_question.details = __DETAILS__
        new_question.save()
        get_last = Question.objects.last()
        self.assertEqual(new_question, get_last)

    def test_insert_question_without_input(self):
        # insert question without input
        new_question = Question()
        new_question.output = __OUTPUT__
        new_question.details = __DETAILS__
        new_question.save()
        count = Question.objects.count()
        self.assertEqual(count, 1)

    def test_delete_all_questions(self):
        Question.objects.all().delete()
        count = Question.objects.count()
        self.assertEqual(count, 0)

    def test_insert_question_without_parameters(self):
        # insert question without parameters
        new_question = Question()
        new_question.save()
        last = Question.objects.last()
        self.assertEqual(last.inputs, "")


if __name__ == "__main__":
    TestQuestions.main()
