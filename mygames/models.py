from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import date
import django_filters
from updown.fields import RatingField

class Game(models.Model):
    name = models.TextField()
    developer = models.TextField(blank=True, null=True)
    genre = models.TextField(blank=True, null=True)
    tag1 = models.TextField(blank=True, null=True)
    tag2 = models.TextField(blank=True, null=True)
    tag3 = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField('USD', max_digits=8, decimal_places=2, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, default=1)
    date = models.DateField(default=date.today)

    def __unicode__(self):
        return u"%s" % self.name

class Review(models.Model):
    RATING_CHOICES = ((1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five'))
    rating = models.PositiveSmallIntegerField('Rating (stars)', blank=False, default=3, choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, default=1)
    date = models.DateField(default=date.today)
    vote = RatingField(can_change_vote=True)

    class Meta:
        abstract = True
        ordering = ['-vote_likes']

class GameReview(Review):
    game = models.ForeignKey(Game)

class GameFilter(django_filters.FilterSet):
    class Meta:
        model = Game
        fields = {
            'name':['icontains'],
            'developer':['icontains'],
            'genre':['icontains'],
            'price':['lt','gt'],
            'date':['year__gt']
        }

class Bookmark(models.Model):
    user = models.ForeignKey(User, default=1)

    class Meta:
        abstract = True

class GameBookmark(Bookmark):
    game = models.ForeignKey(Game)
