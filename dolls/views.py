from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from dolls.models import Question, Choice
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.urls import reverse


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    lastest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in lastest_question_list])
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': lastest_question_list,
        'self_defined': '<Question>'
    }
#     return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#         
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
    
    question = get_object_or_404(Question, pk=question_id)
#     return HttpResponse("You're looking at question %s." % question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = Question.objects.get(pk=question_id)
    return render(request, 'polls/result.html', {'question': question})
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice']) 
    
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You should select one."
            })
        
    
    selected_choice.votes += 1
    selected_choice.save()
    
    
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        
        