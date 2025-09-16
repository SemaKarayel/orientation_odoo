from odoo import api, fields, models

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"

    # fields
    patient_id = fields.Char('Patient ID', required=True)
    first_name = fields.Char('First Name', required=True)
    last_name = fields.Char('Last Name', required=True)
    full_name = fields.Char(string='Full Name', compute='_compute_full_name', store=True)
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', readonly=True)
    address = fields.Text('Address')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    national_id_no = fields.Char(string='National ID No')

