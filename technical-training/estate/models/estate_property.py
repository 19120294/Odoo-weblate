from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Post Code")
    date_availability = fields.Date(
        string="Date Availability",
        copy=False,
        default=lambda self: fields.Date.today() + timedelta(days=90),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("west", "West"),
            ("east", "East"),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="State",
        required=True,
        copy=False,
        default="new",
    )
    reason_cancel = fields.Text(string="Reason for Cancellation")

    @api.depends('offer_ids.status')
    def _compute_state(self):
        for record in self:
            if record.offer_ids:
                if all(offer.status in ('accepted', 'refused') for offer in record.offer_ids):
                    record.state = 'offer_accepted'
                

    total_area = fields.Float(compute='_compute_total_area', string='Total Area', store=True)
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area
         
    best_price = fields.Float(compute='_compute_best_price', string='Best Offer Price', store=True)
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price'), default=0)        
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 100  
            self.garden_orientation = 'north' 
        else:
            self.garden_area = 0
            self.garden_orientation = False


    # soft warning
    
    # @api.constrains('date_availability')
    # def _check_date_availability(self):
    #     for record in self:
    #         if record.date_availability and record.date_availability < fields.Date.today():
    #             warning_msg = {
    #                 'title': 'Warning!',
    #                 'message': 'The availability date cannot be in the past.',
    #             }
    #             # Raise a soft warning
    #             return {
    #                 'warning': warning_msg
    #             }
    
    # prevent
    @api.constrains('date_availability')
    def _check_date_availability(self):
        for record in self:
            if record.date_availability and record.date_availability < fields.Date.today():
                raise ValidationError('The availability date cannot be in the past.')
            
        
    code = fields.Char(string='Code', readonly=True, copy=False)
    @api.model
    def create(self, vals):
        if 'code' not in vals or vals['code'] == '':
            sequence = self.env['ir.sequence'].next_by_code('estate.property.code') or 'EPT00001'
            vals['code'] = sequence
        return super(EstateProperty, self).create(vals)
    
    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Cannot mark as sold, the property is cancelled.")
            record.state = 'sold'

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Cannot cancel a sold property.")
            # record.state = 'canceled'
            return {
                'name': 'Confirm Cancellation',
                'type': 'ir.actions.act_window',
                'res_model': 'confirm.cancel.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {'default_property_id': record.id}
            }
            
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price > 0 and record.selling_price < 0.9 * record.expected_price:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")            

    def action_create_offer(self):
        if self.state != "new":
            raise UserError("You can create offer")
        self.state = 'offer_received'

    _sql_constraints = [
        ('check_expected_price_strictly_positive', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'The selling price must be positive.'),
    ]
    
    # Thêm trường đếm
    count_offer_accepted = fields.Integer(string='Count Offer Accepted', compute='_compute_count_offer_accepted', store=True)

    @api.depends('offer_ids')
    def _compute_count_offer_accepted(self):
        for record in self:
            record.count_offer_accepted = len(record.offer_ids.filtered(lambda offer: offer.status == 'accepted'))
            
    def action_view_accepted_offers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Accepted Offers',
            'view_mode': 'tree,form',
            'res_model': 'estate.property.offer',
            "domain": [("property_id","=",self.id),("status","=","accepted")],
            'context': {'create': False},
        }
        
