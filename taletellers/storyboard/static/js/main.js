function show_details(content) {
    content.style.backgroundColor = "yellow";
}
function hide_details(content) {
    content.style.backgroundColor = "white";
}

$(function () {
    $('[data-toggle="popover"]').popover()
});
$('[data-toggle="popover"]').click(function () {
});
$('.storya').click(function() {
    var id = $(this).context.attributes.id.value;

$.ajax({
    url: '{% url "ulr" %}',
    data: {
        'id': id
    },
    dataType: "json",
    success: function(data) {
        $('.boru').text(data.score);
    }
});
});
$(document).on("click", "#like_button", function() {
    var id = $(this).context.attributes.name.value;
    $.ajax({
        data: {
            "like": "true",
            "id": id
        },
        url: "{% url "like_dislike" %}",
        success: function (data) {
            $('.boru').text(data.like);
        }
    }
)});
$(document).on("click", "#dislike_button", function() {
    var id = $(this).context.attributes.name.value;
    $.ajax({
        data: {
            "like": "false",
            "id": id
        },
        url: "{% url "like_dislike" %}",
        success: function (data) {
            $('.boru').text(data.like);
        }
    }
)}
);
$(document).on("click", "#close_button", function() {
     $('[data-toggle="popover"]').popover("hide")
     $('[data-toggle="popover"]').popover()
});


// ajax example
/*
<span id="like_{{ object.id }}">{{object.score}}</span>
<button onclick="like(true, {{ object.id }})">Like</button>
<button onclick="like(false, {{ object.id }})">Dislike</button>


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


function like(param) {
	$.post({
		data: "{'like': param, 'id': {{object.id}}, 'csrfmiddlewaretoken': getCookie('csrftoken')},
		url: "{% url 'like_dislike' %}
	});
}

 */
