from odoo import api, fields, models


class Copy(models.Model):
    _name = 'library.copy'
    _description = 'Library Book Copy'
    _inherits = {'library.book': "book_id"}

    book_id = fields.Many2one('library.book',
                              'copy_ids',
                              required=True,
                              ondelete='cascade')
    reference = fields.Char()
    rental_ids = fields.One2many('library.rental', 'copy_id')

    # Book information
    name = fields.Char(related='book_id.name', index=True, readonly=True)
    author_ids = fields.Many2many(related='book_id.author_ids',
                                  index=True, readonly=True)
    edition_date = fields.Date(related='book_id.edition_date', readonly=True)
    isbn = fields.Char(related='book_id.isbn', index=True, readonly=True)
    publisher_id = fields.Many2one(related='book_id.publisher_id',
                                   string="Publisher", readonly=True)
