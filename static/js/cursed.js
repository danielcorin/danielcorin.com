$("span.increment").click(function(e){
	var csrftoken = $('[name="csrfmiddlewaretoken"]')[0].value;
	var name = $(this).closest(".name").attr('id');
	$.post( "/curses/", {
		name: name,
		csrfmiddlewaretoken: csrftoken,
	}).done(function(data) {
		$("#count_danny").find(".count_value").html(data.count_danny);
		$("#count_danny").find(".amt").html(data.amt_danny);

		$("#count_des").find(".count_value").html(data.count_des);
		$("#count_des").find(".amt").html(data.amt_des);

	});
});