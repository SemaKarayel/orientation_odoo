from odoo import models, fields, api

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'full_name'

    # fields
    code = fields.Char(string='Code', required=True, copy=False, readonly=True, default=lambda self: 'New')
    full_name = fields.Char(string='Full Name', compute='_compute_full_name', store=True, tracking=True)
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    doctor_ids = fields.Many2many('hospital.doctor', string='Doctors')
    patient_id = fields.Many2one('hospital.patient', string='Patient')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')],
        default='draft', string='state', required=True, tracking=True)
    treatment_ids = fields.One2many('hospital.treatment', 'appointment_id', string='Treatments')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')],
        string='Priority')
    gender = fields.Selection(related='patient_id.gender')
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today)
    prescription = fields.Html(string='Prescription')
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy Lines')
    hide_sales_price = fields.Boolean(string='Hide Sales Price')

    # Compute full name from patient
    @api.depends('patient_id.full_name')
    def _compute_full_name(self):
        for rec in self:
            rec.full_name = rec.patient_id.full_name if rec.patient_id else 'Appointment'

    # Auto-generate code
    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or '/'
        return super().create(vals)

    # Test button
    def action_test(self):
        print("Button Clicked !")
        return {
            'effect': {
                'fadeout': 'fast',
                'message': '',
                'type': 'rainbow_man',
            }
        }

    # state change buttons
    def action_in_progress(self):
        for rec in self:
            rec.state = 'in_progress'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        action = self.env.ref("medical_appointment.action_cancel_appointment").read()[0]
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    # Validation: cannot delete done appointments
    def unlink(self):
        for rec in self:
            if rec.state == 'done':
                raise models.UserError("Cannot delete appointments in Done state.")
        return super().unlink()


class AppointmentPharmacyLines(models.Model):
    _name = 'appointment.pharmacy.lines'
    _description = 'Appointment Pharmacy Lines'

    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(related='product_id.list_price')
    qty = fields.Integer(string='Quantity')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')