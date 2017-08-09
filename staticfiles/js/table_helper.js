function saveTableTab(page_id) {
    // save location of viewing table
    $('.yeartable').click(function () {
        current_year = $(this).attr('href');
        console.log(current_year);
        document.cookie = "current_table_" + page_id + "=" + current_year;
    });

    // read cookie to restore last viewed tab
    var cookie = document.cookie;
    current_year = readCookie('current_table_' + page_id);
    if (current_year) {
        current_year = current_year.replace('#', '');
        $('ul.tabs').tabs('select_tab', current_year);
    }
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}