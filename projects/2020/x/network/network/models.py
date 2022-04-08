from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    #https://stackoverflow.com/questions/15384665/django-manytomanyfield-add-user
    followers = models.ManyToManyField('self', related_name='following_user', symmetrical=False, blank=True, null=True)
    
    def serialize(self):
        return{
            "user_id": self.id,
            "username": self.username,
            "followers": [user.username for user in self.followers.all()],
            # "following": self in user.followingUser.all()
        }

# You will also need to add additional models to this file to represent details about posts,
# likes, and followers.
class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    poster = models.ForeignKey("User", on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    
    def serialize(self):
        return {
            "id": self.id,
            "user":self.user.id,
            "poster": self.poster.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }