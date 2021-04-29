# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class Course(models.Model):
    _name = 'openacademy.course'
    _description = "Open Academy Courses"

    name = fields.Char(required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.partner')
    session_ids = fields.One2many('openacademy.session', 'course_id')
    level = fields.Selection(selection=[("easy", "Easy"),
                                        ("medium", "Medium"),
                                        ("hard", "Hard")])

    attendee_count = fields.Integer(compute='_compute_attendee_count')

    can_edit_responsible = fields.Boolean(
        compute='_compute_can_edit_responsible')

    def _compute_can_edit_responsible(self):
        for r in self:
            r.can_edit_responsible = self.env.user \
                .has_group('openacademy.group_archmaesters')

    @api.depends('session_ids.attendees_count')
    def _compute_attendee_count(self):
        for r in self:
            # Sum all attendees
            attendees = 0
            for session in r.session_ids:
                attendees = attendees + session.attendees_count
            r.attendee_count = attendees

    def open_attendees(self):
        return {
            'name': 'Attendees',
            'view_type': 'form',
            'view_mode': 'tree,form',  # ,form
            'view_id': False,
            'res_model': 'res.partner',
            'type': 'ir.actions.act_window',
            'target': 'main',
            'domain': [('id', 'in', self.session_ids.attendee_ids.ids)]
        }
