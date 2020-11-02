odoo.define('pos_customer_ref_search.phygi_order', function (require) {
"use strict";

var screens = require('point_of_sale.screens');
var PaymentScreenWidget = screens.PaymentScreenWidget;
var models = require('point_of_sale.models');
var rpc = require('web.rpc');

//var pos_models = pos_model.PosModel.prototype.models;

    models.load_models(
        {
            model: 'pos.mlm.orders',
            fields: ['id','customer_id', 'order_number','ref_number','start_date','total_amount',
            'pos_order_id','pos_order_line_id','pos_mlm_line_ids'],
            loaded: function (self, pos_mlm_orders) {
                self.pos_mlm_orders = pos_mlm_orders;
            },
        },


            {
            model: 'pos.mlm.orders.line',
            fields: ['id', 'product_id', 'product_subtotal', 'product_qty', 'pos_mlm_order_id'],
            loaded: function (self, pos_mlm_orders_line) {
                self.pos_mlm_orders_line = pos_mlm_orders_line;
            },
        },
  );



  var _super_PosModel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({


    _save_to_server: function (orders, options) {
            var client = this.get_client();
                    options = options || {};

        var self = this;
        var timeout = typeof options.timeout === 'number' ? options.timeout : 30000 * orders.length;

        // Keep the order ids that are about to be sent to the
        // backend. In between create_from_ui and the success callback
        // new orders may have been added to it.
        var order_ids_to_sync = _.pluck(orders, 'id');

        // we try to send the order. shadow prevents a spinner if it takes too long. (unless we are sending an invoice,
        // then we want to notify the user that we are waiting on something )
        var args = [_.map(orders, function (order) {
                order.to_invoice = options.to_invoice || false;
                return order;
            })];
        args.push(options.draft || false);
            if (client) {

                            return rpc.query({
                    model: 'pos.mlm.orders',
                    method: 'create_phygi_orders',
                    args: args,
//                    kwargs: {},
                }).then(function (server_ids) {
                _.each(order_ids_to_sync, function (order) {
                    self.db.remove_order(order);
                });
                self.set('failed',false);
                return server_ids;
            })
//                .then(function (order) {
//                    console.log(server_ids)
//                })
            }
            return _super_PosModel._save_to_server.call(this, orders, options);
        },


    });






});
