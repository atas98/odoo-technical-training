# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Wizard(models.TransientModel):
    _name = "library.wizard"
    _description = "Wizard: Quick rental creation"

    def _default_copies(self):
        return self.env['library.copy'].browse(self._context.get('active_ids'))

    customer_id = fields.Many2one('res.partner', required=True,
                                  string='Customer')
    return_date = fields.Date()
    copy_ids = fields.Many2many('library.copy', default=_default_copies,
                                string='Copies')
    rental_ids = fields.Many2many('library.rental', string='rentals')

    def action_continue(self):
        # Create rental for each selected copy
        created_ids = []
        for copy in self.copy_ids:
            created_ids.append(self.env['library.rental'].create({
                'customer_id': self.customer_id.id,
                'copy_id': copy.id,
                'rental_date': fields.Date.today(),
                'return_date': self.return_date,
                'planned_return_date': self.return_date,
                'state': 'draft'
            }).id)
        self.env.cr.commit()

        # Redirect to rental view
        return {
            'name': 'Rental',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'res_model': 'library.rental',
            'type': 'ir.actions.act_window',
            'target': 'main',
            'domain': [('id', 'in', created_ids)]
        }
