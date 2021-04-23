# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Course(models.Model):
    _name = 'openacademy.course'
    _description = "OpenAcademy Courses"

    name = fields.Char(required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('openacademy.partner')
    session_ids = fields.One2many('openacademy.session', 'course_id')
    level = fields.Selection(("Easy", "Medium", "Hard"))
