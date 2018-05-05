function toggleChildren() {
    var $element = $(this);

//    alert($element.attr('value'));
    if($element.is(':checked')) {
       $element.siblings('ul').find('input').attr('disabled', true).attr('checked', true);  
    }
    else{
        $element.siblings('ul').find('input').attr('disabled',false).attr('checked', false);
    }
}

function updateTripList() {
    $("input:checked").closest("li").remove();
    var dateItems = $(".date-checkbox").closest("li");
    for (let item of dateItems) {
        if ($($(item).children("ul")[0]).children().length === 0) {
            item.remove();
        }

    }

    var tripItems = $(".trip-checkbox").closest("li");
    for (let item of tripItems) {
        if ($($(item).children("ul")[0]).children().length === 0) {
            item.remove();
        }
    }
    
    // $("#delete-button").css("visibility", "hidden");
}

function deletePlaces(evt) {
    evt.preventDefault();
    var formValues = $('#user-all-trips').serialize();
    $.post("/delete_places",
            formValues,
            updateTripList
        );
}

$('.trip-checkbox, .date-checkbox').on('click', toggleChildren);


$('#user-all-trips').on('submit', deletePlaces)
