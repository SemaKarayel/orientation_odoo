from odoo import fields, models, api
from datetime import date


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'full_name'

    # fields
    patient_id = fields.Char('Patient ID', required=True, tracking=True)
    first_name = fields.Char('First Name', required=True, tracking=True)
    last_name = fields.Char('Last Name', required=True, tracking=True)
    full_name = fields.Char(string='Full Name', compute='_compute_full_name', store=True, tracking=True)
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    ref = fields.Char(string='Reference')
    age = fields.Integer(string='Age', compute='_compute_age', readonly=True, tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True,
                              default='female')

    active = fields.Boolean('Active', default=True)
    address = fields.Text('Address', tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    national_id_no = fields.Char(string='National ID No', tracking=True)
    image = fields.Image(string='Image')

    # Relations
    tag_ids = fields.Many2many('patient.tag', string='Tags')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointments')


    # Compute full name
    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for rec in self:
            rec.full_name = f"{rec.first_name} {rec.last_name}"

    # Compute age
    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                today = date.today()
                rec.age = today.year - rec.date_of_birth.year - (
                        (today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day)
                )
            else:
                rec.age = 0

    # unique national ID no constraint
    _sql_constraints = [
        ('national_id_no_unique', 'unique(national_id_no)', 'National ID number must be unique.')
    ]

