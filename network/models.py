from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    following = models.ManyToManyField("User", related_name="users_followed", blank = True)
    followers = models.ManyToManyField("User", related_name="users_follow", blank = True)

class Post(models.Model):
    post_creator = models.ForeignKey(User, on_delete = models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        newline = '\n'
        return f"{self.post_creator}{newline}{self.content} {newline} Posted on: {self.time_created}"