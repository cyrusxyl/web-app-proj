"""
 followed instruction from
 https://www.codementor.io/rogargon/simple-django-web-application-tutorial-du107rmn4
"""

from django.conf.urls import url
from django.utils import timezone
from django.views.generic import DetailView, ListView, UpdateView
from models import Game
from forms import GameForm
from views import GameCreate, GameDetail, review, game_filter
from updown.views import AddRatingFromModel

urlpatterns = [

# List latest 5 games: /mygames/
    url(r'^$',
        ListView.as_view(
        	queryset=Game.objects.filter(date__lte=timezone.now()).order_by('date')[:5],
        	context_object_name='latest_game_list',
        	template_name='mygames/game_list.html'),
        name='game_list'),

# Game details, ex.: /mygames/games/1/
    url(r'^games/(?P<pk>\d+)/$',
        GameDetail.as_view(),
        name='game_detail'),

# Create a game, /mygames/games/create/
    url(r'^games/create/$',
        GameCreate.as_view(),
        name='game_create'),

# Edit game details, ex.: /mygames/games/1/edit/
    url(r'^games/(?P<pk>\d+)/edit/$',
        UpdateView.as_view(
        	model = Game,
        	template_name = 'mygames/form.html',
        	form_class = GameForm),
        name='game_edit'),

# Create a game review, ex.: /mygames/games/1/reviews/create/
# Unlike the previous patterns, this one is implemented using a method view instead of a class view
    url(r'^games/(?P<pk>\d+)/reviews/create/$',
    	review,
    	name='review_create'),

    url(r'^reviews/(?P<object_id>\d+)/vote/(?P<score>[\d\-]+$)',
    	AddRatingFromModel(), {
            'app_label': 'mygames',
            'model': 'GameReview',
            'field_name': 'vote',
        },
    	name='review_vote'),

    url(r'^games/search$', game_filter, name='game_filter')
]
