from django.http import HttpResponse, HttpResponseRedirect
from .models import NewsArticle
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = "news/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return NewsArticle.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
