from odoo import api, fields, models


class Rental(models.Model):
    _name = 'library.rental'
    _description = "Library Rental"

    customer_id = fields.Many2one('library.partner', 'rental_ids')
    book_id = fields.Many2one('library.book', 'rental_ids')
    rental_date = fields.Date()
    return_date = fields.Date()

    customer_address = fields.Text(related='customer_id.address', stored=True)
    customer_email = fields.Char(related='customer_id.email', stored=True)
    book_authors = fields.Many2many(related='book_id.author_ids', stored=True)
    book_edition_date = fields.Date(related='book_id.edition_date',
                                    stored=True)
    book_publisher = fields.Char(related='book_id.publisher_id.name',
                                 stored=True)
