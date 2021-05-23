Sortable.create(list, {
    group: 'shared',
    multiDrag: true,
    selectedClass: "selected",

    animation: 0,
    ghostClass: 'blue-background-class'
});


$("tr").on("dragend",function(){
    setTimeout(tableRenumberRows, 10);
});