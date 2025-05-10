from django.shortcuts import render
from .forms import PredictionForm
from .models import TeamPerformance, GameTime, Ballpark, PitcherStats, RecentTeamPerformance
from .services import calculate_team_performance_score

def prediction_view(request):
    prediction_score = None
    team_score = None
    recent_performance_score = None
    ballpark_score = None
    pitcher_score = None
    game_time_score = None

    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            team = form.cleaned_data['team']
            is_home = form.cleaned_data['is_home'] == 'True'
            opponent = form.cleaned_data['opponent']
            game_time_type = form.cleaned_data['game_time']  # 'day or night'

            # Get the GameTime record for the selected team
            game_time = GameTime.objects.get(team=team)

            # Calculate the game time score based on the selected game time type
            if game_time_type == 'day':
                game_time_score = game_time.get_day_game_score()
            else:
                game_time_score = game_time.get_night_game_score()

            # 1. Team Performance Score (from TeamPerformance model)
            team_score = team.win_percentage()

            # 2. Recent Performance Score (from RecentTeamPerformance model)
            recent_performance = RecentTeamPerformance.objects.get(team=team)
            recent_performance_score = recent_performance.win_percentage_last_5

            # 3. Home/Away Advantage (Home game: use team's home ballpark)
            if is_home:
                ballpark = Ballpark.objects.get(team=team)
                ballpark_score = ballpark.get_dimension_factor() * ballpark.get_altitude_factor() * ballpark.get_rain_factor() * ballpark.get_wind_factor()
            else:
                # Away game: opponent's home ballpark
                ballpark = Ballpark.objects.get(team=opponent)
                ballpark_score = ballpark.get_dimension_factor() * ballpark.get_altitude_factor() * ballpark.get_rain_factor() * ballpark.get_wind_factor()

            # 4. Pitcher Effectiveness Score (from PitcherStats model)
            pitcher_stats = PitcherStats.objects.get(team=opponent)
            pitcher_score = pitcher_stats.get_pitcher_effectiveness_score()

            # Calculate the final prediction score with weighted factors (on a scale from 0 to 1)
            total_score = (team_score * 0.25 + 
                           recent_performance_score * 0.15 + 
                           ballpark_score * 0.20 + 
                           pitcher_score * 0.20 + 
                           game_time_score * 0.10)

            # Normalize the score to be between 0 and 1 (ensures final score is within the desired range)
            prediction_score = min(max(total_score, 0), 1)

    else:
        form = PredictionForm()

    # Pass all the individual factor scores and the final prediction score to the template
    return render(request, 'predictions/predict.html', {
        'form': form,
        'team_score': team_score,
        'recent_performance_score': recent_performance_score,
        'ballpark_score': ballpark_score,
        'pitcher_score': pitcher_score,
        'game_time_score': game_time_score,
        'prediction_score': prediction_score
    })