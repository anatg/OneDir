from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from file_demo.models import UserFiles
from django.forms import Form
from django.conf import settings
import json_helper, json

# Handles the file upload,
#TODO: Test updated version
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            print "-------------------------upload file"
            form = Form(request.POST, request.FILES)
            if form.is_valid():
                print "file valid"
                print request.FILES
                instance = UserFiles(user=request.user,directory=request.POST['directory'], file=request.FILES['file'])
                instance.save()
                json_helper.update_file(settings.MEDIA_ROOT+str(request.user.username)+'/',
                                        '/'+request.POST['directory']+'/'+request.POST['file'])
                return HttpResponseRedirect(reverse('file_demo.views.upload_file'))
        else:
            response = HttpResponse()
            response.content = "User not authenticated"
            response.status_code = 497
            return response
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
#TODO: Test updated version
@ensure_csrf_cookie
def register(request):
    if request.method == 'POST':
        response = HttpResponse()
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username, '',password)
        user.save()
        user = authenticate(username=username, password=password)
        json_helper.create_json(settings.MEDIA_ROOT+str(request.user.username)+'/')
        if user is not None:
            if user.is_active:
                login(request, user)
                response.set_cookie('mfusername', username)
        response.content = json.dumps(json_helper.read_json(settings.MEDIA_ROOT+str(user.username)+'/'))
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

#Change user's password
#Expects a user cookie and password through POST
#returns a 200 code for success and a 497 for failure
@ensure_csrf_cookie
def change_password(request):
    if request.method == 'POST':
        response = HttpResponse()
        if request.user.is_authenticated():
            password = request.POST['password']
            request.user.set_password(password)
            request.user.save()
            response.content = "User password change successful"
            response.status_code = 200
        else:
            response.content = "User not authenticated"
            response.status_code = 497
        return response
    else:
        return HttpResponse()

#Returns a user's json file list as a json
# user must be authenticated
#If successful returns user json and status code 200
#If fails returns status code 497
#TODO: Test updated version
def json_request(request):
    response = HttpResponse()
    if request.user.is_authenticated():
        response.content = json.dumps(json_helper.read_json(settings.MEDIA_ROOT+str(request.user.username)+'/'))
        response['Content-Type'] = 'application/json'
        response.status_code = 200
    else:
        response.content = "Failed to authenticate user"
        response.status_code = 497
    return response

# Deletes user's file
# Expects user to be authenticated, a file directory, and a file name
# Returns updated json file
#TODO: Test updated version
@csrf_exempt
def delete_file(request):
    if request.method == 'POST':
        response = HttpResponse()
        if request.user.is_authenticated():
            filename = request.POST['directory'] + '/' + request.POST['file']
            file = UserFiles.objects.filter(user__username=request.user.username).get(file=filename)
            file.delete()
            json_helper.delete_file(settings.MEDIA_ROOT+str(request.user.username)+'/', filename)
            response.content = json.dumps(json_helper.read_json(settings.MEDIA_ROOT+str(request.user.username)+'/'))
            response['Content-Type'] = 'application/json'
            response.status_code = 200
        else:
            response.content = "Failed to authenticate user"
            response.status_code = 497
        return response
    else :
        return HttpResponse()


#NOTE: ONLY FOR TESTING
# Test if a user login was succesful
# A cookie with the appropriate session id is expected in the request
def cookie_test(request):
    if request.user.is_authenticated():
        return HttpResponse("Authenticated")
    else:
        return HttpResponse("Not Authenticated")