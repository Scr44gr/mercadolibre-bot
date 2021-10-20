# mercadolibre items info response
#       {
#              "code": 200,
#              "body": {
#                  "id": "MLA594239600",
#                  "site_id": "MLA",
#                  "title": "Item De Test - Por Favor No Ofertar",
#                  "subtitle": null,
#                  "seller_id": 303888594,
#                  "category_id": "MLA401685",
#                  "official_store_id": null,
#                  "price": 120,
#                  "base_price": 120,
#                  "original_price": null,
#                  "currency_id": "",
#                  "initial_quantity": 1,
#                  "available_quantity": 1,
#                  "sold_quantity": 0,
#                  "sale_terms": [],
#                  [...
#                  ] "automatic_relist": false,
#                  "date_created": "2018-02-26T18:15:05.000Z",
#                  "last_updated": "2018-03-29T04:14:39.000Z",
#                  "health": null
#              }
#          }
#       ]
#
#


params_format = {
    
    'price': 'price',
    'average_price': 'base_price',
    'state': 'status',
    'sales': 'sold_quantity',
    'sales_in_cash': 'sold_quantity',
    'free_shipping': lambda d: d['shipping']['free_shipping'],
    'stock': 'available_quantity',
}


DATE_TO = {
    '01': 'Enero',
    '02': 'Febrero',
    '03': 'Marzo',
    '04': 'Abril',
    '05': 'Mayo',
    '06': 'Junio',
    '07': 'Julio',
    '08': 'Agosto',
    '09': 'Septiembre',
    '10': 'Octubre',
    '11': 'Noviembre',
    '12': 'Diciembre'
}