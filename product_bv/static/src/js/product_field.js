odoo.define('product_bv.product_field', function(require){
"use strict";


    var models = require('point_of_sale.models');

    models.load_fields('product.product', [
        'bv_value'
    ]);

});
