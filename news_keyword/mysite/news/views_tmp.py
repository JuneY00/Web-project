from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone

class DetailView(generic.DetailView):
    model = Question
    template_name="news/detail.html"
    
class ResultsView(generic.DetailView):
    model = Question
    template_name="news/results.html"

    def vote(request, question_id):        
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
        except(KeyError, Choice.DoesNotExist):
            return render(
                request,
                "news/detail.html",
                {
                    "question": question,
                    "error_message" : "You didn't select a choice.",
                },
            ) 
        else:
            selected_choice.votes = F("votes") +1 
            selected_choice.save()
            
        return HttpResponseRedirect(reverse("news:results", args=(question.id,)))


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # 변수명과 python 객체를 연결하는 dict 값 
    context = {"latest_question_list": latest_question_list}
    # return HttpResponse(template.render(context, request))
    # render(request, template name, contexxt(optional))
    return render(request, "news/index.html", context)

def detail(request, question_id):
    # get_object_or_404
    # 객체가 존재하지 않을 때 get() 사용해서 http404 exception 
    
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")

    question = get_object_or_404(Question, pk=question_id)
    return render(request, "news/detail.html", {"question":question})
    # return HttpResponse("You're looking at question %s" % question_id)

def results(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request,"news/results.html",{"question":question})

    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        return render(
            request,
            "news/detail.html",
            {
                "question": question,
                "error_message" : "You didn't select a choice.",
            },
        ) 
    else:
        selected_choice.votes = F("votes") +1 
        selected_choice.save()
        
    return HttpResponseRedirect(reverse("news:results", args=(question.id,)))
    # return HttpResponse("You're voting on question %s." % question_id)
