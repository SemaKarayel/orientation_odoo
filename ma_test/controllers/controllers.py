# -*- coding: utf-8 -*-
# from odoo import http


# class MaTest(http.Controller):
#     @http.route('/ma_test/ma_test', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ma_test/ma_test/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ma_test.listing', {
#             'root': '/ma_test/ma_test',
#             'objects': http.request.env['ma_test.ma_test'].search([]),
#         })

#     @http.route('/ma_test/ma_test/objects/<model("ma_test.ma_test"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ma_test.object', {
#             'object': obj
#         })
