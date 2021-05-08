from odoo import api, fields, models


class Copy(models.Model):
    _name = 'library.copy'
    _description = 'Library Book Copy'
    _inherits = {'product.product': "book_id"}

    book_id = fields.Many2one('product.product',
                              'copy_ids',
                              required=True,
                              ondelete='cascade',
                              domain=[('is_book', '=', True)])
    reference = fields.Char()
    rental_ids = fields.One2many('library.rental', 'copy_id')
    book_state = fields.Selection(selection=[('available', 'Available'),
                                             ('rented', 'Rented'),
                                             ('lost', 'Lost')],
                                  default='available')
    readers_count = fields.Integer(compute='_compute_readers_count',
                                   store=True)

    # Book information available, rented, lost
    name = fields.Char(related='book_id.name', index=True,
                       readonly=True, store=True)
    author_ids = fields.Many2many(related='book_id.author_ids',
                                  index=True, readonly=True)
    edition_date = fields.Date(related='book_id.edition_date', readonly=True)
    isbn = fields.Char(related='book_id.isbn', index=True,
                       readonly=True, store=True)
    publisher_id = fields.Many2one(related='book_id.publisher_id',
                                   string="Publisher", readonly=True)

    @api.depends('rental_ids')
    def _compute_readers_count(self):
        for r in self:
            r.readers_count = len(r.rental_ids.ids)

    def open_readers(self):
        return {
            'name': 'Readers',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'res_model': 'res.partner',
            'type': 'ir.actions.act_window',
            'target': 'main',
            'domain': [('id', 'in', self.rental_ids.customer_id.ids)]
        }
