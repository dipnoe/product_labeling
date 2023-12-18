from odoo import models, fields, api


class ProductPropertyChangeAct(models.Model):
    _name = 'product_labeling.act'
    _description = 'Act of Changing Product Properties'

    name = fields.Char('Название акта')
    last_destination = fields.Text(string='Last destination')
    new_destination = fields.Text(string='New destination', required=True)
    state = fields.Selection([
        ('sale', 'Sale'),
        ('purchase', 'Purchase'),
        ('internal_movement', 'Internal movement')],
        string='Assigned status', required=True)
    product = fields.Many2one('product_labeling.product', required=True)
    count = fields.Integer(string='Count', required=True)
    expense_income_ids = fields.One2many('product_labeling.expense_income', 'act_id', string="Expenses/Incomes")
    is_applied = fields.Boolean(default=False, string='Is applied?')

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

    def apply_act(self):
        for record in self:
            record.is_applied = True
            if record.state == 'purchase':
                for i in range(record.count):
                    self.env['product_labeling.marked_product'].create({
                        'last_destination': record.new_destination,
                        'state': record.state,
                        'product': record.product.id
                    })
            elif record.state in ['internal_movement', 'sale']:
                marked_products = self.env['product_labeling.marked_product'].search([
                    ('product', '=', record.product.id)
                ])
                for product in marked_products:
                    product.write({
                        'last_destination': record.new_destination,
                        'state': record.state
                    })
