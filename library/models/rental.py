from odoo import api, fields, models


class Rental(models.Model):
    _name = 'library.rental'
    _description = "Library Rental"

    customer_id = fields.Many2one('library.partner',
                                  'rental_ids')
    copy_id = fields.Many2one('library.copy', 'rental_ids')
    rental_date = fields.Date(default=fields.Date.today())
    return_date = fields.Date()
    planned_return_date = fields.Date()

    book_id = fields.Many2one(related='copy_id.book_id', readonly=True)
    customer_address = fields.Text(related='customer_id.address')
    customer_email = fields.Char(related='customer_id.email')
    book_authors = fields.Many2many(related='book_id.author_ids')
    book_edition_date = fields.Date(related='book_id.edition_date')
    book_publisher = fields.Char(related='book_id.publisher_id.name')
