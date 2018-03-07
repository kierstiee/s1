$((context => () => {

    var page_num = 0;
    var pages = context.num_pages;
    $('#products').load('/catalog/index.products/' + context.cid + '/' + page_num + '/');
    console.log(page_num, pages);

//    if (page_num = 0) {
//        $('#left_nav').closest('a').hide()
//
//        $('#right_nav').click(function() {
//            page_num = page_num + 1;
//            $('#products').load('/catalog/index.products/' + context.cid + '/' + page_num + '/');
//        })
//    }
//
//    else if (page_num > 0 && page_num < pages) {
//        $('#left_nav').click(function() {
//            page_num = page_num - 1;
//            $('#products').load('/catalog/index.products/' + context.cid + '/' + page_num + '/');
//        })
//
//        $('#right_nav').click(function() {
//            page_num = page_num + 1;
//            $('#products').load('/catalog/index.products/' + context.cid + '/' + page_num + '/');
//        })
//    }
//
//    else if (page_num = pages) {
//        $('#left_nav').click(function() {
//            page_num = page_num - 1;
//            $('#products').load('/catalog/index.products/' + context.cid + '/' + page_num + '/');
//        })
//
//        $('#right_nav').closest('a').hide()
//    }
//
//    else {
//        $('#products').load('/catalog/index/0/')
//    }

})(DMP_CONTEXT.get()));
