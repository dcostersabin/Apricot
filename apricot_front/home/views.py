from django.shortcuts import render
from django.shortcuts import redirect
import requests
from django.http.response import HttpResponse
from django.core.validators import validate_email
from django.core.validators import ValidationError
from django.contrib import messages
import pandas as pd

__SERVER_URL__ = 'http://localhost:8000/'


def home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        try:
            email = request.POST['email']
            password = request.POST['password']
            if len(password) < 5:
                messages.warning(request, 'Invalid Credentials')
                return redirect('login')
            try:
                validate_email(email)
                data = {'email': email, 'password': password}
                response = requests.post(url=__SERVER_URL__ + 'auth/token', data=data)
                if response.status_code == 200:
                    data = response.json()
                    http_response = redirect('dash')
                    http_response.set_cookie('token', data['access'])
                    http_response.set_cookie('refresh', data['refresh'])
                    return http_response
                else:
                    messages.warning(request, 'Invalid Credentials')
                    return redirect('login')

            except ValidationError:
                messages.warning(request, 'Invalid Credentials')
                return redirect('login')
        except KeyError:
            return redirect('login')


def dash(request):
    # get repos
    try:
        token = request.COOKIES['token']
    except KeyError:
        return render(request, 'home.html')

    head = {'Authorization': 'Bearer ' + token}
    # user info request
    response = requests.get(url=__SERVER_URL__ + 'user', headers=head)
    if response.status_code == 401:
        data = {'refresh': request.COOKIES['refresh']}
        refresh_response = requests.post(url=__SERVER_URL__ + 'auth/refresh', data=data)
        if refresh_response.status_code >= 400:
            return redirect('home')
        refresh = refresh_response.json()
        token = refresh['access']
    head = {'Authorization': 'Bearer ' + token}
    #     resend user info request after token refresh
    response = requests.get(url=__SERVER_URL__ + 'user', headers=head)
    user_info = response.json()
    is_superuser = user_info['is_superuser']
    if not is_superuser:
        #     resend repo request after token update
        response = requests.get(url=__SERVER_URL__ + 'repo', headers=head)
        repo = response.json()
        user_image = repo[0]['owner_avatar_login']
        # get question
        if user_info['verified']:
            response = requests.get(url=__SERVER_URL__ + 'questions', headers=head)
            question = response.json()
        else:
            question = {}

        if user_info['verified']:
            # get submission details
            response = requests.get(url=__SERVER_URL__ + 'submission', headers=head)
            submission = response.json()
        else:
            submission = {}

        response = render(request, 'dashboard.html',
                          {'repo': repo, 'question': question, 'user': user_info, 'user_image': user_image,
                           'submission': submission})
        response.set_cookie('token', token)
        return response

    if is_superuser:
        http_response = requests.get(__SERVER_URL__ + 'submission', headers=head)
        if http_response.status_code == 200:
            sub_data = http_response.json()

        response = render(request, 'dashboard.html', {'user': user_info, 'sub': sub_data})
        response.set_cookie('token', token)
        return response


def oauth(request, refresh, token):
    response = redirect('/dashboard')
    response.set_cookie('refresh', refresh)
    response.set_cookie('token', token)
    return response


def logout(request):
    try:
        token = request.COOKIES['token']
    except KeyError:
        return render(request, 'home.html')
    if token is not None:
        head = {'Authorization': 'Bearer ' + token}
        requests.post(url=__SERVER_URL__ + 'oauth/logout/', headers=head)
        response = redirect('home')
        response.delete_cookie('token')
        response.delete_cookie('refresh')
        return response


def refresh_repo(request):
    try:
        token = request.COOKIES['token']
    except KeyError:
        return render(request, 'home.html')
    head = {'Authorization': 'Bearer ' + token}
    requests.post(__SERVER_URL__ + 'repo/', headers=head)
    return redirect('dash')


def submit(request, id, username, reponame):
    url = 'https://github.com/' + username + '/' + reponame + '.git'
    try:
        token = request.COOKIES['token']
    except KeyError:
        return render(request, 'home.html')
    if token is not None:
        head = {'Authorization': 'Bearer ' + token}
        data = {'url': url}
    response = requests.put(__SERVER_URL__ + 'submission/' + id, headers=head, data=data)
    if response.status_code == 200:
        messages.success(request, 'Submission Successful')
    else:
        messages.warning(request, response.json())
    return redirect('dash')


def benchmark(request, submission_id):
    try:
        token = request.COOKIES['token']
    except KeyError:
        return render(request, 'home.html')
    if token is not None:
        head = {'Authorization': 'Bearer ' + token}

    response = requests.post(__SERVER_URL__ + 'benchmarks/' + submission_id, headers=head)
    print(response.status_code)
    return redirect('dash')


