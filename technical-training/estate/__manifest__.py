{
    'name': 'Estate Module',  # Name of your module
    'version': '1.0',             # Version of your module
    'license': 'LGPL-3',          # License type (e.g., LGPL-3, MIT, etc.)
    'depends': ['base'],          # List of dependencies (for now, specify the base module)
    'demo': [],
    'description': 'Module Estate for lession 2',  # Optional description
    'author': 'Minh Nguyen Binh_ Intern BAP',        # Optional author name
    'website': 'https://bap.bemo-cloud.com/',  # Optional website
    'category': 'Custom',         # Optional category
    'data':[
            #security files
            'security/res_group.xml',
            'security/ir.model.access.csv',
            
            #view files
            'views/estate_property_offer_views.xml',
            'views/estate_property_views.xml', 
            'views/estate_property_type_views.xml',
            'views/estate_property_tag_views.xml',
            'views/estate_menu.xml',
            
            #data files
            'data/demo.xml' 
            ],                   # List of data files (XML, CSV, etc.)
    'installable': True,          # Specify if the module is installable
    'application': True,         # Specify if it's an application
    'auto_install': False,
    'test': [],
}
