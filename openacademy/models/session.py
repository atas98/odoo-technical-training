# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


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

    seats = fields.Integer()
    taken_seats = fields.Float(compute='_compute_taken_seats')

    @api.depends('attendee_ids', 'seats')
    def _compute_taken_seats(self):
        for record in self:
            record.taken_seats = 100 * len(record.attendee_ids) / record.seats

    @api.constrains('taken_seats')
    def _check_taken_seats(self):
        if self.taken_seats > 100:
            raise ValidationError('Too many attendees')