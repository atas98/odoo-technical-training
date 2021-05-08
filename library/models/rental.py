from odoo import api, fields, models


class Rental(models.Model):
    _name = 'library.rental'
    _description = "Library Rental"

    customer_id = fields.Many2one('res.partner',
                                  'rental_ids',
                                  domain=[('partner_type', '=', 'customer')])
    copy_id = fields.Many2one('library.copy', 'rental_ids')
    rental_date = fields.Date(default=fields.Date.today())
    return_date = fields.Date(default=fields.Date.today())
    planned_return_date = fields.Date(default=fields.Date.today())

    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('rented', 'Rented'),
                                        ('returned', 'Returned'),
                                        ('lost', 'Lost')],
                             default='draft')

    book_id = fields.Many2one(related='copy_id.book_id', readonly=True)
    customer_address = fields.Char(related='customer_id.contact_address')
    customer_email = fields.Char(related='customer_id.email')
    book_name = fields.Char(related='book_id.name')
    book_authors = fields.Many2many(related='book_id.author_ids')
    book_edition_date = fields.Date(related='book_id.edition_date')
    book_publisher = fields.Char(related='book_id.publisher_id.name')

    def add_fee(self, type):
        for r in self:
            # Calculate payment price
            if type == 'time':
                rent_days = float((r.return_date - r.rental_date).days)
                price = self.env.ref('library.price_rent').price
                duration = self.env.ref('library.price_rent').duration
                price_sum = rent_days*price/duration
            elif type == 'loss':
                price_sum = self.env.ref('library.price_loss').price
            else:
                return
            # Create payment
            self.env['library.payment'].create({
                'date': r.rental_date,
                'amount': price_sum,
                'customer_id': r.customer_id.id
            })
            self.env.cr.commit()

    def action_confirm(self):
        for r in self:
            r.state = 'rented'
            r.copy_id.book_state = 'rented'
            r.add_fee('time')

    def action_return(self):
        for r in self:
            r.state = 'returned'
            r.copy_id.book_state = 'available'

    def action_lost(self):
        for r in self:
            r.state = 'lost'
            r.copy_id.book_state = 'lost'
            r.copy_id.active = False
            r.add_fee('loss')
