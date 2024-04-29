$('#checkmark-svg').on('click', function () {
    svg = $(this);
    svg.removeClass('run-animation').width();
    svg.addClass('run-animation');
    return false;
})