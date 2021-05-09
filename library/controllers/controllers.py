# -*- coding: utf-8 -*-
from odoo import fields, http
from datetime import timedelta


class Library(http.Controller):
    @http.route('/library/books/', auth='user', website=True)
    def book_list_route(self, **kw):
        books = http.request.env['library.copy']
        return http.request.render('library.website_books', {
            'books': books.search([('book_state', '!=', 'lost')])
        })

    @http.route('/library/books/<model("library.copy"):book>/',
                auth='user',
                website=True)
    def book_info_route(self, book):
        if book.book_state == 'available':
            return http.request.render('library.website_rent_confirm', {
                'book': book
            })
        elif book.book_state == 'rented':
            return http.request.redirect('/library/books/already_rented')
        else:
            return

    @http.route('/library/books/already_rented', auth='user', website=True)
    def already_rented_route(self, **kw):
        return http.request.render('library.website_already_rented', {})

    @http.route('/library/books/<model("library.copy"):book>/confirmed',
                auth='user', website=True)
    def rental_complete_route(self, book):
        new_rental = http.request.env['library.rental'].create({
            "copy_id": book.id,
            "customer_id": http.request.env.user.id,
            "rental_date": fields.Date.today(),
            "return_date": fields.Date.today()+timedelta(days=30),
            "planned_return_date": fields.Date.today()+timedelta(days=30)
        })
        new_rental.action_confirm()
        return http.request.render('library.website_rental_complete', {})


# Book list -> Rent form -> Rent complete
#           -> Already rented
