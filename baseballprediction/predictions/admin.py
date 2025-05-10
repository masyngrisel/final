from django.contrib import admin

from django.contrib import admin
from .models import TeamPerformance, Ballpark, PitcherStats, RecentTeamPerformance, GameTime

# Register your models
admin.site.register(TeamPerformance)
admin.site.register(Ballpark)
admin.site.register(PitcherStats)
admin.site.register(RecentTeamPerformance)
admin.site.register(GameTime)
