from .models import TeamPerformance, RecentTeamPerformance, Ballpark, PitcherStats, GameTime

def calculate_team_performance_score(team, opponent, is_home, game_time):
    # Debug: print the game_time value to check it
    print(f"Game Time Passed: {game_time}")

    # Get selected team and opponent
    team_name = team.team_name  
    opponent_name = opponent.team_name

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
    pitcher_stats = PitcherStats.objects.get(team=opponent)  # opponent's pitcher
    pitcher_score = pitcher_stats.get_pitcher_effectiveness_score()
    opponent_advantage_score = pitcher_stats.get_opponent_advantage_score()

    # 5. Day/Night Game Score (from GameTime model)
    if game_time == "day":
        print("Calculating for Day Game")
        # Assuming `get_day_game_score()` returns the score for day games
        game_time_score = GameTime.objects.get(team=team).get_day_game_score()
    elif game_time == "night":
        print("Calculating for Night Game")
        # Assuming `get_night_game_score()` returns the score for night games
        game_time_score = GameTime.objects.get(team=team).get_night_game_score()
    else:
        print("Unknown game time value:", game_time)
        game_time_score = 0  # Default score if game_time is neither "day" nor "night"

    # Combine all scores
    total_score = (team_score + recent_performance_score + ballpark_score + pitcher_score + opponent_advantage_score + game_time_score) / 6

    return total_score