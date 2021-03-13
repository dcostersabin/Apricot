$('.repo').hide();

function search() {
    $('.repo').hide();
    var txt = $('#search-title').val();
    if (txt == "") {
        $('.repo').hide();
    }
    $('.repo').each(function () {
        if ($(this).text().toUpperCase().indexOf(txt.toUpperCase()) != -1) {
            $(this).show();
        }
    });
}

function repohide() {
    $('.repo').hide();

}

