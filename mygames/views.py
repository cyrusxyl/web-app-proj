"""
 followed instruction from
 https://www.codementor.io/rogargon/simple-django-web-application-tutorial-du107rmn4
"""

from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.shortcuts import render
from models import GameReview, Game, GameFilter
from forms import GameForm

class GameDetail(DetailView):
  model = Game
  template_name = 'mygames/game_detail.html'

  def get_context_data(self, **kwargs):
    context = super(GameDetail, self).get_context_data(**kwargs)
    context['RATING_CHOICES'] = GameReview.RATING_CHOICES
    return context

class GameCreate(CreateView):
  model = Game
  template_name = 'mygames/form.html'
  form_class = GameForm

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(GameCreate, self).form_valid(form)

def review(request, pk):
  game = get_object_or_404(Game, pk=pk)
  review = GameReview(
      rating=request.POST['rating'],
      comment=request.POST['comment'],
      user=request.user,
      game=game)
  review.save()
  return HttpResponseRedirect(reverse('mygames:game_detail', args=(game.id,)))

def game_filter(request):
    filter = GameFilter(request.GET, queryset=Game.objects.all())
    return render(request, 'mygames/game_filter.html', {'filter': filter})

import json

from django.contrib import auth
from django.http import HttpResponse
from django.views import View


class BookmarkView(View):
    # This variable will set the bookmark model to be processed
    model = None

    def post(self, request, pk):
        # We need a user
        user = auth.get_user(request)
        # Trying to get a bookmark from the table, or create a new one
        bookmark, created = self.model.objects.get_or_create(user=user, obj_id=pk)
        # If no new bookmark has been created,
        # Then we believe that the request was to delete the bookmark
        if not created:
            bookmark.delete()

        return HttpResponse(
            json.dumps({
                "result": created,
                "count": self.model.objects.filter(obj_id=pk).count()
            }),
            content_type="application/json"
        )
