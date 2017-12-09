"""
 followed instruction from
 https://www.codementor.io/rogargon/simple-django-web-application-tutorial-du107rmn4
"""

from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from django.shortcuts import render
from models import GameReview, Game, GameFilter, GameBookmark
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

class BookmarkList(ListView):
  # model = Game
  # context_object_name='latest_game_list',
  template_name='mygames/game_list.html'

  def get_queryset(self):
      bookmarks = GameBookmark.objects.filter(user=self.request.user)
      queryset = []
      for bm in bookmarks:
          queryset += Game.objects.filter(id=bm.game.id)
      return queryset


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

def bookmark(request, pk):
  game = get_object_or_404(Game, pk=pk)
  bookmark, created = GameBookmark.objects.get_or_create(user=request.user, game=game)
  if not created:
            bookmark.delete()
  return HttpResponseRedirect(reverse('mygames:game_detail', args=(game.id,)))
