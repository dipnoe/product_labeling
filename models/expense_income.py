from odoo import models, fields, api


class ExpenseIncome(models.Model):
    _name = 'product_labeling.expense_income'
    _description = 'Expense/Income'

    act_id = fields.Many2one('product_labeling.act', string='Act')
    promotion = fields.Integer('Product promotion, rubles')
    logistics_cost = fields.Integer('Logistics, rubles')
    purchase_cost = fields.Integer('Purchase cost, rubles')
    agency_commission = fields.Integer('Agency commission, rubles')
    sale = fields.Integer('Sale, rubles')
    sum = fields.Integer(string='Sum, rubles', compute='_compute_sum')

    def confirm_create(self):
        return True

    def _compute_sum(self):
        for record in self:
            total_sum = 0
            total_sum -= record.promotion or 0
            total_sum -= record.logistics_cost or 0
            total_sum -= record.purchase_cost or 0
            total_sum -= record.agency_commission or 0
            total_sum += record.sale or 0
            # Assign the total to the 'sum' field
            record.sum = total_sum

    # @api.model
    # def create(self, vals):
    #     record = super(ExpenseIncome, self).create(vals)
    #     record.act_id = record.act_id
    #     return record
