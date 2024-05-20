from django.db import models

class Team(models.Model):
    poke1 = models.CharField(max_length=100, null=False, blank=False)
    poke2 = models.CharField(max_length=100, null=False, blank=False)
    poke3 = models.CharField(max_length=100, null=False, blank=False)
    poke4 = models.CharField(max_length=100, null=False, blank=False)
    poke5 = models.CharField(max_length=100, null=False, blank=False)
    poke6 = models.CharField(max_length=100, null=False, blank=False)


class History(models.Model):
    date = models.DateField()
    player = models.CharField(max_length=100, null=False, blank=False)
    opponent = models.CharField(max_length=100, null=False, blank=False)
    platform = models.CharField(max_length=100, null=True, blank=True)
    event = models.CharField(max_length=100, null=True, blank=True)
    player_score = models.IntegerField(null=True)
    opp_score = models.IntegerField(null=True)
    player_win = models.BooleanField()
    observations = models.TextField()
    player_team_paste = models.CharField(max_length=255, null=True, blank=True)
    opp_team_paste = models.CharField(max_length=255, null=True, blank=True)
    opp_guild_name = models.CharField(max_length=100, null=True, blank=True)
    player_team = models.OneToOneField(Team, on_delete=models.CASCADE, null=True, related_name='Player_team')
    opp_team = models.OneToOneField(Team, on_delete=models.CASCADE, null=True, related_name='Opponent_team')
