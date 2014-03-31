from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.shortcuts import render, render_to_response
#from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from file_demo.models import UserFiles
from django.forms import Form

# Handles the file upload,
# TODO: Force the post request to send a directory structure of the file
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        print "-------------------------upload file"
        form = Form(request.POST, request.FILES)
        if form.is_valid():
            print "file valid"
            print request.FILES
            instance = UserFiles(user=request.user,file=request.FILES['file'])
            instance.save()
            return HttpResponseRedirect(reverse('file_demo.views.upload_file'))
    else:
        form = Form()

    documents = UserFiles.objects.all()

    return render_to_response(
        'file_demo/upload_file.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )

#Expects a username through POST data
# checks to ensure username is not already taken
# returns a 498 status code if taken or a 200 if it is unique
@csrf_exempt
def check_username(request):
    if request.method == 'POST':
        response = HttpResponse()
        if User.objects.filter(username=request.POST['username']).count():
            response.content = "Username is already taken"
            response.reason_phrase = "Username must not already be taken"
            response.status_code = 498
            #return username is not unique
        else:
            response.content = "Username is acceptable"
            response.status_code = 200
            #return username is unique
        return response

# Registers user, expects a username and password
# NOTE: username and password should already be validated and appropriate
@ensure_csrf_cookie
def register(request):
    if request.method == 'POST':
        response = HttpResponse()
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username, '',password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                response.set_cookie('mfusername', username)
        response.content = "Registered User"
        response.status_code = 200
        return response
    else:
        return HttpResponse()

# Expects post data with a header with a csrf token and POST data with a username and password
# checks if username and password is valid and then logs in the user
# returns a cookie with user's session if successful and a status code of 200
# returns a status code of 499 if unsuccessful
@ensure_csrf_cookie
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        response = HttpResponse()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                response.content = "logged in"
                response.status_code = 200
                login(request, user)
                response.set_cookie('mfusername', username)
            else:
                response.content = "not logged in"
                response.status_code = 499
        else:
            response.content = "not logged in"
            response.status_code = 499

        return response
    else:
        return HttpResponse()

# Test if a user login was succesful
# A cookie with the appropriate session id is expected in the request
def cookie_test(request):
    if request.user.is_authenticated():
        return HttpResponse("Authenticated")
    else:
        return HttpResponse("Not Authenticated")