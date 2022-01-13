from odoo import models, fields


class SoccerSeason(models.Model):
    _name = 'soccer.season'
    _description = "Soccer Season"
    _rec_name = 'full_name'

    year = fields.Char()
    full_name = fields.Char(compute='_compute_full_name')
    league_id = fields.Many2one('soccer.league')
    match_ids = fields.One2many('soccer.match', 'season_id')
    team_ids = fields.Many2many('soccer.team', 'season_team_relation', 'season_id', 'team_id', copy=False)

    def _compute_full_name(self):
        for rec in self:
            rec.full_name = rec.year + ' - ' + rec.league_id.name if rec.league_id else rec.year
