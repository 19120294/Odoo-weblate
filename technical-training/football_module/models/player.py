from odoo import models, fields


class football_module(models.Model):
    _name = "player"
    _description = "Player"

    name = fields.Char(string="Name", required=True)
    image = fields.Image(string="Image", attachment=True)
    country = fields.Char(string="Country")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")], string="Gender", default="male"
    )
    day_of_birth = fields.Datetime(string="Day of birth")
    position = fields.Selection(
        [("fw", "Foward"), ("mid", "Middle"), ("def", "Defender"), ("gk", "GK")],
        string="Position",
    )
    height = fields.Float(string="Height (cm)")
    weight = fields.Float(string="Weight (kg)")
    
