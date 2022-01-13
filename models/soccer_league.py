from odoo import models, fields

TYPES = [
    ('Cup', 'Cup'),
    ('League', 'League'),
]


class SoccerLeague(models.Model):
    _name = 'soccer.league'
    _description = "Soccer League"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']

    api_id = fields.Char()
    name = fields.Char()
    type = fields.Selection(selection=TYPES)
    country_id = fields.Many2one('res.country')
    season_ids = fields.One2many('soccer.season', 'league_id')
