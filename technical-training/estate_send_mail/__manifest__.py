{
    'name': 'Estate Send Mail',
    'version': '1.0',
    'category': 'Estate',
    'author': 'Minh Nguyen Binh_Intern BAP',
    'depends': ['estate', 
                'mail',
                'base'],
    'data': [
        'views/estate_property_views.xml',
        'data/email_templates.xml',
        # 'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
