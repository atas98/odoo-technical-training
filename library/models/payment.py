from odoo import api, fields, models


class Price(models.Model):
    _name = 'library.payment'

    date = fields.Date(default=fields.Date.today())
    amount = fields.Float()
    customer_id = fields.Many2one('res.partner',
                                  string='Customer',
                                  domain=[('partner_type', '=', 'customer')])
