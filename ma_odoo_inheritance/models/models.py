# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class ma_odoo_inheritance(models.Model):
#     _name = 'ma_odoo_inheritance.ma_odoo_inheritance'
#     _description = 'ma_odoo_inheritance.ma_odoo_inheritance'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
