from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.shortcuts import render, render_to_response
#from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from file_demo.models import Data
from django.forms import Form

# Create your views here.
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        print "-------------------------upload file"
        form = Form(request.POST, request.FILES)
        if form.is_valid():
            print "file valid"
            print request.FILES
            instance = Data(file=request.FILES['file'])
            instance.save()
            return HttpResponseRedirect(reverse('file_demo.views.upload_file'))
    else:
        form = Form()

    documents = Data.objects.all()

    return render_to_response(
        'file_demo/upload_file.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )

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

def register(request):
    if request.method == 'POST':
        response = HttpResponse()
        user = User.objects.create_user(request.POST['username'], request.POST['password'])
        user.save()

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

def cookie_test(request):
    if request.user.is_authenticated():
        return HttpResponse("Authenticated")
    else:
        return HttpResponse("Not Authenticated")