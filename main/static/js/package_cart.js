var amount = 0.0;
var final_amount = 0.0;
var amount_package = 0.0;
var amount_order = 0.0;
var discount = Object.create({discount:0, order: false, package: false, amount_limit:0.0}) ;

// set up the total amount for each package
$('tbody').find(".package").each(function(){
  var order = 0.0, storage = 0.0, shipping = 0.0;
  if($(this).parents('tr').find('.order_amount').length>0){
    order = parseFloat($(this).parents('tr').find('.order_amount').text());
  }
  if($(this).parents('tr').find('.storage_fee').length>0){
    storage = parseFloat($(this).parents('tr').find('.storage_fee').text());
  }
  if($(this).parents('tr').find('.shipping_fee').length>0){
    shipping = parseFloat($(this).parents('tr').find('.shipping_fee').text());
  }
  var total = order + storage + shipping;
  $(this).parents('tr').find('.total_amount').text(total.toFixed(2))
  if( !total > 0){
    $(this).parents('tr').find('input[type=checkbox]').prop('disabled',true);
    $(this).parents('tr').find('input[type=checkbox]').prop('title','disabled');
  }
});

// for apply coupon
function apply_coupon(csrf, url){
    if($('#id_code').prop('type')==='hidden'){
      $('#id_code').prop('type','text');
    }else{
            $('.errornote').remove();
            let dt={'csrfmiddlewaretoken': csrf,
                    'coupon':$('#id_code').val()
                  };
            $.ajax({
              type: "POST",
              url: url,
              data: dt,
              success: function(data){
                if(data === ''){
                  var errornote = document.createElement("p");
                  errornote.setAttribute("class", "errornote");
                  errornote.innerHTML = gettext('The coupon does not exist.');
                  $('#coupon_block').before(errornote)
                }else{
                  coup = JSON.parse(data)

                  if (coup==false){
                    var errornote = document.createElement("p");
                    errornote.setAttribute("class", "errornote");
                    errornote.innerHTML = gettext('The coupon is invalid.');
                    $('#coupon_block').before(errornote)
                  }else{
                    discount = coup;
                    if($('#discount_block').length == 0){
                      var disc = '<div id="discount_block">'+
                                dt.coupon +
                                '('+ discount.discount + '% OFF):'+
                                '<span class="w3-right" id="discount_amount"></span></div>'
                      $('#amount_block').before(disc);
                    }
                    update_price(discount);
                    $('#id_code').prop('type','hidden');
                  }
                }
              },
              failure: function(data){

              },
          });

    }
}// end of apply coupon

function update_price(discount){
  if (discount.package){
    var new_package = amount_package *(100-discount.discount)/100;
  }else{
    var new_package = amount_package;
  }
  if (discount.order){
    var new_order = amount_order *(100-discount.discount)/100;
  }else{
    var new_order = amount_order;
  }
  if(discount.amount_limit && discount.amount_limit<(amount - final_amount)){
    final_amount = amount - discount.amount_limit;
  }else{
    final_amount = new_package+new_order;
  }
  $('#id_total_amount').text(final_amount.toFixed(2));
  $('#discount_amount').text("-"+(amount - final_amount).toFixed(2));
}// end of update price

$(document).ready(function(){
      //  for select all checkbox
      $('#select_all_coshipping').change(function(){
        if($(this).prop('checked')){
          $(this).parents('table').find("input[type=checkbox]").each(function(){
            if(!$(this).prop('disabled')){
              $(this).prop('checked', true);
            }
          });
        }else{
          $(this).parents('table').find("input[type=checkbox]").each(function(){
            $(this).prop('checked', false);
          });
        }
      });// end of select_all_coshipping
      $('#select_all_order').change(function(){
        if($(this).prop('checked')){
          $(this).parents('table').find("input[type=checkbox]").each(function(){
            if(!$(this).prop('disabled')){
              $(this).prop('checked', true);
            }
          });
        }else{
          $(this).parents('table').find("input[type=checkbox]").each(function(){
            $(this).prop('checked', false);
          });
        }
      });// end of select all
      $('#select_all_direct_package').change(function(){
        if($(this).prop('checked')){
          $(this).parents('table').find("input[type=checkbox]").each(function(){
            if(!$(this).prop('disabled')){
              $(this).prop('checked', true);
            }
          });
        }else{
          $(this).parents('table').find("input[type=checkbox]").each(function(){
            $(this).prop('checked', false);
          });
        }
      });// end of select all

// change the amount when any checkbox changed
      $('input[type=checkbox]').change(function(){
              amount_package = 0.0;
              amount_order = 0.0;
              $('#selected_list').empty();

              $('tbody').find("input[type=checkbox]").each(function(){
                  if($(this).prop('checked')){
                      var single = 0.0;
                      if($(this).parents('tr').find('.total_amount').length>0){
                        single = parseFloat($(this).parents('tr').find('.total_amount').text());
                      }
                      if($(this).parents('tr').find('.order').length>0){
                        amount_order = amount_order+single;
                      }
                      else{
                        amount_package = amount_package+single;
                      }
                    var selected = '<div class="selected_package w3-row">' +
                                    $(this).parents('tr').find('.cust_tracking_num').text().toUpperCase() +
                                    '<span class="w3-right">' +
                                    single.toFixed(2) +
                                    '</span></div>'
                    $('#selected_list').append(selected);
                  }

              });
              amount = amount_package+amount_order;
              if(discount.discount>0){
                  update_price(discount);
              }else{
                  $('#id_total_amount').text(amount.toFixed(2));
              }

      });//end of checkbox changed

});
