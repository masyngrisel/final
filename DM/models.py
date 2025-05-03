from django.db import models

from django.db import models

class TeamPerformance(models.Model):
    team_name = models.CharField(max_length=100, unique=True)
    wins = models.PositiveIntegerField()
    losses = models.PositiveIntegerField()
    avg_runs_scored = models.FloatField()
    avg_runs_allowed = models.FloatField()

    def win_percentage(self):
        """Calculate win percentage."""
        total_games = self.wins + self.losses
        return self.wins / total_games if total_games > 0 else 0

    def calculate_performance_score(self):
        """Calculate performance score based on win percentage and runs scored/allowed."""
        win_score = self.win_percentage()  
        offensive_score = self.avg_runs_scored  
        defensive_score = 1 / (self.avg_runs_allowed + 1)  

        # Normalize offensive and defensive scores by taking them as percentages
        offensive_score = offensive_score / 10  
        defensive_score = defensive_score * 10  

        # Final performance score
        performance_score = (win_score * 0.4) + (offensive_score * 0.3) + (defensive_score * 0.3)
        
        return performance_score

    def __str__(self):
        return self.team_name
    

class Ballpark(models.Model):
    team = models.OneToOneField(TeamPerformance, on_delete=models.CASCADE, related_name='home_ballpark', null=True, blank=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    
    DIMENSION_CHOICES = [
        ('small', 'Small'),
        ('average', 'Average'),
        ('large', 'Large'),
    ]
    dimensions = models.CharField(max_length=10, choices=DIMENSION_CHOICES)
    
    altitude = models.IntegerField(help_text="Altitude in feet")
    
    wind = models.CharField(
        max_length=11,
        choices=[
            ('blowing_in', 'Blowing In'),
            ('blowing_out', 'Blowing Out'),
            ('no_wind', 'No Wind')
        ],
        default='no_wind'
    )

    rain = models.BooleanField(default=False)

    def get_dimension_factor(self):
        """Returns a factor based on field dimensions."""
        return {'small': 1, 'average': 0.5, 'large': 0}.get(self.dimensions, 0.5)

    def get_altitude_factor(self):
        """Returns a factor based on the altitude."""
        return self.altitude / 1000  # Normalize by dividing by 1000 for easier comparison.

    def get_rain_factor(self):
        """Rain reduces scoring, so we give it a factor."""
        return 0.5 if self.rain else 1

    def get_wind_factor(self):
        """Return wind factor: Blowing out helps scoring, Blowing in reduces scoring."""
        return {
            'blowing_in': 0.5,
            'blowing_out': 1.5,
            'no_wind': 1
        }.get(self.wind, 1)

    def calculate_ballpark_score(self):
        """Calculate a score for the ballpark based on its characteristics."""
        dimension_score = self.get_dimension_factor()  # Small fields benefit batters.
        altitude_score = self.get_altitude_factor()  # Higher altitudes benefit batters.
        rain_score = self.get_rain_factor()  # Rain reduces scoring potential.
        wind_score = self.get_wind_factor()  # Wind can increase or decrease scoring.

        # Combine all factors to calculate the final ballpark score
        ballpark_score = (dimension_score + altitude_score + rain_score + wind_score) / 4

        return ballpark_score

    def __str__(self):
        return self.name
    
    
class PitcherStats(models.Model):
    team = models.OneToOneField(TeamPerformance, on_delete=models.CASCADE, related_name='pitcher_stats')
    name = models.CharField(max_length=100)
    era = models.FloatField(help_text="Earned Run Average")
    whip = models.FloatField(help_text="Walks + Hits per Inning Pitched")
    opponent_batting_avg = models.FloatField(help_text="Team's batting average against this pitcher")
    league_avg_batting_avg = models.FloatField(default=0.250, help_text="League-wide batting average for comparison")

    def get_pitcher_effectiveness_score(self):
        """
        Combine ERA and WHIP: lower is better.
        Normalize relative to league expectations. 
        Lower score = better performance.
        """
        # Combine ERA and WHIP for a general pitcher effectiveness score
        effectiveness = (self.era + self.whip) / 2
        return effectiveness

    def get_opponent_advantage_score(self):
        """
        If the team hits better than league average against this pitcher, it's an advantage.
        Score > 1 = advantage, < 1 = disadvantage.
        """
        if self.league_avg_batting_avg > 0:
            return self.opponent_batting_avg / self.league_avg_batting_avg
        return 1  

    def calculate_pitcher_score(self):
        """
        Calculate the final score for the pitcher, combining effectiveness and opponent advantage.
        Lower score means better pitcher performance.
        """
        effectiveness_score = self.get_pitcher_effectiveness_score()
        opponent_advantage_score = self.get_opponent_advantage_score()

        # Combine the scores 
        pitcher_score = (effectiveness_score + opponent_advantage_score) / 2

        return pitcher_score

    def __str__(self):
        return f"{self.name} ({self.team.team_name})"
    


class RecentTeamPerformance(models.Model):
    team = models.ForeignKey(TeamPerformance, on_delete=models.CASCADE, related_name='recent_performance')
    wins_last_5 = models.IntegerField(default=0)  # Number of wins in the last 5 games
    losses_last_5 = models.IntegerField(default=0)  # Number of losses in the last 5 games
    win_percentage_last_5 = models.FloatField(default=0.0)  # Win percentage in the last 5 games

    def update_win_loss(self):
        total_games = self.wins_last_5 + self.losses_last_5
        if total_games > 0:
            self.win_percentage_last_5 = self.wins_last_5 / total_games
        else:
            self.win_percentage_last_5 = 0  # No games played yet

    def get_recent_performance_score(self):
        """
        Calculate a score based on the win percentage in the last 5 games.
        Teams with higher win percentages will have a better score.
        """
        if self.win_percentage_last_5 >= 0.7:
            return 1.0  # Excellent performance
        elif self.win_percentage_last_5 >= 0.4:
            return 0.5  # Average performance
        else:
            return 0.2  # Poor performance

    def __str__(self):
        return f"{self.team.team_name} - Recent Performance"
    
    
class GameTime(models.Model):
    team = models.ForeignKey(TeamPerformance, on_delete=models.CASCADE, related_name='game_time')
    wins_day = models.PositiveIntegerField(default=0)  # Wins in day games
    losses_day = models.PositiveIntegerField(default=0)  # Losses in day games
    wins_night = models.PositiveIntegerField(default=0)  # Wins in night games
    losses_night = models.PositiveIntegerField(default=0)  # Losses in night games

    def win_percentage_day(self):
        """Calculates the win percentage in day games."""
        total_day_games = self.wins_day + self.losses_day
        return self.wins_day / total_day_games if total_day_games > 0 else 0

    def win_percentage_night(self):
        """Calculates the win percentage in night games."""
        total_night_games = self.wins_night + self.losses_night
        return self.wins_night / total_night_games if total_night_games > 0 else 0

    def get_day_game_score(self):
        """Creates a score for the team based on its day game win percentage."""
        win_percentage = self.win_percentage_day()
        if win_percentage >= 0.7:
            return 1.0  # Excellent performance
        elif win_percentage >= 0.4:
            return 0.5  # Average performance
        else:
            return 0.2  # Poor performance

    def get_night_game_score(self):
        """Creates a score for the team based on its night game win percentage."""
        win_percentage = self.win_percentage_night()
        if win_percentage >= 0.7:
            return 1.0  # Excellent performance
        elif win_percentage >= 0.4:
            return 0.5  # Average performance
        else:
            return 0.2  # Poor performance

    def __str__(self):
        return f"{self.team.team_name} - Day/Night Performance"