{
    "name": "Estate Module",  # Name of your module
    "version": "1.0",  # Version of your module
    "license": "LGPL-3",  # License type (e.g., LGPL-3, MIT, etc.)
    "depends": [
        "base",
        "website",
        "web",
        "mail",
        "report_xlsx",
    ],  # List of dependencies (for now, specify the base module)
    "demo": [],
    "description": "Module Estate for lession 2",  # Optional description
    "author": "Minh Nguyen Binh_ Intern BAP",  # Optional author name
    "website": "https://bap.bemo-cloud.com/",  # Optional website
    "category": "Custom",  # Optional category
    "data": [
        # security, data, view, rp, wizard, menu
        # security files
        "security/res_group.xml",
        "security/ir.model.access.csv",
        # data files
        "data/demo.xml",
        # view files
        "views/estate_property_offer_views.xml",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_user_views.xml",
        "views/templates_widget.xml",
        "views/demo_widget_views.xml",
        "views/estate_property_templates.xml",
        "views/feedback_snippet.xml",
        "views/feedback_views.xml",
        "views/homepage_views.xml",
        # wizard
        "wizard/views/confirm_cancel_estate_views.xml",
        "wizard/views/estate_property_report_views.xml",
        # menu
        "views/estate_menu.xml",
    ],
    "qweb": [
        "static/src/xml/qweb_template.xml",
    ],
    # List of data files (XML, CSV, etc.)
    # 'qweb': [
    #     # 'static/src/xml/custom_color_widget_template.xml',
    # ],
    "installable": True,  # Specify if the module is installable
    "application": True,  # Specify if it's an application
    "auto_install": False,
    "test": [],
}
