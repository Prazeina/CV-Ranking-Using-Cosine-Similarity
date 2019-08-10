from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    skill = models.CharField(max_length=100, default=' ')
    education = models.CharField(max_length=100, default=' ')
    experience = models.CharField(max_length=100, default=' ')
    salary = models.IntegerField(default=0)
    required = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #cascade user delete vayechi post ni delete hunu parcha

    def __str__(self):
        return self.title #object oriented series, print garney tarika

    #so django knows how to find location to specific post

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk}) #REVERSE RETURNS FULL PATH AS A STRING


class CV(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='cvs/')

    def get_filename(self):
        print('get_file:', self.pdf.name)
        return self.pdf.name.split('/')[-1]

    # def delete(self, *args, **kwargs):
    #     self.pdf.delete()
    #     super().delete(*args, **kwargs)
