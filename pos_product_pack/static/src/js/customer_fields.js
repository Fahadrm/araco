odoo.define('pos_product_pack.pos_product_fields', function(require){
"use strict";

    var PosModels = require('point_of_sale.models');
    var PosModel = PosModels.PosModel;
    var models = require('point_of_sale.models');


    PosModels.load_fields('product.product', [
        'pack_line_ids','used_in_pack_line_ids','pack_ok'
    ]);


//    var _super_Order = models.Order.prototype;
//	models.Order = models.Order.extend({
//		add_product: function(product, options){
//        	var self = this;
//        	if(product.pack_ok && product.pack_line_ids.length > 0){
//
//            	_super_Order.add_product.call(self, product, options);
//
//        	}
//        	else{
//            	_super_Order.add_product.call(self, product, options);
//        	}
//		},
//	});


});
