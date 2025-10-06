from odoo import models, fields, api

class CreateAppointmentWizard(models.TransientModel):
    _name = 'create.appointment.wizard'
    _description = 'Create Appointment Wizard'

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_ids = fields.Many2many('hospital.doctor', string='Doctors')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')

    def action_create_appointment(self):
        self.ensure_one()
        vals = {
            'patient_id': self.patient_id.id,
            'doctor_ids': [(6,0,self.doctor_ids.ids)],
            # appointment_time, code will be defaulted
        }
        appt = self.env['hospital.appointment'].create(vals)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'res_id': appt.id,
            'view_mode': 'form',
            'target': 'current',
        }