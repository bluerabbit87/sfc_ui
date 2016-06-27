from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import loader


# Create your views here.
def index(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #output = ', '.join([q.question_text for q in latest_question_list])
    #template = loader.get_template('ui/index.html')
    #print template
    
    #print "index"
    #return HttpResponse("Hello World")
    return render(request, 'ui/index.html')