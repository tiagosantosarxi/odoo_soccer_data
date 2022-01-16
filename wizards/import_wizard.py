import json

from dateutil import parser

from odoo import models, fields

IMPORT_TYPES = [
    ('team', 'From Team'),
    ('league', 'From League'),
    ('leagues', 'Leagues')
]


class SoccerDataImportWizard(models.TransientModel):
    _name = 'soccer.data.import.wizard'
    _inherit = 'api.communication.mixin'
    _description = 'API Communication Mixin'

    import_type = fields.Selection(IMPORT_TYPES)
    league_id = fields.Many2one('soccer.league')
    team_id = fields.Many2one('soccer.team')
    year = fields.Char()
    extra_statistics = fields.Boolean()

    def _prepare_league_vals(self, league):
        country = self.env['res.country'].search([('name', '=', league.get('country').get('name'))])
        if not country:
            country.create({
                'name': league.get('country').get('name')
            })
        vals = {
            'api_id'    : league.get('league').get('id'),
            'name'      : league.get('league').get('name'),
            'type'      : league.get('league').get('type'),
            'country_id': country.id
        }
        return vals

    def _prepare_game_vals(self, game):
        league_id = self.env['soccer.league'].search([('api_id', '=', game.get('league').get('id'))], limit=1)
        if not league_id:
            league_id = self.env['soccer.league'].create({
                'api_id': game.get('league').get('id'),
                'name'  : game.get('league').get('name')
            })
        season_id = self.env['soccer.season'].search(
            [('league_id', '=', league_id.id), ('year', '=', game.get('league').get('season'))], limit=1)
        if not season_id:
            season_id = self.env['soccer.season'].create({
                'league_id': league_id.id,
                'year'     : game.get('league').get('season')
            })
        home_team = self.env['soccer.team'].search([('api_id', '=', game.get('teams').get('home').get('id'))], limit=1)
        if not home_team:
            home_team = self.env['soccer.team'].create({
                'api_id'    : game.get('teams').get('home').get('id'),
                'name'      : game.get('teams').get('home').get('name'),
                'season_ids': [(6, 0, season_id.ids)]
            })
        if season_id not in home_team.season_ids:
            home_team.write({
                "season_ids": [(4, season_id.id)],
            })
        away_team = self.env['soccer.team'].search([('api_id', '=', game.get('teams').get('away').get('id'))], limit=1)
        if not away_team:
            away_team = self.env['soccer.team'].create({
                'api_id'    : game.get('teams').get('away').get('id'),
                'name'      : game.get('teams').get('away').get('name'),
                'season_ids': [(6, 0, season_id.ids)]
            })
        if season_id not in away_team.season_ids:
            away_team.write({
                "season_ids": [(4, season_id.id)],
            })
        vals = {
            'api_id'      : game.get('fixture').get('id'),
            'date'        : parser.parse(game.get('fixture').get('date')).replace(tzinfo=None),
            'status'      : game.get('fixture').get('status').get('long'),
            'elapsed_time': game.get('fixture').get('status').get('elapsed') and float(
                game.get('fixture').get('status').get('elapsed')),
            'home_goals'  : game.get('goals').get('home'),
            'away_goals'  : game.get('goals').get('away'),
            'home_team'   : home_team.id,
            'away_team'   : away_team.id,
            'league_id'   : league_id.id,
            'season_id'   : season_id.id,
        }
        return vals

    def import_data(self):
        if self.import_type == 'team':
            self.import_games_from_team()
        elif self.import_type == 'league':
            self.import_games_from_league_by_season_id()
        elif self.import_type == 'leagues':
            self.import_leagues()

    def import_leagues(self):
        endpoint = '/v3/leagues'
        type = 'GET'
        params = {}
        response = self.call(endpoint, type, params)
        json_response = json.loads(response.content)
        for league in json_response.get('response'):
            if not self.env['soccer.league'].search([('api_id', '=', league.get('league').get('id'))]):
                self.env['soccer.league'].create(self._prepare_league_vals(league))

    def import_games_from_team(self):
        endpoint = '/v3/fixtures'
        type = 'GET'
        params = {
            'team'  : self.team_id.api_id,
            'season': self.year
        }
        response = self.call(endpoint, type, params)
        json_response = json.loads(response.content)
        for game in json_response.get('response'):
            self.find_or_create_game(game)

    def import_games_from_league_by_season_id(self):
        endpoint = '/v3/fixtures'
        type = 'GET'
        params = {
            'league': self.league_id.api_id,
            'season': self.year
        }
        response = self.call(endpoint, type, params)
        json_response = json.loads(response.content)
        for game in json_response.get('response'):
            self.find_or_create_game(game)

    def find_or_create_game(self, game):
        game_id = self.env['soccer.match'].search([('api_id', '=', game.get('fixture').get('id'))])
        if not game_id:
            game_id = self.env['soccer.match'].create(self._prepare_game_vals(game))
        if self.extra_statistics and game_id.needs_to_import_stats():
            endpoint = '/v3/fixtures/statistics'
            type = 'GET'
            params = {
                'fixture': game_id.api_id
            }
            response = self.call(endpoint, type, params)
            json_response = json.loads(response.content)
            if json_response and json_response.get('response'):
                for stat in json_response.get('response'):
                    game_id.write(game_id.prepare_games_statistics_vals(stat))
        return game_id
