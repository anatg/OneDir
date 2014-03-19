from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response
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