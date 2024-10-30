from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'

    name = fields.Char(
        string='Name', 
        required=True
    )
    
    @api.constrains('name')
    def _check_name_unique_case_insensitive(self):
        for record in self:
            existing = self.search([('name', '=', record.name)], limit=1)
            if existing and existing.id != record.id:
                raise ValidationError("The name must be unique, ignoring case.")
                
            existing_case_insensitive = self.search([
                ('id', '!=', record.id),
                ('name', 'ilike', record.name)  
            ], limit=1)
            if existing_case_insensitive:
                raise ValidationError("The name must be unique, ignoring case.")