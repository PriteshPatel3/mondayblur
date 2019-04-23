from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User #To use django authentication system
from django.urls import reverse #to get reverse
#from PIL import Image #easy saving and manipulating of image 

class category (models.Model):
    category = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True)

    def __str__(self):
        return self.category


class question (models.Model):
    title = models.CharField(max_length=100) #use charfield to limit user input
    slug = models.SlugField(max_length=100)
    content = models.TextField() #use TextField if there is no limit for the content
    date_published = models.DateTimeField(default=timezone.now) #auto-select the current time
    category = models.ForeignKey(category,on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #if the user is deleted the question will be deleted
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question-detail', args=[question.slug])

class comment(models.Model):
    post = models.ForeignKey(question,on_delete=models.CASCADE,related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_published = models.DateTimeField(default=timezone.now)
    comment = models.TextField()
    approved = models.BooleanField(default=False)

    def approved(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.comment
    
    def get_absolute_url(self):
        return reverse('question-detail', args=[question.slug])



    