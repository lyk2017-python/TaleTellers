function show_details(content) {
    content.style.backgroundColor = "yellow";
}
function hide_details(content) {
    content.style.backgroundColor = "white";
}

/*
function getCookie(name) {
	// django's official function, search => "django csrf ajax"
}


function inc_like(param) {
	$.post({
		data: "{'like': param, 'id': {{object.id}}, 'csrfmiddlewaretoken': getCookie('csrftoken')},
		url: "{% url 'like_dislike' %}
	});
}

 */
