from odoo import api, fields, models


class Publisher(models.Model):
    _name = 'library.publisher'
    _description = "Library Publisher"

    name = fields.Char()
