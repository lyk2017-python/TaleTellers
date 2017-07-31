function show_details(content) {
    content.style.backgroundColor = "yellow";
}
function hide_details(content) {
    content.style.backgroundColor = "white";
}

/*
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


function inc_like(param) {
	$.post({
		data: "{'like': param, 'id': {{object.id}}, 'csrfmiddlewaretoken': getCookie('csrftoken')},
		url: "{% url 'like_dislike' %}
	});
}

 */
