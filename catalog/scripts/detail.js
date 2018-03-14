var cid;
var pages

$((context => () => {

})(DMP_CONTEXT.get()));

function change_page(increment) {
    var curr_page = parseInt($('#current_page').text())
    page_num = curr_page -1 + increment;
    if (page_num < 0) {page_num = 0;};
    if (page_num > pages - 1) {page_num = pages - 1;};
    $('#products').load('/catalog/index.products/' + cid + '/' + page_num + '/');
};
