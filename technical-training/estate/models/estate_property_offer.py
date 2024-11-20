from datetime import timedelta

from odoo import _, models, fields, api
from odoo.exceptions import UserError, ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(
        string="Offer Price"
    )
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
            ("new","New")
        ],
        string="Status",
        default="new",
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner", 
        string="Partner", 
        required=True
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", 
        string="Property Type", 
        store=True
    )
    validity = fields.Integer(
        default=7
    )
    date_deadline = fields.Date(
        compute="_compute_date_deadline", 
        inverse="_inverse_date_deadline", 
        store=True
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = fields.Date.today() + timedelta(
                    days=record.validity
                )

    # @api.onchange("date_deadline")
    # def _inverse_date_deadline(self):
    #     for record in self:
    #         if record.date_deadline:
    #             if record.create_date:
    #                 record.validity = (record.date_deadline - record.create_date).days
    #             else:
    #                 record.validity = 7  
    #         else:
    #             record.validity = 7  

    @api.onchange("date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                if record.create_date:
                    # Chuyển đổi create_date sang date để tính toán chính xác
                    record.validity = (record.date_deadline - record.create_date.date()).days
                else:
                    record.validity = 7  
            else:
                record.validity = 7  
                
    def update(self, vals):
        # Kiểm tra trạng thái
        if 'status' in vals and vals['status'] == 'accepted':
            raise ValidationError(_("Cannot Edit/Delete Offer Accepted"))
        return super(EstatePropertyOffer, self).write(vals)

    def unlink(self):
        for offer in self:
            if offer.status == 'accepted':
                raise ValidationError(_("Cannot Edit/Delete Offer Accepted"))
        return super(EstatePropertyOffer, self).unlink()
    
    # def action_accept(self):
    #     for offer in self:
    #         if offer.status == 'accepted':
    #             raise UserError("This offer has already been accepted.")

    #         # Cập nhật trạng thái offer
    #         offer.status = 'accepted'
            
    #         # Cập nhật tài sản tương ứng
    #         property = offer.property_id
            
    #         # Cập nhật giá bán và người mua cho tài sản
    #         accepted_offers = property.offer_ids.filtered(lambda o: o.status == 'accepted')
    #         property.selling_price = sum(accepted_offers.mapped('price'))
            
    #         # Lấy thông tin người mua từ offer cuối cùng được chấp nhận
    #         last_accepted_offer = accepted_offers[-1] if accepted_offers else False
    #         if last_accepted_offer:
    #             property.buyer_id = last_accepted_offer.partner_id
    
    def action_accept(self):
        if self.status == 'accepted':
            raise UserError("This offer has already been accepted.")

        # Cập nhật trạng thái offer
        self.status = 'accepted'
        
        # Cập nhật tài sản tương ứng
        property = self.property_id
        
        # Cập nhật giá bán và người mua cho tài sản
        accepted_offers = property.offer_ids.filtered(lambda o: o.status == 'accepted')
        property.selling_price = sum(accepted_offers.mapped('price'))
        
        # Lấy thông tin người mua từ offer cuối cùng được chấp nhận
        last_accepted_offer = accepted_offers[-1] if accepted_offers else False
        if last_accepted_offer:
            property.buyer_id = last_accepted_offer.partner_id

                
    def action_refuse(self):
        self.status = 'refused'
        # Cập nhật tài sản tương ứng
        property = self.property_id
        
        # Cập nhật giá bán và người mua cho tài sản
        accepted_offers = property.offer_ids.filtered(lambda o: o.status == 'accepted')
        property.selling_price = sum(accepted_offers.mapped('price'))
        
        # Lấy thông tin người mua từ offer cuối cùng được chấp nhận
        last_accepted_offer = accepted_offers[-1] if accepted_offers else False
        if last_accepted_offer:
            property.buyer_id = last_accepted_offer.partner_id


    _sql_constraints = [
        ('check_offer_price_strictly_positive', 'CHECK(price >= 0)', 'The offer price must be strictly positive.')
    ]
    
    @api.model
    def create(self, vals):
        if vals.get('property_id'):
            property_id = self.env['estate.property'].browse(vals['property_id'])
            
            existing_offer = property_id.offer_ids.filtered(lambda o: o.price > vals.get('price', 0))
            if existing_offer:
                raise UserError("Cannot create an offer lower than an existing offer.")
            
            property_id.state = 'offer_received'

        return super(EstatePropertyOffer, self).create(vals)