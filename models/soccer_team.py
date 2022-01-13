from odoo import models, fields


class SoccerTeam(models.Model):
    _name = 'soccer.team'
    _description = "Soccer Team"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']

    api_id = fields.Char()
    name = fields.Char()
    match_ids = fields.One2many('soccer.match', compute='_compute_match_ids')
    player_ids = fields.One2many('soccer.player', 'team_id')
    season_ids = fields.Many2many('soccer.season', 'season_team_relation', 'team_id', 'season_id', copy=False)

    def _compute_match_ids(self):
        for rec in self:
            match_ids = self.env['soccer.match'].search(['|', ('home_team', '=', rec.id), ('away_team', '=', rec.id)])
            rec.match_ids = match_ids
