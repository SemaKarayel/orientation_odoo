from odoo import fields, models, api
from datetime import date


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # fields + 'gender', 'active',
    patient_id = fields.Char('Patient ID', required=True, tracking=True)
    first_name = fields.Char('First Name', required=True, tracking=True)
    last_name = fields.Char('Last Name', required=True, tracking=True)
    full_name = fields.Char(string='Full Name', compute='_compute_full_name', store=True, tracking=True)
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', readonly=True, tracking=True)
    gender = fields.Selection([('male','Male'), ('female','Female')], string='Gender', tracking=True)
    address = fields.Text('Address', tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    national_id_no = fields.Char(string='National ID No', tracking=True)
    active = fields.Boolean('Active', default=True)

