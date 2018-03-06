(function(context) {
    return function(){
        // utc_epoch comes from index.py
        console.log('Current epoch in UTC is ' + context.utc_epoch);}
})(DMP_CONTEXT.get());

//on click event
//$("#products").load()
//"/catalog/index.products/cid/page_num"  the .products is a def in my index.py
