import requests

from odoo import models
from odoo.exceptions import ValidationError


class ApiCommunicationMixin(models.AbstractModel):
    _name = 'api.communication.mixin'
    _description = 'API Communication Mixin'

    def call(self, endpoint, type, params=False):
        x_rapidapi_key = self.env['ir.config_parameter'].sudo().get_param('x-rapidapi-key')
        x_rapidapi_host = self.env['ir.config_parameter'].sudo().get_param('x-rapidapi-host')
        url = 'https://' + x_rapidapi_host + endpoint
        if not x_rapidapi_host or not x_rapidapi_host:
            raise ValidationError("Error setting up API headers. Check System Parameters.")
        headers = {
            'x-rapidapi-key' : x_rapidapi_key,
            'x-rapidapi-host': x_rapidapi_host
        }
        response = requests.request(type, url, headers=headers, params=params)
        return response
