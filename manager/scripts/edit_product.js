(function(context) {

    var choice = (context.title);
    if (choice == 'BulkProduct') {
        $('#id_itemID').closest('p').hide()
        $('#id_retire_date').closest('p').hide()
        $('#id_max_rental_days').closest('p').hide()

        $('#id_reorder_trigger').closest('p').show()
        $('#id_reorder_quantity').closest('p').show()
    }
    else if (choice == 'RentalProduct') {
            $('#id_reorder_trigger').closest('p').hide()
            $('#id_reorder_quantity').closest('p').hide()

            $('#id_itemID').closest('p').show()
            $('#id_retire_date').closest('p').show()
            $('#id_max_rental_days').closest('p').show()
    }
    else if (choice == 'IndividualProduct') {
        $('#id_reorder_trigger').closest('p').hide()
        $('#id_reorder_quantity').closest('p').hide()
        $('#id_retire_date').closest('p').hide()
        $('#id_max_rental_days').closest('p').hide()

        $('#id_itemID').closest('p').show()
    }
    console.log(choice);

    choice.onchange = function(){
        if (choice == 'BulkProduct') {
            $('#id_itemID').closest('p').hide()
            $('#id_retire_date').closest('p').hide()
            $('#id_max_rental_days').closest('p').hide()

            $('#id_reorder_trigger').closest('p').show()
            $('#id_reorder_quantity').closest('p').show()
        }
        else if (choice == 'RentalProduct') {
            $('#id_reorder_trigger').closest('p').hide()
            $('#id_reorder_quantity').closest('p').hide()

            $('#id_itemID').closest('p').show()
            $('#id_retire_date').closest('p').show()
            $('#id_max_rental_days').closest('p').show()
        }
        else if (choice == 'IndividualProduct') {
            $('#id_reorder_trigger').closest('p').hide()
            $('#id_reorder_quantity').closest('p').hide()
            $('#id_retire_date').closest('p').hide()
            $('#id_max_rental_days').closest('p').hide()

            $('#id_itemID').closest('p').show()
        }
        console.log(choice);
    }

})(DMP_CONTEXT.get());

