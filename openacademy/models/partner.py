# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Partner(models.Model):
    _name = 'openacademy.partner'

    name = fields.Char()
    instructor = fields.Boolean()
    responsible_id = fields.Many2many('openacademy.session', readonly=True)
