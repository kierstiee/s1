var cid;
var pages

$((context => () => {

    var page_num = 0;
    pages = context.num_pages;
    cid = context.cid

//    if (page_num == 0) {
//        $('#left_nav').closest('a').hide();
//    }
//
//    else if (page_num == pages) {
//        $('#right_nav').closest('a').hide();
//    }

    $('#products').load('/catalog/index.products/' + cid + '/' + page_num + '/');
//
//    else {
//        $('#products').load('/catalog/index/0/')
//    }

})(DMP_CONTEXT.get()));

function change_page(increment) {
    var curr_page = parseInt($('#current_page').text())
    page_num = curr_page -1 + increment;
    if (page_num < 0) {page_num = 0;};
    if (page_num > pages - 1) {page_num = pages - 1;};
    $('#products').load('/catalog/index.products/' + cid + '/' + page_num + '/');
    console.log('I am the very model')
};
