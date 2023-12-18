from odoo import models, fields, api
from odoo.odoo.exceptions import ValidationError

ADD = 4


def calculate_total_from_ei_array(expense_income_items):
    total = 0
    for item in expense_income_items:
        if item.operation in ['purchase_cost', 'promotion', 'logistics_cost', 'agency_commission']:
            total -= item.operation_costs
        elif item.operation == 'sale':
            total += item.operation_costs
    return total


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
    total = fields.Integer(string='Total')
    profit = fields.Integer(string='Profit')
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
            self._compute_total(record)

            if record.state == 'purchase':
                marked_products = []

                for i in range(record.count):
                    product = self.env['product_labeling.marked_product'].create({
                        'last_destination': record.new_destination,
                        'state': record.state,
                        'product': record.product.id
                    })

                    marked_products.append(product)

                self._add_expenses_incomes_to_marked_products(record, marked_products)
            elif record.state in ['internal_movement', 'sale']:
                marked_products = self.env['product_labeling.marked_product'].search([
                    ('product', '=', record.product.id),
                    ('last_destination', '=', record.last_destination)
                ], limit=record.count)

                self._add_expenses_incomes_to_marked_products(record, marked_products)

                if len(marked_products) != record.count:
                    raise ValidationError('Not enough')

                for product in marked_products:
                    product.write({
                        'last_destination': record.new_destination,
                        'state': record.state,
                    })

                if record.state == 'sale':
                    self._compute_profit_when_sale(record, marked_products)

    def _compute_total(self, record):
        expense_income_items = self.env['product_labeling.expense_income'].search([
            ('act_id', '=', record.id)
        ])

        record.total = calculate_total_from_ei_array(expense_income_items)

    def _add_expenses_incomes_to_marked_products(self, record, marked_products):
        expense_income_items = self.env['product_labeling.expense_income'].search([
            ('act_id', '=', record.id)
        ])

        ei_to_add = []

        for ei_item in expense_income_items:
            ei_to_add.append((ADD, ei_item.id))

        for mp_item in marked_products:
            mp_item.expense_incomes = ei_to_add

    def _compute_profit_when_sale(self, record, marked_products):
        act_profit = 0
        for product in marked_products:
            expense_income_items = self.env['product_labeling.expense_income'].search([
                ('marked_products', 'in', [product.id])
            ])

            total = calculate_total_from_ei_array(expense_income_items)
            act_profit += total
            product.final_profit = total
        record.profit = act_profit
