from rest_framework.decorators import api_view
from rest_framework.response import Response
from submission.models import Submission
from rest_framework.status import HTTP_400_BAD_REQUEST
from repodetails.models import RepoDetail


@api_view(['GET'])
def submission(request):
    if request.method == 'GET':
        if request.user.is_staff or request.user.is_superuser:
            all_submission = Submission.objects.all()
            serialized = [data.serialized() for data in all_submission]
            return Response(serialized)
        else:
            # get user submission
            submission_details = Submission.objects.get(user_id=request.user)
            return Response(submission_details.serialized())


@api_view(['GET', 'PUT'])
def submission_one(request, submission_id):
    if request.method == 'GET':
        if request.user.is_staff or request.user.is_superuser:
            try:
                sub = Submission.objects.get(id=submission_id)
                sub = sub.serialized()
                return Response(sub)
            except Submission.DoesNotExist:
                return Response("Invalid Key", status=HTTP_400_BAD_REQUEST)
        else:
            return Response("Not Allowed", status=HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        try:
            sub = Submission.objects.get(id=submission_id)
            # user can only submit once
            if sub.repo_url != "None":
                return Response("Already Submitted", status=HTTP_400_BAD_REQUEST)
            if request.user.id == sub.user_id.id:
                try:
                    if request.POST['url'] is not None:
                        # Check if the url is within our database
                        # if not provided url is from third party
                        try:
                            repo_details = RepoDetail.objects.get(clone_url=request.POST['url'], user_id=request.user)
                            sub.repo_url = repo_details.clone_url
                            sub.save()
                            return Response("Submitted Successfully")
                        except RepoDetail.DoesNotExist:
                            return Response("URL Does Not Match", status=HTTP_400_BAD_REQUEST)
                    else:
                        return Response("Invalid URL Or User Has Already Submitted", status=HTTP_400_BAD_REQUEST)
                except KeyError:
                    return Response("URL Not Provided", status=HTTP_400_BAD_REQUEST)
            else:
                return Response("Not Allowed", status=HTTP_400_BAD_REQUEST)
        except Submission.DoesNotExist:
            return Response("Invalid Key", status=HTTP_400_BAD_REQUEST)
