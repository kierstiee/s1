$(function() {

    var choice = $("#id_type")
    if (choice.val() == 'BulkProduct') {
        $('#id_itemID').hide()
        $('#id_retire_date').hide()
        $('#id_max_rental_days').hide()

        $('#id_reorder_trigger').show()
        $('#id_reorder_quantity').show()
    }
    else if (choice.val() == 'RentalProduct') {
        $('#id_reorder_trigger').hide()
        $('#id_reorder_quantity').hide()

        $('#id_itemID').show()
        $('#id_retire_date').show()
        $('#id_max_rental_days').show()
    }
    else if (choice.val() == 'IndividualProduct') {
        $('#id_reorder_trigger').hide()
        $('#id_reorder_quantity').hide()
        $('#id_retire_date').hide()
        $('#id_max_rental_days').hide()

        $('#id_itemID').show()
    }
    console.log(choice.val())

    choice.on('change', function(){
        if (choice.val() == 'BulkProduct') {
            $('#id_itemID').hide()
            $('#id_retire_date').hide()
            $('#id_max_rental_days').hide()

            $('#id_reorder_trigger').show()
            $('#id_reorder_quantity').show()
        }
        else if (choice.val() == 'RentalProduct') {
            $('#id_reorder_trigger').hide()
            $('#id_reorder_quantity').hide()

            $('#id_itemID').show()
            $('#id_retire_date').show()
            $('#id_max_rental_days').show()
        }
        else if (choice.val() == 'IndividualProduct') {
            $('#id_reorder_trigger').hide()
            $('#id_reorder_quantity').hide()
            $('#id_retire_date').hide()
            $('#id_max_rental_days').hide()

            $('#id_itemID').show()
        }
        console.log(choice.val())
    })
})
