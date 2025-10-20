from odoo import models, fields, api
from odoo.exceptions import UserError

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'full_name'

    # Fields
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
        default='draft', string='State', required=True, tracking=True)
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

    # NEW fields
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    pending_amount = fields.Float(string='Pending Amount', compute='_compute_pending_amount', store=True)
    sale_order_line = fields.One2many('sale.order.line', 'appointment_id', string='Sale Order Line')
    # Smart buttons -> count
    sale_orders_count = fields.Integer(string='Sale Orders', compute='_compute_sale_orders_count')
    invoices_count = fields.Integer(string='Invoices', compute='_compute_invoices_count')
    payments_count = fields.Integer(string='Payments', compute='_compute_payments_count')

    # Compute method -> amounts
    @api.depends('sale_order_line.price_subtotal')
    def _compute_total_amount(self):
        for appointment in self:
            total = sum(appointment.sale_order_line.mapped('price_subtotal'))
            appointment.total_amount = total

    @api.depends('total_amount')
    def _compute_pending_amount(self):
        for appointment in self:
            payments = self.env['account.payment'].search([('appointment_id', '=', appointment.id)])
            paid = sum(payments.mapped('amount'))
            appointment.pending_amount = appointment.total_amount - paid

    # Compute methods -> buttons
    @api.depends('sale_order_line')
    def _compute_sale_orders_count(self):
        for rec in self:
            rec.sale_orders_count = self.env['sale.order'].search_count([
                ('appointment_id', '=', rec.id)
            ])

    @api.depends()
    def _compute_invoices_count(self):
        for rec in self:
            rec.invoices_count = self.env['account.move'].search_count([
                ('appointment_id', '=', rec.id),
                ('move_type', '=', 'out_invoice')
            ])

    @api.depends()
    def _compute_payments_count(self):
        for rec in self:
            rec.payments_count = self.env['account.payment'].search_count([
                ('appointment_id', '=', rec.id)
            ])

    # Action -> Smart Buttons
    def action_open_sale_orders(self):
        self.ensure_one() # more than one -> error
        return {
            'type': 'ir.actions.act_window', # open a window
            'name': 'Sale Orders',
            'res_model': 'sale.order', # source
            'view_mode': 'tree,form',
            'domain': [('appointment_id', '=', self.id)], # domain: filter
            'context': {'default_appointment_id': self.id}, # if create new fill appointment_id
        }

    def action_open_invoices(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('appointment_id', '=', self.id), ('move_type', '=', 'out_invoice')],
            'context': {'default_appointment_id': self.id},
        }

    def action_open_payments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payments',
            'res_model': 'account.payment',
            'view_mode': 'tree,form',
            'domain': [('appointment_id', '=', self.id)],
            'context': {'default_appointment_id': self.id},
        }

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

    # State change buttons
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
                raise UserError("Cannot delete appointments in Done state.")
        return super().unlink()


class AppointmentPharmacyLines(models.Model):
    _name = 'appointment.pharmacy.lines'
    _description = 'Appointment Pharmacy Lines'

    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(related='product_id.list_price', store=True)
    qty = fields.Integer(string='Quantity')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')


# Inherit sale/order/invoice/payment
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')

class AccountMove(models.Model):
    _inherit = 'account.move'
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')