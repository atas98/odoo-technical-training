from odoo import api, fields, models


class Price(models.Model):
    _name = 'library.price'

    name = fields.Char()
    duration = fields.Float()
    price = fields.Float()
    type = fields.Selection(selection=[('time', 'Time'),
                                       ('one', 'One')],
                            default='time')
