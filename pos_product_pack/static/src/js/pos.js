    var posmodel_super = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        load_server_data: function(){
                var self = this;

                self.models.forEach(function(elem) {
                  if(elem.model == 'product.product'){
                       elem.fields = ['id', 'name', 'pack_line_ids','used_in_pack_line_ids','lst_price']
                        elem.domain = ['pack_ok', '=', true]
//                        elem.loaded = function(self, result) {
//
//			self.set({ 'product_pack': result });
//
//
//		},
                    }
                }),

                var loaded = posmodel_super.load_server_data.apply(this, arguments);
                return loaded;
            },
            });


