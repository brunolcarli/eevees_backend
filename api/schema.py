import graphene
from django.conf import settings
from api.models import Team, History
from api.util import get_team, read_paste_url


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


###################################
# QUERY
###################################


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


###################################
# MUTATION
###################################

class CreateHistoryRecord(graphene.relay.ClientIDMutation):
    history = graphene.Field(HistoryType)

    class Input:
        date = graphene.Date(required=True)
        player = graphene.String(required=True)
        opponent = graphene.String(required=True)
        platform = graphene.String()
        event = graphene.String()
        player_score = graphene.Int()
        opp_score = graphene.Int()
        player_win = graphene.Boolean(required=True)
        observations = graphene.String()
        player_team_paste = graphene.String()
        opp_team_paste = graphene.String()
        opp_guild_name = graphene.String()

    def mutate_and_get_payload(self, info, **kwargs):


        # Validate teams
        if not kwargs.get('player_team_paste') or 'https://pokepast' not in kwargs.get('player_team_paste', ''):
            raise Exception('Player team pokepaste is required')
        
        if not kwargs.get('opp_team_paste') or 'https://pokepast' not in kwargs.get('opp_team_paste', ''):
            raise Exception('Opponent team pokepaste is required')

        if kwargs.get('player_score') is not None and kwargs.get('opp_score') is not None:
            kwargs['player_win'] = kwargs['player_score'] > kwargs['opp_score']

        # Create battle history
        record = History.objects.create(**kwargs)

        # create player team
        player_teamlist = get_team(read_paste_url(kwargs['player_team_paste']))
        player_team = Team.objects.create(**player_teamlist)

        # create opponent team
        opp_teamlist = get_team(read_paste_url(kwargs['opp_team_paste']))
        opp_team = Team.objects.create(**opp_teamlist)

        # save objects
        player_team.save()
        opp_team.save()
        record.player_team = player_team
        record.opp_team = opp_team
        record.save()

        return CreateHistoryRecord(record)


class Mutation:
    create_history_record = CreateHistoryRecord.Field()
