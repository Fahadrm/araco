odoo.define('pos_customer_ref_search.get_customer', function(require){
"use strict";


    var models = require('point_of_sale.models');

    var POSDB = require('point_of_sale.DB');


    models.load_fields('res.partner','ref');


//var _super_Db = models.PosDB.prototype;
POSDB.include(


        {
    _partner_search_string: function(partner){
        if (partner.ref){
        var str =  partner.name || '';
        if(partner.barcode){
            str += '|' + partner.barcode;
        }
        if(partner.address){
            str += '|' + partner.address;
        }
        if(partner.phone){
            str += '|' + partner.phone.split(' ').join('');
        }
        if(partner.mobile){
            str += '|' + partner.mobile.split(' ').join('');
        }
        if(partner.email){
            str += '|' + partner.email;
        }
        if(partner.vat){
            str += '|' + partner.vat;
        }

        var ref = partner.ref.toString();
            str += '|' + ref.concat(partner.name)
        str = '' + partner.id + ':' + str.replace(':','') + '\n';
        return str;
        }

        return this._super.apply(this,arguments);
    },
}


);










});
