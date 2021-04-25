# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Session(models.Model):
    _name = 'openacademy.session'

    active = fields.Boolean(default=True)

    name = fields.Char(required=True)
    state = fields.Selection(selection=[('draft', 'Draft'), 
                                        ('confirmed', 'Confirmed'), 
                                        ('done', 'Done')], default='draft')
    start_date = fields.Date(default=fields.Date.today())
    end_date = fields.Date(default=fields.Date.today())
    duration = fields.Float(digits=(6, 2), default=1.0)
    instructor_id = fields.Many2one('openacademy.partner')
    course_id = fields.Many2one('openacademy.course',
                                required=True,
                                ondelete='cascade')
    attendee_ids = fields.Many2many('openacademy.partner')

    seats = fields.Integer()
    taken_seats = fields.Float(compute='_compute_taken_seats')

    @api.depends('attendee_ids', 'seats')
    def _compute_taken_seats(self):
        for r in self:
            if r.seats:
                r.taken_seats = 100 * len(r.attendee_ids) / r.seats
            else:
                r.taken_seats = 0.0

    @api.constrains('attendee_ids')
    def _check_taken_seats(self):
        for r in self:
            if r.taken_seats > 100.0:
                raise ValidationError('Number of attendees exceeds the number of availible seats')
