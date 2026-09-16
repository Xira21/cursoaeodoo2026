{
    "name": "Real State Natalia",
    "version": "1.0",
    "summary": "Real estate management module",
    "description": "This module allows you to manage real estate properties, including listings, sales, and rentals.",
    "author": "Natalia",
    "category": "Real Estate",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/realestate_property_views.xml",
        "views/realestate_menuitems.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "application": True,
}