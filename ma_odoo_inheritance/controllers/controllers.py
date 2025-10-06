# -*- coding: utf-8 -*-
# from odoo import http


# class MaOdooInheritance(http.Controller):
#     @http.route('/ma_odoo_inheritance/ma_odoo_inheritance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ma_odoo_inheritance/ma_odoo_inheritance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ma_odoo_inheritance.listing', {
#             'root': '/ma_odoo_inheritance/ma_odoo_inheritance',
#             'objects': http.request.env['ma_odoo_inheritance.ma_odoo_inheritance'].search([]),
#         })

#     @http.route('/ma_odoo_inheritance/ma_odoo_inheritance/objects/<model("ma_odoo_inheritance.ma_odoo_inheritance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ma_odoo_inheritance.object', {
#             'object': obj
#         })
