from odoo import api, fields, models


class Partner(models.Model):
    _name = 'library.partner'
    _description = "Library Partner"

    name = fields.Char()
    email = fields.Char()
    address = fields.Text()
    partner_type = fields.Selection(('customer', 'author'))
    rental_ids = fields.One2many('library.rental', 'customer_id')
