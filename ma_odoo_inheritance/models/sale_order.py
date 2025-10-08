from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmed_user_id = fields.Many2one('res.partner', string='Confirmed User')

