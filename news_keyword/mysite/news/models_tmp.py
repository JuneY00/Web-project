import datetime
from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200) # char field, max_length is mandatory 
    pub_date = models.DateTimeField("date published") # datetime field 
  
    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        now = timezone.now()
        # self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        return now - datetime.timedelta(days=1) <= self.pub_date <=now  

class Choice(models.Model):    
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)  

    def __str__(self):
        return self.choice_text


