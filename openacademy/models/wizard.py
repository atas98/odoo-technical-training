# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Wizard(models.TransientModel):
    _name = "openacademy.wizard"
    _description = "Wizard: Quick Registration of Attendees to Sessions"

    def _default_attendees(self):
        return self.env['res.partner'].browse(self._context.get('active_ids'))

    session_id = fields.Many2many('openacademy.session',
        string="Session", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees",
                                    default=_default_attendees)

    def subscribe(self):
        self.session_id.attendee_ids |= self.attendee_ids
        return {}
