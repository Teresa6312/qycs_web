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

// for apply rewards
function apply_reward(reward){
  if($('#id_reward_point_used').prop('type')==='hidden'){
    $('#id_reward_point_used').prop('type','number');
    $('#id_reward_point_used').prop('title','You have '+ reward +' point(s).');
  }else{
    if(0<$('#id_reward_point_used').val()<= reward &&  $('#id_reward_point_used').val()/100 < amount && discount===0){
      amount = amount + reward_used/100;
      reward_used = $('#id_reward_point_used').val();
      amount = amount - reward_used/100;
      $('#id_total_amount').text(amount.toFixed(2));
      if($('#reward_used_block').length>0){
        $('#reward_used_block').remove();
      }
      var rew = '<div id="reward_used_block">' + reward_used +
                ' points:<span class="w3-right" id="reward_discount_amount">-'+
                (reward_used/100).toFixed(2) +
                '</span></div>'
      $('#amount_block').before(rew);
      $('#id_reward_point_used').prop('type','hidden');
      $('#id_coupon').val('');
    }else if(discount>0){
      var errornote = '<p class="errornote">Coupon and Reward ponits can bed used only one.</p>'
      $('#reward_block').before(errornote);
    }
  }
}// endof apply rewards
// for apply coupon
function apply_coupon(csrf, url){
    if($('#id_coupon').prop('type')==='hidden'){
      $('#id_coupon').prop('type','text');
    }else{
      if(reward_used===0){
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
                  var errornote = '<p class="errornote">The coupon is not exicted.</p>'
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
        }else {
          var errornote = '<p class="errornote">Coupon and Reward ponits can bed used only one.</p>'
          $('#coupon_block').before(errornote);
        }
    }
}// end of apply coupon

$(document).ready(function(){
  //  for select all checkbox
      $('#select_all').change(function(){
        if($(this).prop('checked')){
          $('tbody').find("input[type=checkbox]").each(function(){
            if(!$(this).prop('disabled')){
              $(this).prop('checked', true);
            }
          });
        }else{
          $('tbody').find("input[type=checkbox]").each(function(){
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
