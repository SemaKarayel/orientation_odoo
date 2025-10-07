from odoo import models, fields

class Treatment(models.Model):
    _name = 'hospital.treatment'
    _description = 'Treatment'

    name = fields.Char('Name', required=True)
    is_done = fields.Boolean('Is Done', default=False)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    patient_id = fields.Many2one('hospital.patient', string='Patient')