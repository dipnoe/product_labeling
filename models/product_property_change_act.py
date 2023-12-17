from odoo import models, fields, api


class ProductPropertyChangeAct(models.Model):
    _name = 'product_labeling.act'
    _description = 'Act of Changing Product Properties'

    name = fields.Char('Название акта', required=True)
    last_destination = fields.Text(string='Last destination', required=True)
    new_destination = fields.Text(string='New destination', required=True)
    status = fields.Selection([
        ('sale', 'Sale'),
        ('purchase', 'Purchase'),
        ('internal_movement', 'Internal movement')],
        string='Assigned status', required=True)
    product = fields.Many2one('product_labeling.product', required=True)
    count = fields.Integer(string='Count', required=True)
    expense_income_ids = fields.One2many('product_labeling.expense_income', 'act_id', string="Expenses/Incomes")

    @api.model
    def create(self, vals):
        record = super(ProductPropertyChangeAct, self).create(vals)
        record.name = f"Акт изменения свойств товаров #{record.id}"
        return record

    def write(self, vals):
        if 'name' not in vals or not vals['name']:
            vals['name'] = f"Акт изменения свойств товаров #{self.id}"
        return super(ProductPropertyChangeAct, self).write(vals)

    def confirm_create(self):
        return True

