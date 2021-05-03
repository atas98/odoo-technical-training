# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError, Warning


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
    end_date = fields.Date(store=True,
                           compute='_get_end_date',
                           inverse='_set_end_date')
    duration = fields.Float(digits=(6, 2), default=1.0)
    seats = fields.Integer()
    is_paid = fields.Boolean(default=False)

    product_id = fields.Many2one('product.template')
    taken_seats = fields.Float(compute='_compute_taken_seats')
    attendees_count = fields.Integer(compute='_compute_attendees_count',
                                     store=True)
    instructor_id = fields.Many2one('res.partner',
                                    domain=[('instructor', '=', True)],
                                    required=True)
    course_id = fields.Many2one('openacademy.course',
                                required=True,
                                ondelete='cascade')
    attendee_ids = fields.Many2many('res.partner')

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

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue

            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            r.duration = (r.end_date - r.start_date).days + 1

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

    def invoice_teacher(self):
        if self.instructor_id:
            # Search for instructor account
            instructor_account_move = self.env['account.move'].search([
                ('partner_id', '=', self.instructor_id.id)
            ], limit=1)
            if not instructor_account_move:
                instructor_account_move = self.env['account.move'].sudo().create({
                    'partner_id': self.instructor_id.id,
                    'type_name': 'out_invoice',
                    'invoice_date': fields.Date.today(),
                    'journal_id': 1
                })
            # Set expense account
            expense_account = self.env['account.account'].search([('user_type_id', '=', \
                self.env.ref('account.data_account_type_expenses').id)], limit=1)

            # Add line to account
            self.env['account.move.line'].sudo().with_context(check_move_validity=False).create({
                'name': self.product_id.name,
                'move_id': instructor_account_move.id,
                'journal_id': 1,
                'account_id': expense_account.id,
                'product_id': self.product_id.id,
                'price_unit': self.product_id.lst_price,
                'date': fields.Date.today()
            })

            # Set session as paid
            self.is_paid = True
        else:
            Warning("Instructor must be set")
