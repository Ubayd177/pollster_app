from django.shortcuts import render


from .models import Question, Choice
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

# questions displayed
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5] #limit to 5
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# specific questions and choices displayed
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', { 'question': question }) #pass questions as dictionary


# display poll results
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', { 'question': question })


#vote for question
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        select = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'You didnt select a choice.',
        })
    else:
        select.votes += 1
        select.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
