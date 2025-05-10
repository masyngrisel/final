from django import forms
from .models import TeamPerformance

class PredictionForm(forms.Form):
    team = forms.ModelChoiceField(queryset=TeamPerformance.objects.all(), label="Select Your Team")
    is_home = forms.ChoiceField(choices=[(True, "Home"), (False, "Away")], label="Game Location")
    opponent = forms.ModelChoiceField(queryset=TeamPerformance.objects.all(), label="Select Opponent")
    game_time = forms.ChoiceField(choices=[('day', 'Day Game'), ('night', 'Night Game')], label="Time of Game")