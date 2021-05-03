# -*- coding: utf-8 -*-
from odoo import http


class Openacademy(http.Controller):
    @http.route('/openacademy/courses/', auth='public', website=True)
    def courses(self, **kw):
        courses = http.request.env['openacademy.course']
        return http.request.render('openacademy.courses', {
            'course': courses.search([])
        })

    @http.route('/openacademy/course/<model("openacademy.course"):course>/',
                auth='public',
                website=True)
    def course_info(self, course):
        return http.request.render('openacademy.course_info', {
            'course': course
        })

    @http.route('/openacademy/sessions/', auth='public', website=True)
    def sessions(self, **kw):
        sessions = http.request.env['openacademy.session']
        return http.request.render('openacademy.sessions', {
            'session': sessions.search([])
        })

    @http.route('/openacademy/session/<model("openacademy.session"):session>/',
                auth='public',
                website=True)
    def session_info(self, session):
        return http.request.render('openacademy.session_info', {
            'session': session
        })
