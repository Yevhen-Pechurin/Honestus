{
    'name': 'Custom Product',

    'summary': 'Customization for product.product',

    'description': 'This module add new fields in product',

    'author': 'Yevhen Pechurin',
    'category': 'Sale',
    'version': '0.1',
    'license': 'LGPL-3',
    'depends': [
        'product',
        'sale',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/sale_report_template.xml',
        'report/honestus_sale_report.xml',
    ],
}
