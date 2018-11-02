var amount = 0.0;
var discount = 0;
var reward_used = 0;
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
    if($('#id_coupon').prop('type')==='hidden'){
      $('#id_coupon').prop('type','text');
    }else{
            $('.errornote').remove();
            let dt={'csrfmiddlewaretoken': csrf,
                    'coupon':$('#id_coupon').val()
                  };
            $.ajax({
              type: "POST",
              url: url,
              data: dt,
              success: function(data){
                console.log(data);
                if(data === ''){
                  var errornote = document.createElement("p");
                  errornote.setAttribute("class", "errornote");
                  errornote.innerHTML = gettext('The coupon does not exist.');
                  $('#coupon_block').before(errornote)
                }else{
                  discount = parseFloat(data);
                  amount = amount *(100-discount)/100;
                  $('#id_total_amount').text(amount.toFixed(2));
                  var disc = '<div id="discount_block">'+
                            dt.coupon +
                            '('+ discount + '% OFF):'+
                            '<span class="w3-right" id="discount_amount">-'+
                            (amount *discount/100).toFixed(2) +
                            '</span></div>'
                  $('#amount_block').before(disc);
                  $('#id_coupon').prop('type','hidden');
                  $('#id_reward_point_used').val(0);
                }
              },
              failure: function(data){
                console.log(failure);
              },
          });

    }
}// end of apply coupon

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

// change the amount when any checkbox chenged
      $('input[type=checkbox]').change(function(){
        amount = 0.0;
        $('#selected_list').empty();
        $('tbody').find("input[type=checkbox]").each(function(){
            if($(this).prop('checked')){
                var single = 0.0;
                if($(this).parents('tr').find('.total_amount').length>0){
                  single = parseFloat($(this).parents('tr').find('.total_amount').text());
                }
              amount = amount + single;
              var selected = '<div class="selected_package">' +
                              $(this).parents('tr').find('.cust_tracking_num').text().toUpperCase() +
                              '<span class="w3-right">' +
                              single.toFixed(2) +
                              '</span></div>'
              $('#selected_list').append(selected);
            }

        });

        if(amount *(100-discount)/100>reward_used/100){
          amount = amount *(100-discount)/100 - reward_used/100;
        }else{
          reward_used = 0;
          amount = amount *(100-discount)/100;
          $('#reward_used_block').remove();
          $('#id_reward_point_used').val(0);
        }
        $('#discount_amount').text((amount *discount/100).toFixed(2));
        $('#reward_used_amount').text((reward_used/100).toFixed(2));
        $('#id_total_amount').text(amount.toFixed(2));
      });//end of checkbox changed
});
