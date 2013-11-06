$('.wishlist-btns .btn').click(function(event){
    event.preventDefault();
    $('.btn').removeClass('active')
    var btn = ($(this))
    var span = $(this).children('span')
    var msg = $(this).parent().siblings('.ajax-response')
    var classes = $(span).attr('class');

    $(this).children('span').attr('class', 'icon-refresh icon-spin');

    $.getJSON($(this).attr('data-url'), function(response){
        $(span).attr('class', classes);
        $(btn).addClass('active')
        $(msg).fadeIn()
    });
    return false
});
