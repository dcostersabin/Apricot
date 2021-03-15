from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from submission.models import Submission
from benchmark.models import Benchmark
from questions.models import Question


@api_view(['POST'])
def reset(request):
    if request.user.is_staff or request.user.is_superuser:
        # get last submission
        last_submission = Submission.objects.latest('id')
        last_submission.checked_status = False
        last_submission.repo_url = 'None'
        last_submission.save()
        last_submission.checked_status = False
        last_submission.repo_url = 'None'
        last_submission.save()
        try:
            Benchmark.objects.latest('id').delete()
        except Benchmark.DoesNotExist:
            return Response('Success')
        return Response('Success')
    return Response("Not Allowed", status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def assign(request):
    if request.user.is_staff or request.user.is_superuser:
        # get last question
        ques = Question.objects.latest('id')
        last_submission = Submission.objects.latest('id')
        last_submission.checked_status = False
        last_submission.repo_url = 'None'
        last_submission.question_id = ques
        last_submission.save()
        return Response('Success')
    return Response("Not Allowed", status=HTTP_400_BAD_REQUEST)
