(function(context) {
    
    // utc_epoch comes from index.py
    console.log('Current epoch in UTC is ' + context.utc_epoch);
    
})(DMP_CONTEXT.get());

$(document).ready(function() {
	// get current URL path and assign 'active' class
	var pathname = window.location.pathname;
	$('.nav > li > a[href="'+pathname+'"]').parent().addClass('active');
})
