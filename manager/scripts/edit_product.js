$(function() {

    var choice = $("#id_type")
    if (choice.val() == 'BulkProduct') {
        $('#id_itemID').closest('p').hide()
        $('#id_retire_date').closest('p').hide()
        $('#id_max_rental_days').closest('p').hide()

        $('#id_reorder_trigger').closest('p').show()
        $('#id_reorder_quantity').closest('p').show()
    }
    else if (choice.val() == 'RentalProduct') {
            $('#id_reorder_trigger').closest('p').hide()
            $('#id_reorder_quantity').closest('p').hide()

            $('#id_itemID').closest('p').show()
            $('#id_retire_date').closest('p').show()
            $('#id_max_rental_days').closest('p').show()
    }
    else if (choice.val() == 'IndividualProduct') {
        $('#id_reorder_trigger').closest('p').hide()
        $('#id_reorder_quantity').closest('p').hide()
        $('#id_retire_date').closest('p').hide()
        $('#id_max_rental_days').closest('p').hide()

        $('#id_itemID').closest('p').show()
    }
    console.log(choice.val())

    choice.on('change', function(){
        if (choice.val() == 'BulkProduct') {
            $('#id_itemID').closest('p').hide()
            $('#id_retire_date').closest('p').hide()
            $('#id_max_rental_days').closest('p').hide()

            $('#id_reorder_trigger').closest('p').show()
            $('#id_reorder_quantity').closest('p').show()
        }
        else if (choice.val() == 'RentalProduct') {
            $('#id_reorder_trigger').closest('p').hide()
            $('#id_reorder_quantity').closest('p').hide()

            $('#id_itemID').closest('p').show()
            $('#id_retire_date').closest('p').show()
            $('#id_max_rental_days').closest('p').show()
        }
        else if (choice.val() == 'IndividualProduct') {
            $('#id_reorder_trigger').closest('p').hide()
            $('#id_reorder_quantity').closest('p').hide()
            $('#id_retire_date').closest('p').hide()
            $('#id_max_rental_days').closest('p').hide()

            $('#id_itemID').closest('p').show()
        }
        console.log(choice.val())
    })
})
