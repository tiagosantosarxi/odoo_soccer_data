from odoo import models, fields, api


class SoccerStatsWizard(models.TransientModel):
    _name = 'soccer.stats.wizard'
    _description = 'Soccer Stats Wizard'

    team_id = fields.Many2one('soccer.team')
    season_ids = fields.Many2many('soccer.season')
    pythagorean_expectation_percentage = fields.Float(compute='_compute_pythagorean_expectation_percentage')
    real_win_percentage = fields.Float(compute='_compute_real_win_percentage')
    home_pythagorean_expectation_percentage = fields.Float(compute='_compute_home_pythagorean_expectation_percentage')
    home_real_win_percentage = fields.Float(compute='_compute_home_real_win_percentage')
    away_pythagorean_expectation_percentage = fields.Float(compute='_compute_away_pythagorean_expectation_percentage')
    away_real_win_percentage = fields.Float(compute='_compute_away_real_win_percentage')
    selectable_season_ids = fields.Many2many(related='team_id.season_ids')

    @api.onchange('team_id')
    def onchange_team_id(self):
        self.season_ids = False

    @api.onchange('season_ids')
    def onchange_season_ids(self):
        self._compute_real_win_percentage()
        self._compute_pythagorean_expectation_percentage()
        self._compute_away_real_win_percentage()
        self._compute_away_pythagorean_expectation_percentage()
        self._compute_home_real_win_percentage()
        self._compute_home_pythagorean_expectation_percentage()

    def _compute_real_win_percentage(self):
        for rec in self:
            rec.real_win_percentage = len(
                rec.season_ids.mapped('match_ids').filtered(
                    lambda l: l.elapsed_time > 0 and l.winner == rec.team_id)) / len(
                rec.season_ids.mapped('match_ids').filtered(
                    lambda l: l.elapsed_time > 0 and rec.team_id in [l.home_team,
                                                                     l.away_team])) if rec.season_ids else 0

    def _compute_pythagorean_expectation_percentage(self):
        for rec in self:
            goals_scored = sum(rec.season_ids.mapped('match_ids').filtered(
                lambda l: l.elapsed_time > 0 and l.home_team == rec.team_id).mapped(
                'home_goals') + rec.season_ids.mapped('match_ids').filtered(
                lambda l: l.elapsed_time > 0 and l.away_team == rec.team_id).mapped(
                'away_goals'))
            goals_suffered = sum(
                rec.season_ids.mapped('match_ids').filtered(
                    lambda l: l.elapsed_time > 0 and l.home_team == rec.team_id).mapped(
                    'away_goals') + rec.mapped('season_ids').match_ids.filtered(
                    lambda l: l.elapsed_time > 0 and l.away_team == rec.team_id).mapped(
                    'home_goals'))
            rec.pythagorean_expectation_percentage = goals_scored / (
                    goals_scored + goals_suffered) if rec.season_ids else 0

    def _compute_home_real_win_percentage(self):
        for rec in self:
            rec.home_real_win_percentage = len(
                rec.season_ids.mapped('match_ids').filtered(
                    lambda l: l.elapsed_time > 0 and l.winner == rec.team_id and l.home_team == rec.team_id)) / len(
                rec.season_ids.mapped('match_ids').filtered(
                    lambda l: l.elapsed_time > 0 and l.home_team == rec.team_id)) if rec.season_ids else 0

    def _compute_home_pythagorean_expectation_percentage(self):
        for rec in self:
            goals_scored = sum(rec.season_ids.mapped('match_ids').filtered(
                lambda l: l.elapsed_time > 0 and l.home_team == rec.team_id).mapped(
                'home_goals'))
            goals_suffered = sum(rec.season_ids.mapped('match_ids').filtered(
                lambda l: l.elapsed_time > 0 and l.home_team == rec.team_id).mapped(
                'away_goals'))
            rec.home_pythagorean_expectation_percentage = goals_scored / (
                    goals_scored + goals_suffered) if rec.season_ids else 0

    def _compute_away_real_win_percentage(self):
        for rec in self:
            rec.away_real_win_percentage = len(
                rec.season_ids.mapped('match_ids').filtered(
                    lambda l: l.elapsed_time > 0 and l.winner == rec.team_id and l.away_team == rec.team_id)) / len(
                rec.season_ids.mapped('match_ids').filtered(
                    lambda l: l.elapsed_time > 0 and l.away_team == rec.team_id)) if rec.season_ids else 0

    def _compute_away_pythagorean_expectation_percentage(self):
        for rec in self:
            goals_scored = sum(rec.season_ids.mapped('match_ids').filtered(
                lambda l: l.elapsed_time > 0 and l.away_team == rec.team_id).mapped(
                'away_goals'))
            goals_suffered = sum(rec.season_ids.mapped('match_ids').filtered(
                lambda l: l.elapsed_time > 0 and l.away_team == rec.team_id).mapped(
                'home_goals'))
            rec.away_pythagorean_expectation_percentage = goals_scored / (
                    goals_scored + goals_suffered) if rec.season_ids else 0
