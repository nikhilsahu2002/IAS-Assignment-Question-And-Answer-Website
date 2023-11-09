from django.db import models

# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length=100)
    question = models.TextField()
    answer = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    submit_time = models.DateTimeField()
    subject = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)

    def __str__(self):
        return self.title