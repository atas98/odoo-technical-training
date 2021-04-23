from odoo import api, fields, models


class Rental(models.Model):
    _name = 'library.rental'
    _description = "Library Rental"

    customer_id = fields.Many2one('library.partner', 'rental_ids')
    book_id = fields.Many2one('library.book', 'rental_ids')
    rental_date = fields.Date()
    return_date = fields.Date()
