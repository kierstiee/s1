(function(context) {
    
    // utc_epoch comes from index.py
    console.log('Current epoch in UTC is ' + context.utc_epoch);
    
})(DMP_CONTEXT.get());

$(function() {
    var u = window.location.href.substr(window.location.href
                .lastIndexOf("/") + 1);
    $(".nav li a").each(function() {
    $h = $(this).attr("href");
    if ($h == u || $h == '')
        $(this).addClass("active");
    })
});
