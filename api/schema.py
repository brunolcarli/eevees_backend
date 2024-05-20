import graphene
from django.conf import settings
from api.models import Team, History

class TeamType(graphene.ObjectType):
    poke1 = graphene.String()
    poke2 = graphene.String()
    poke3 = graphene.String()
    poke4 = graphene.String()
    poke5 = graphene.String()
    poke6 = graphene.String()


class HistoryType(graphene.ObjectType):
    date = graphene.Date()
    player = graphene.String()
    opponent = graphene.String()
    platform = graphene.String()
    event = graphene.String()
    player_score = graphene.Int()
    opp_score = graphene.Int()
    player_win = graphene.Boolean()
    observations = graphene.String()
    player_team_paste = graphene.String()
    opp_team_paste = graphene.String()
    opp_guild_name = graphene.String()
    player_team = graphene.Field(TeamType)
    opp_team = graphene.Field(TeamType)




class Query:
    version = graphene.String()
    def resolve_version(self, info, **kwargs):
        return settings.VERSION

    history = graphene.List(
        HistoryType,
        date=graphene.Date(description='Filter by date'),
        date__gte=graphene.Date(description='Filter by date greater or equal inputed date value'),
        date__lte=graphene.Date(description='Filter by date lesser or equal inputed date value'),
        player=graphene.String(description='Filter by player name'),
        opponent=graphene.String(description='Filter by opponent name'),
        event=graphene.String(description='Filter by event name'),
        player_win=graphene.Boolean(description='Filter by player battle result (true for win, false for lose)')
    )
    def resolve_history(self, info, **kwargs):
        return History.objects.filter(**kwargs)

