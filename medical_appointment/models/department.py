from odoo import models, fields, api

class Department(models.Model):
    _name = 'hospital.department'
    _description = 'Hospital Department'
    _rec_name = 'code'

    # fields
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)


    # Code constraint
    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Code must be unique.')
    ]

