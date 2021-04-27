# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean(default=False)
    session_ids = fields.Many2many('openacademy.session',
                                   relation='attendee_ids',
                                   string="Attended Sessions",
                                   readonly=True,
                                   auto_join=True)
