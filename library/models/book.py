from odoo import api, fields, models


class Book(models.Model):
    _name = 'library.book'
    _description = "Library Book"

    name = fields.Char()
    author_ids = fields.Many2many('library.partner')
    edition_date = fields.Date()
    isbn = fields.Char()
    publisher_id = fields.Many2one('library.publisher')
    rental_ids = fields.One2many('library.rental', 'book_id')
