from odoo import api, fields, models


class Book(models.Model):
    _inherit = 'product.product'

    _sql_constraints = [
        ('isbn_unique', 'unique(isbn)', 'ISBN already exists!')
    ]

    is_book = fields.Boolean()
    author_ids = fields.Many2many('res.partner',
                                  string="Authors",
                                  index=True)
    edition_date = fields.Date()
    isbn = fields.Char(index=True)
    publisher_id = fields.Many2one('res.partner',
                                   string="Publisher")
    copy_ids = fields.One2many('library.copy', 'book_id')
