"""
 followed instruction from 
 https://www.codementor.io/rogargon/simple-django-web-application-tutorial-du107rmn4
"""

from django.forms import ModelForm
from models import Game


class GameForm(ModelForm):
    class Meta:
        model = Game
        exclude = (
            'user',
            'date', )
