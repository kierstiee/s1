$(function() hide_product(choice){
    if (choice == 'BulkProduct') {
        $('#id_itemID').hide();
        $('#id_retire_date').hide();
        $('#id_max_rental_days').hide();

        $('#id_reorder_trigger').show();
        $('#id_reorder_quantity').show();
    }
    else if (choice == 'RentalProduct') {
        $('#id_reorder_trigger').hide();
        $('#id_reorder_quantity').hide();

        $('#id_itemID').show();
        $('#id_retire_date').show();
        $('#id_max_rental_days').show();
    }
    else if (choice == 'IndividualProduct') {
        $('#id_reorder_trigger').hide();
        $('#id_reorder_quantity').hide();
        $('#id_retire_date').hide();
        $('#id_max_rental_days').hide();

        $('#id_itemID').show();
    }


})

$(function() {

    var choice = $('#id_type')
    hide_product(choice)
    console.log(choice)

    choice.on('change', function(){
        hide_product(choice)

})
