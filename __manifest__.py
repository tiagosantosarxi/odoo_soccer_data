# -*- coding: utf-8 -*-

{
    'name'        : "Soccer Data",
    'version'     : '15.0.0.0.1',
    'category'    : 'Sales/Sales',
    'summary'     : """Soccer Data""",
    'description' : """Soccer Datax""",
    'depends'     : [
        'base',
        'mail'
    ],
    'data'        : [
        'data/ir_config_parameters.xml',
        'security/ir.model.access.csv',
        'views/soccer_data_feed_views.xml',
        'views/soccer_league_views.xml',
        'views/soccer_team_views.xml',
        'views/soccer_player_views.xml',
        'views/soccer_season_views.xml',
        'wizards/soccer_stats_wizard_views.xml',
        'wizards/import_wizard_views.xml',
        'wizards/soccer_matchup_wizard_views.xml'
    ],
    'installable' : True,
    'auto_install': False
}
