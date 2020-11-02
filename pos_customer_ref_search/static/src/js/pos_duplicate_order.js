odoo.define('pos_customer_ref_search.pos_duplicate_order', function(require){
"use strict";
    var models = require('point_of_sale.models');
    var POSDB = require('point_of_sale.DB');
//    models.load_fields('pos.order',['update_status','order_type','ref_number']);
       models.load_fields('pos.order.line','ecommerce_id');



//    var models = require('point_of_sale.models');
//    var _super_posmodel = models.PosModel.prototype;
//    models.PosModel = models.PosModel.extend({
//        initialize: function (session, attributes) {
//            var partner_model = _.find(this.models, function(model){ return model.model === 'pos.order'; });
//            partner_model.fields.push('update_status','order_type','ref_number');
//
//            var res_partner_model = _.find(this.models, function(model){ return model.model === 'pos.order.line'; });
//            res_partner_model.fields.push('ecommerce_id');
//
//            return _super_posmodel.initialize.call(this, session, attributes);
//        },
//    });




});
