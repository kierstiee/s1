$((context => () => {
    picture = context.url;
    console.log(picture);
    $('#first_pic').attr('src',picture);
})(DMP_CONTEXT.get()));

function change_pic(pic) {
    picture = pic;
    console.log(picture);
    $('#first_pic').attr('src',picture);
};
