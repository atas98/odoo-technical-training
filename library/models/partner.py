from odoo import api, fields, models
import logging


class Partner(models.Model):
    _inherit = 'res.partner'

    partner_type = fields.Selection(selection=[('customer', 'Customer'),
                                               ('author', 'Author'),
                                               ('publisher', 'Publisher')])
    rental_ids = fields.One2many('library.rental', 'customer_id')
    payment_ids = fields.One2many('library.payment', 'customer_id')

    amount_owned = fields.Float(compute='_compute_amount_owned', store=True)

    @api.depends('payment_ids')
    def _compute_amount_owned(self):
        for r in self:
            r.amount_owned = sum(payment.amount for payment in r.payment_ids)

    @api.model
    def _cron_check_date(self):
        # today = fields.Date.today()
        rental_expired = self.rental_ids.search([])
        # '&', ,
        # ('state', '=', 'rented')
                #  ('return_date', '<', today)
        for rental in rental_expired:
            # Send mail
            context = {
                'partner_name': rental.customer_id.name,
                'partner_email': rental.customer_id.email,
                'book_name': rental.book_id.name,
                'return_date': rental.return_date
            }
            logging.error(rental.customer_id.name)
            # template_id = self.env['ir.model.data'].get_object('library', 'rental_notification_template')
            #     .browse(template_id) \
            #     .send_mail(rental.customer_id.id)
                # .with_context(context) \