def view_score(request, submission_id):
    # get repos
    try:
        token = request.COOKIES['token']
    except KeyError:
        return render(request, 'home.html')

    head = {'Authorization': 'Bearer ' + token}
    # user info request
    response = requests.get(url=__SERVER_URL__ + 'user', headers=head)
    if response.status_code == 401:
        data = {'refresh': request.COOKIES['refresh']}
        refresh_response = requests.post(url=__SERVER_URL__ + 'auth/refresh', data=data)
        if refresh_response.status_code >= 400:
            return redirect('home')
        refresh = refresh_response.json()
        token = refresh['access']
    head = {'Authorization': 'Bearer ' + token}
    #     resend user info request after token refresh
    response = requests.get(url=__SERVER_URL__ + 'user', headers=head)
    user_info = response.json()
    is_superuser = user_info['is_superuser']
    if not is_superuser:
        return redirect('home')
    else:
        http_response = requests.get(url=__SERVER_URL__ + 'benchmarks/' + submission_id, headers=head)
        if http_response.status_code == 200:
            data = http_response.json()
            question_id = data['submission']['question_id']
            question = requests.get(url=__SERVER_URL__ + 'questions/' + str(question_id), headers=head)
            question = question.json()
            highest = requests.get(url=__SERVER_URL__ + 'benchmarks/highest/' + str(question_id), headers=head)
            highest = highest.json()

        else:
            return redirect('dash')
        response = render(request, 'score.html',
                          {'user': user_info, 'data': data, 'question': question, 'highest': highest})
        return response


def add_question(request):
    # get repos
    try:
        token = request.COOKIES['token']
    except KeyError:
        return render(request, 'home.html')

    head = {'Authorization': 'Bearer ' + token}

    response = requests.get(url=__SERVER_URL__ + 'user', headers=head)
    if response.status_code == 401:
        data = {'refresh': request.COOKIES['refresh']}
        refresh_response = requests.post(url=__SERVER_URL__ + 'auth/refresh', data=data)
        if refresh_response.status_code >= 400:
            return redirect('home')
        refresh = refresh_response.json()
        token = refresh['access']
    head = {'Authorization': 'Bearer ' + token}

    try:
        details = request.POST['details']
        inputs = request.POST['input']
        output = request.POST['output']
        if len(details) > 5 and len(inputs) > 0 and len(output) > 0:
            data = {
                'details': details,
                'inputs': inputs,
                'output': output
            }
            response = requests.post(__SERVER_URL__ + 'questions/', headers=head, data=data)
            if response.status_code == 201:
                messages.success(request, response.json())
                http_response = redirect('dash')
                http_response.set_cookie('token', token)
                return http_response
            else:
                messages.warning(request, 'Invalid Data Given')
                return redirect('dash')
        else:
            messages.warning(request, 'Invalid Data Given')
            return redirect('dash')
    except KeyError:
        messages.warning(request, 'Invalid Data Given')
        return redirect('dash')


def reset(request):
    try:
        token = request.COOKIES['token']
    except KeyError:
        return render(request, 'home.html')

    head = {'Authorization': 'Bearer ' + token}

    response = requests.get(url=__SERVER_URL__ + 'user', headers=head)
    if response.status_code == 401:
        data = {'refresh': request.COOKIES['refresh']}
        refresh_response = requests.post(url=__SERVER_URL__ + 'auth/refresh', data=data)
        if refresh_response.status_code >= 400:
            return redirect('home')
        refresh = refresh_response.json()
        token = refresh['access']
    head = {'Authorization': 'Bearer ' + token}

    reset_last = requests.post(url=__SERVER_URL__ + 'demo/reset', headers=head)
    re = reset_last.json()
    if reset_last.status_code == 200:
        messages.success(request, re)
        return redirect('dash')
    else:
        messages.warning(request, 'Something Went Wrong Try Again')
        return redirect('dash')


def assign(request):
    try:
        token = request.COOKIES['token']
    except KeyError:
        return render(request, 'home.html')

    head = {'Authorization': 'Bearer ' + token}

    response = requests.get(url=__SERVER_URL__ + 'user', headers=head)
    if response.status_code == 401:
        data = {'refresh': request.COOKIES['refresh']}
        refresh_response = requests.post(url=__SERVER_URL__ + 'auth/refresh', data=data)
        if refresh_response.status_code >= 400:
            return redirect('home')
        refresh = refresh_response.json()
        token = refresh['access']
    head = {'Authorization': 'Bearer ' + token}

    assign = requests.post(url=__SERVER_URL__ + 'demo/assign', headers=head)
    re = assign.json()
    if assign.status_code == 200:
        messages.success(request, re)
        return redirect('dash')
    else:
        messages.warning(request, 'Something Went Wrong Try Again')
        return redirect('dash')
