
odoo.define('pos_product_pack.pos_product_pack_file', function(require) {
	"use strict";

	var screens = require('point_of_sale.screens');
    var models = require('point_of_sale.models');
    var PopUpWidget = require('point_of_sale.popups');
    var gui = require('point_of_sale.gui');
    var _t = require('web.core')._t;
    var core = require('web.core');
    var QWeb = core.qweb;
    var utils = require('web.utils');
    var round_di = utils.round_decimals;

	models.load_models([
//	{
//		model: 'product.product',
//		condition: function(self) {
//			return true; },
//		fields: ['id', 'name', 'pack_line_ids','used_in_pack_line_ids','lst_price'],
//		domain: function(self) {
//			return [
//				['pack_ok', '=', true]
//			]; },
//		loaded: function(self, result) {
//
//			self.set({ 'product_pack': result });
//
//
//		},
//	},
//

	 {
		model: 'product.pack.line',
		condition: function(self) {
			return true; },
		fields: ['id', 'parent_product_id', 'quantity', 'offer_price', 'product_id'],
		domain: function(self) {
			return []; },
		loaded: function(self, result) {

			self.set({ 'wk_pack_product': result });


		},


	}], { 'after': 'product.product' });

	screens.ProductListWidget.include({
		wk_is_pack_product: function(product_id) {
			var self = this;
			var pack_product = [];
			var pack_product_list = self.pos.db.get_product_by_id(product_id);
			if (pack_product_list.pack_ok == true) {
                pack_product.push(self.pos.db.get_product_by_id(product_id));

//			var pack_product = self.pos.get('product_pack');
			for (var i = 0; i < pack_product.length; i++) {
				if (pack_product[i].id == product_id) {
					return true;
				}
			}
			}
		},
	});
	screens.ProductScreenWidget.include({
		click_product: function(product) {
           if(product.to_weight && this.pos.config.iface_electronic_scale){
               this.gui.show_screen('scale',{product: product});
           }else{
                self = this;
                var had_pack = "";
                var pack_product = [];
                var packing=[];
			    var pack_product_list = self.pos.db.get_product_by_id(product.id);
			    if (pack_product_list.pack_ok == true) {
                pack_product.push(self.pos.db.get_product_by_id(product.id));

//                var pack_product = self.pos.db.product_by_id;

//                var pack_product = self.pos.get('product_pack');
                var wk_pack_products = self.pos.get('wk_pack_product');

                for (var i = 0; i < pack_product.length; i++) {
                    if (pack_product[i].id == product.id && (pack_product[i].pack_line_ids).length > 0) {
                        for (var j = 0; j < (pack_product[i].pack_line_ids).length; j++) {
                            for (var k = 0; k < wk_pack_products.length; k++) {
                                if (wk_pack_products[k].id == pack_product[i].pack_line_ids[j]) {
                                	packing.push(pack_product[i])
                                    had_pack = 1;
                                    this.pos.get_order().add_product(this.pos.db.product_by_id[wk_pack_products[k].product_id[0]],
                                         {quantity: wk_pack_products[k].quantity,
                                          price: wk_pack_products[k].offer_price,});
                                }
                            }
                        }
                    }
                }
                }
                                if(packing.length > 0) {
                                    let uniqueChars = [];
                packing.forEach((c) => {
                    if (!uniqueChars.includes(c)) {
                        uniqueChars.push(c);
                    }
                });

               for (var k = 0; k < uniqueChars.length; k++) {

                	this.pos.get_order().add_product(this.pos.db.product_by_id[uniqueChars[k].id],
                                         {
                                          price: 0,});
               }

                }
                if (had_pack!=1){
                    this.pos.get_order().add_product(product);
                }
           }
        },
	});

	var _super = models.Orderline;
	models.Orderline = models.Orderline.extend({
		getPackProduct: function(pack_product_id, product_price, product_qty) {
			self = this;
			var pack_product = [];
			var pack_product_list = self.pos.db.get_product_by_id(pack_product_id);
			if (pack_product_list.pack_ok == true) {
                pack_product.push(self.pos.db.get_product_by_id(pack_product_id));
//		    var pack_product = self.pos.db.product_by_id;

//			var pack_product = self.pos.get('product_pack');
//			var pack_product = self.pos.get('product_pack');
			var wk_pack_products = self.pos.get('wk_pack_product');
			var pack_product_list = [];
			var savedprice = 0;
			for (var i = 0; i < pack_product.length; i++) {
				if (pack_product[i].id == pack_product_id && (pack_product[i].pack_line_ids).length > 0) {
					for (var j = 0; j < (pack_product[i].pack_line_ids).length; j++) {
						for (var k = 0; k < wk_pack_products.length; k++) {
							if (wk_pack_products[k].id == pack_product[i].pack_line_ids[j]) {


//							var product_val = { 'display_name': wk_pack_products[k].product_id[1],'price': wk_pack_products[k].offer_price };
//								pack_product_list.push({ 'product': product_val, 'qty': wk_pack_products[k].quantity * parseFloat(product_qty) });
//								savedprice += wk_pack_products[k].offer_price * wk_pack_products[k].quantity * parseFloat(product_qty);

								var product_val = { 'display_name': wk_pack_products[k].name, 'uom_id': wk_pack_products[k].uom_id, 'price': wk_pack_products[k].price };
								pack_product_list.push({ 'product': product_val, 'qty': wk_pack_products[k].product_quantity * parseFloat(product_qty) });
								savedprice += wk_pack_products[k].price * wk_pack_products[k].product_quantity * parseFloat(product_qty);
							}
						}
					}
					return { 'pack_product_list': pack_product_list, 'wk_pack_benefit': savedprice - product_price };
				}
			}
			}

		},
		wk_get_unit: function(unit_id) {
			if (!unit_id) {
				return undefined;
			}
			return unit_id[1];
		},
	});

//	var _super = models.Order;
//	models.Order = models.Order.extend({
//		get_pack_product_benefits: function(orderlines) {
//			var self = this;
//			var savedprice = 0;
//			var wk_quantity_price = 0
//			var pack_products = self.pos.get('product_pack')
//			var wk_pack_products = self.pos.get('wk_pack_product')
//			_.each(orderlines, function(orderline) {
//				_.each(pack_products, function(pack_product) {
//					if (orderline.product.id == pack_product.id) {
//						_.each(pack_product.pack_line_ids, function(pack_product_ids) {
//							for (var k = 0; k < wk_pack_products.length; k++) {
//
//								if (wk_pack_products[k].id == pack_product_ids) {
//									savedprice = savedprice + (wk_pack_products[k].price * wk_pack_products[k].product_quantity * orderline.quantity);
//
//								}
//							}
//
//
//						});
//						wk_quantity_price += orderline.quantity * orderline.product.price
//					}
//
//				});
//
//			});
//			savedprice -= wk_quantity_price;
//			if (savedprice > parseFloat(0))
//				return savedprice;
//			return 0;
//		},
//	});
});
