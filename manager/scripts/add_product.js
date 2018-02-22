$(function() {

    var choice = $('#id_type')
    choice.on('change', function(){
        console.log(choice.val())
        $().closest('p').hide()})

})
