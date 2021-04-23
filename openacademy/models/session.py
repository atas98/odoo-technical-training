# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Session(models.Model):
    _name = 'openacademy.session'

    active = fields.Boolean(default=True)

    name = fields.Char(required=True)
    state = fields.Selection(('draft', 'confirmed', 'done'), default='draft')
    start_date = fields.Date(default=fields.Date.today())
    end_date = fields.Date(default=fields.Date.today())
    duration = fields.Float(digits=(4, 2), default=1.0)
    instructor_id = fields.Many2one('openacademy.partner')
    course_id = fields.Many2one('openacademy.course',
                                required=True,
                                ondelete='cascade')
    attendee_ids = fields.Many2many('openacademy.partner')
