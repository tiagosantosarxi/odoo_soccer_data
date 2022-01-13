import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class SoccerPlayer(models.Model):
    _name = 'soccer.player'
    _description = 'Soccer Player'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']

    name = fields.Char()
    full_name = fields.Char()
    country_id = fields.Many2one('res.country')
    team_id = fields.Many2one('soccer.team')
