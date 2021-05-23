function tableRenumberRows() {
    $('.table tbody tr').each(function(i) {
        var number = i + 1;
        $(this).find('th:first').text(number);
    });
}

tableRenumberRows();