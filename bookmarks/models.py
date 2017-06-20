from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Bookmark(models.Model):
    title = models.CharField(max_length = 20)
    link = models.URLField(max_length=200)
    tag = models.ManyToManyField(Tag, related_name='tag')
    user = models.ForeignKey(User, related_name = 'user')
    sharebookmark = models.BooleanField(default = False)

    def __str__(self):
        return ('{} - {}'.format(self.title, self.link))

class voting(models.Model):
    bookmark = models.ForeignKey(Bookmark, related_name= 'bookmark')
    votes = models.IntegerField(default = 1)
    users_voted = models.ManyToManyField(User)

    def __str__(self):
        return ('{} - {}'.format(self.bookmark, self.votes))

class friendship(models.Model):
    from_friend = models.ForeignKey(User, related_name= 'from_friend')
    to_friend = models.ForeignKey(User, related_name='to_friend')

    def __str__(self):
        return ('{} - {}'.format(self.from_friend, self.to_friend))

    class Meta:
        unique_together = (("from_friend","to_friend"),)
