from odoo import models, fields, api


class SoccerMatchupWizard(models.TransientModel):
    _name = 'soccer.matchup.wizard'
    _description = 'Soccer Matchup Wizard'

    home_team_id = fields.Many2one('soccer.team')
    away_team_id = fields.Many2one('soccer.team')
    home_pythagorean_expectation_percentage = fields.Float(compute='_compute_pythagorean_expectation_percentage')
    away_pythagorean_expectation_percentage = fields.Float(compute='_compute_pythagorean_expectation_percentage')
    matchups = fields.One2many('soccer.match', compute='_compute_matchups')
    home_head_to_head_pythagorean_expectation_percentage = fields.Float(
        compute='_compute_head_to_head_pythagorean_expectation_percentage')
    away_head_to_head_pythagorean_expectation_percentage = fields.Float(
        compute='_compute_head_to_head_pythagorean_expectation_percentage')
    home_global_head_to_head_pythagorean_expectation_percentage = fields.Float(
        compute='_compute_head_to_head_pythagorean_expectation_percentage')
    away_global_head_to_head_pythagorean_expectation_percentage = fields.Float(
        compute='_compute_head_to_head_pythagorean_expectation_percentage')

    @api.depends('home_team_id', 'away_team_id')
    def _compute_matchups(self):
        for rec in self:
            rec.matchups = [(6, 0, rec.home_team_id.match_ids.filtered(
                lambda m: (m.home_team == rec.home_team_id and m.away_team == rec.away_team_id and m.elapsed_time > 0) or (
                        m.home_team == rec.away_team_id and m.away_team == rec.home_team_id) and m.elapsed_time > 0).ids)] if rec.home_team_id and rec.away_team_id else False

    @api.onchange('home_team_id', 'away_team_id')
    def onchange_season_ids(self):
        self._compute_pythagorean_expectation_percentage()

    def _compute_pythagorean_expectation_percentage(self):
        for rec in self:
            home_team_goals_scored = sum(rec.home_team_id.match_ids.filtered(
                lambda l: l.elapsed_time > 0 and l.home_team == rec.home_team_id).mapped(
                'home_goals'))
            home_goals_suffered = sum(
                rec.home_team_id.match_ids.filtered(
                    lambda l: l.elapsed_time > 0 and l.home_team == rec.home_team_id).mapped(
                    'away_goals'))
            rec.home_pythagorean_expectation_percentage = home_team_goals_scored / (
                    home_team_goals_scored + home_goals_suffered) if rec.home_team_id else 0
            away_team_goals_scored = sum(rec.away_team_id.match_ids.filtered(
                lambda l: l.elapsed_time > 0 and l.away_team == rec.away_team_id).mapped(
                'away_goals'))
            away_goals_suffered = sum(
                rec.away_team_id.match_ids.filtered(
                    lambda l: l.elapsed_time > 0 and l.away_team == rec.away_team_id).mapped(
                    'home_goals'))
            rec.away_pythagorean_expectation_percentage = away_team_goals_scored / (
                    away_team_goals_scored + away_goals_suffered) if rec.away_team_id else 0

    @api.depends('home_team_id', 'away_team_id')
    def _compute_head_to_head_pythagorean_expectation_percentage(self):
        for rec in self:
            home_head_to_head_team_goals_scored = sum(rec.matchups.filtered(
                lambda
                    l: l.elapsed_time > 0 and l.home_team == rec.home_team_id).mapped(
                'home_goals'))
            home_head_to_head_goals_suffered = sum(
                rec.matchups.filtered(
                    lambda
                        l: l.elapsed_time > 0 and l.home_team == rec.home_team_id).mapped(
                    'away_goals'))
            rec.home_head_to_head_pythagorean_expectation_percentage = home_head_to_head_team_goals_scored / (
                    home_head_to_head_team_goals_scored + home_head_to_head_goals_suffered) if rec.home_team_id and rec.away_team_id and home_head_to_head_team_goals_scored + home_head_to_head_goals_suffered > 0 else 0
            rec.away_head_to_head_pythagorean_expectation_percentage = home_head_to_head_goals_suffered / (
                    home_head_to_head_goals_suffered + home_head_to_head_team_goals_scored) if rec.home_team_id and rec.away_team_id and home_head_to_head_team_goals_scored + home_head_to_head_goals_suffered > 0 else 0
            head_to_head_home_team_goals_scored = sum(rec.matchups.filtered(
                lambda
                    l: l.elapsed_time > 0 and l.home_team == rec.home_team_id).mapped(
                'home_goals')) + sum(
                rec.matchups.filtered(
                    lambda
                        l: l.elapsed_time > 0 and l.home_team == rec.away_team_id).mapped(
                    'away_goals'))
            head_to_head_away_team_goals_scored = sum(rec.matchups.filtered(
                lambda
                    l: l.elapsed_time > 0 and l.home_team == rec.home_team_id).mapped(
                'away_goals')) + sum(
                rec.matchups.filtered(
                    lambda
                        l: l.elapsed_time > 0 and l.home_team == rec.away_team_id).mapped(
                    'home_goals'))
            rec.home_global_head_to_head_pythagorean_expectation_percentage = head_to_head_home_team_goals_scored / (
                    head_to_head_home_team_goals_scored + head_to_head_away_team_goals_scored) if rec.home_team_id and rec.away_team_id and head_to_head_home_team_goals_scored + head_to_head_away_team_goals_scored > 0 else 0
            rec.away_global_head_to_head_pythagorean_expectation_percentage = head_to_head_away_team_goals_scored / (
                    head_to_head_away_team_goals_scored + head_to_head_home_team_goals_scored) if rec.home_team_id and rec.away_team_id and head_to_head_away_team_goals_scored + head_to_head_home_team_goals_scored > 0 else 0
