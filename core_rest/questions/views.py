from rest_framework.decorators import api_view
from rest_framework.response import Response
from allauth.account.decorators import login_required
from rest_framework import status
from codeAnalyzer.AllBenchmark.Benchmark import Benchmark
from allauth.socialaccount.models import SocialToken
from repodetails.models import RepoDetail
from allauth.account.models import EmailAddress
from submission.models import Submission
from questions.models import Question
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from questions.models import QuestionSerializer


@api_view(['GET'])
@login_required
def add(request):
    if request.user.is_staff:
        user = request.user
        return Response(user.email)
    content = {'Permission Denied': 'You are not allowed to perform this'}
    return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def testing(request):
    username = request.user.username
    repo = RepoDetail.objects.get(repo_name='python-test')
    repo = repo
    repo_names = repo.repo_name
    url = repo.clone_url
    language = repo.language
    tokens = SocialToken.objects.get(account__user=request.user)
    expected_output = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,3,4,0,2,4,6,8,0,3,6,9,12,0,4,8,12,16,0,0,0,0,0,0,2,4,6,8,0,4,8,12,16,0,6,12,18,24,0,8,16,24,32,0,0,0,0,0,0,3,6,9,12,0,6,12,18,24,0,9,18,27,36,0,12,24,36,48,0,0,0,0,0,0,4,8,12,16,0,8,16,24,32,0,12,24,36,48,0,16,32,48,64"
    params = '5'
    b = Benchmark(url=url, username=username, access_token=tokens.token, repo_name=repo_names,
                  expected_output=expected_output, code_type=language, params=5)
    score = b.start(visualize=False)
    print(score)
    return Response(str(score))


@api_view(['GET', 'POST', 'DELETE'])
def question(request):
    if request.method == 'GET':
        if request.user.is_staff or request.user.is_superuser:
            # return all question
            all_question = Question.objects.all()
            serialized_question = [quest.serialize() for quest in all_question]
            return Response(serialized_question)
        else:
            verified = EmailAddress.objects.get(email=request.user.email)
            if verified.verified:
                submission = Submission.objects.get(user_id=request.user)
                assigned_question = Question.objects.get(submission=submission)
                assigned_question = assigned_question.serialize()
                question_detail = assigned_question['details']
                return Response(question_detail)
            else:
                return Response("Email Is Not Verified", status=HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        if request.user.is_staff or request.user.is_superuser:
            # insert question for admin or superuser
            serial = QuestionSerializer(data=request.POST)
            if serial.is_valid():
                serial.save()
                return Response("Question Added", status=HTTP_201_CREATED)
            else:
                return Response("Invalid Data", status=HTTP_400_BAD_REQUEST)
        else:
            return Response("Post Request Not Allowed", status=HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if request.user.is_staff or request.user.is_superuser:
            try:
                question_id = request.POST['id']

                try:
                    questions = Question.objects.get(id=question_id)
                    questions.delete()
                    return Response("Deleted Successfully", status=HTTP_200_OK)
                except Question.DoesNotExist:
                    return Response("Invalid Key Provided", status=HTTP_400_BAD_REQUEST)

            except KeyError:
                return Response("Key Not Provided", status=HTTP_400_BAD_REQUEST)
        else:
            return Response("Not Allowed", status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def question_one(request, question_id):
    if request.user.is_staff or request.user.is_superuser:
        try:
            quest = Question.objects.get(id=question_id)
            quest = quest.serialize()
            return Response(quest)
        except Question.DoesNotExist:
            return Response("Invalid Key", status=HTTP_400_BAD_REQUEST)
    else:
        return Response("Not Allowed", status=HTTP_400_BAD_REQUEST)
