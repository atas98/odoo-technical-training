from odoo import api, fields, models


class Book(models.Model):
    _name = 'library.book'
    _description = "Library Book"

    name = fields.Char(index=True)
    author_ids = fields.Many2many('library.partner',
                                  string="Authors",
                                  index=True)
    edition_date = fields.Date()
    isbn = fields.Char(index=True)
    publisher_id = fields.Many2one('library.publisher',
                                   string="Publisher")
    copy_ids = fields.One2many('library.copy', 'book_id')
