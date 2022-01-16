from odoo import models, fields

STATS_MAP_KEYS = {
    'Shots on Goal'   : 'shots_on_goal',
    'Shots off Goal'  : 'shots_off_goal',
    'Total Shots'     : 'total_shots',
    'Blocked Shots'   : 'blocked_shots',
    'Shots insidebox' : 'shots_inside_box',
    'Shots outsidebox': 'shots_outside_box',
    'Fouls'           : 'fouls',
    'Corner Kicks'    : 'corner_kicks',
    'Offsides'        : 'offsides',
    'Ball Possession' : 'ball_possession',
    'Yellow Cards'    : 'yellow_cards',
    'Red Cards'       : 'red_cards',
    'Goalkeeper Saves': 'goalkeeper_saves',
    'Total passes'    : 'total_passes',
    'Passes accurate' : 'passes_accurate',
    'Passes %'        : 'passes_percentage'

}


class SoccerMatch(models.Model):
    _name = 'soccer.match'
    _description = "Soccer Match"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    api_id = fields.Char()
    league_id = fields.Many2one('soccer.league', ondelete='cascade')
    season_id = fields.Many2one('soccer.season', ondelete='cascade')
    date = fields.Datetime()
    status = fields.Char()
    elapsed_time = fields.Float()
    home_team = fields.Many2one('soccer.team', ondelete='cascade')
    away_team = fields.Many2one('soccer.team', ondelete='cascade')
    home_goals = fields.Integer()
    away_goals = fields.Integer()
    result = fields.Selection([('home', 'Home Win'), ('draw', 'Draw'), ('away', 'Away Win')], compute='_compute_result')
    winner = fields.Many2one('soccer.team', compute='_compute_winner')
    home_shots_on_goal = fields.Integer()
    home_shots_off_goal = fields.Integer()
    home_total_shots = fields.Integer()
    home_blocked_shots = fields.Integer()
    home_shots_inside_box = fields.Integer()
    home_shots_outside_box = fields.Integer()
    home_fouls = fields.Integer()
    home_corner_kicks = fields.Integer()
    home_offsides = fields.Integer()
    home_ball_possession = fields.Float()
    home_yellow_cards = fields.Integer()
    home_red_cards = fields.Integer()
    home_goalkeeper_saves = fields.Integer()
    home_total_passes = fields.Integer()
    home_passes_accurate = fields.Integer()
    home_passes_percentage = fields.Float()
    away_shots_on_goal = fields.Integer()
    away_shots_off_goal = fields.Integer()
    away_total_shots = fields.Integer()
    away_blocked_shots = fields.Integer()
    away_shots_inside_box = fields.Integer()
    away_shots_outside_box = fields.Integer()
    away_fouls = fields.Integer()
    away_corner_kicks = fields.Integer()
    away_offsides = fields.Integer()
    away_ball_possession = fields.Float()
    away_yellow_cards = fields.Integer()
    away_red_cards = fields.Integer()
    away_goalkeeper_saves = fields.Integer()
    away_total_passes = fields.Integer()
    away_passes_accurate = fields.Integer()
    away_passes_percentage = fields.Float()
    has_stats = fields.Boolean()

    def _compute_winner(self):
        for rec in self:
            rec.winner = rec.home_team if rec.result == 'home' else rec.away_team if rec.result == 'away' else False

    def _compute_result(self):
        for rec in self:
            rec.result = 'home' if rec.home_goals > rec.away_goals else 'away' if rec.home_goals < rec.away_goals else 'draw'

    def name_get(self):
        result = []
        for match in self:
            name = match.home_team.name + ' vs ' + match.away_team.name + '(' + str(match.home_goals) + '-' + str(
                match.away_goals) + ')' or ''
            result.append((match.id, name))
        return result

    def prepare_games_statistics_vals(self, stat):
        team = 'home_' if stat.get('team').get('id') == int(self.home_team.api_id) else 'away_'
        vals = {
            'has_stats': True
        }
        for stat_line in stat.get('statistics'):
            if STATS_MAP_KEYS.get(stat_line.get('type')) in ['passes_percentage', 'ball_possession']:
                vals.update({
                    team + STATS_MAP_KEYS.get(stat_line.get('type')): float(stat_line.get('value').replace('%', '')) / 100
                })
            else:
                vals.update({
                    team + STATS_MAP_KEYS.get(stat_line.get('type')): stat_line.get('value')
                })
        return vals

    def needs_to_import_stats(self):
        return self.elapsed_time >= 90 and not self.has_stats