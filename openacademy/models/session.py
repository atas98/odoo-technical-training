# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'Open Academy Sessions'
    _inherit = 'mail.thread'

    active = fields.Boolean(default=True)

    name = fields.Char(required=True)
    level = fields.Selection(related='course_id.level', default='easy')
    level_boundary = fields.Integer(compute='_compute_level_boundary',
                                    readonly=True)
    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('confirmed', 'Confirmed'),
                                        ('done', 'Done')],
                             default='draft',
                             tracking=True,
                             groups='openacademy.group_maesters')
    start_date = fields.Date(default=fields.Date.today())
    end_date = fields.Date(default=fields.Date.today())
    duration = fields.Float(digits=(6, 2), default=1.0)

    instructor_id = fields.Many2one('res.partner',
                                    domain=[('instructor', '=', True)],
                                    required=True)
    course_id = fields.Many2one('openacademy.course',
                                required=True,
                                ondelete='cascade')

    # @api.model
    # def _attendee_domain(self):
    #     return [('level', '>=', self.level_boundary)]   

    attendee_ids = fields.Many2many('res.partner')

    seats = fields.Integer()
    taken_seats = fields.Float(compute='_compute_taken_seats')

    attendees_count = fields.Integer(compute='_compute_attendees_count',
                                     stored=True)

    @api.depends('level')
    def _compute_level_boundary(self):
        for r in self:
            if r.level == 'easy':
                r.level_boundary = 0
            elif r.level == 'medium':
                r.level_boundary = 4
            elif r.level == 'hard':
                r.level_boundary = 7
            else:
                r.level_boundary = 0

    @api.model
    def create(self, values):
        session = super(Session, self).create(values)
        # Confirm session with more then half taken seats
        if self.taken_seats >= 50 and self.state == 'draft':
            self.state = 'confirmed'

        # Add instructor to chatter
        self.message_subscribe([self.instructor_id.id])

        return session

    def write(self, values):
        session = super(Session, self).write(values)
        # Confirm session with more then half taken seats
        if self.taken_seats >= 50 and self.state == 'draft':
            self.state = 'confirmed'

        # Add instructor to chatter
        self.message_subscribe([self.instructor_id.id])

        return session

    @api.depends('attendee_ids', 'seats')
    def _compute_taken_seats(self):
        for r in self:
            if r.seats:
                r.taken_seats = 100 * r.attendees_count / r.seats
            else:
                r.taken_seats = 0.0

    @api.depends('attendee_ids')
    def _compute_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)

    @api.constrains('attendee_ids')
    def _validate_taken_seats(self):
        for r in self:
            if r.taken_seats > 100.0:
                raise ValidationError('Number of attendees exceeds the number of availible seats')

    # Header buttons handlers
    def action_confirm(self):
        for r in self:
            r.state = 'confirmed'

    def action_done(self):
        for r in self:
            r.state = 'done'

    def action_draft(self):
        for r in self:
            r.state = 'draft'
