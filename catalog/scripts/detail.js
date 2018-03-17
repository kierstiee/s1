$((context => () => {
    picture = context.url;
    $('#first_pic').attr('src',picture);
})(DMP_CONTEXT.get()));

function change_pic(pic) {
    picture = pic;
    $('#first_pic').attr('src',picture);
};
