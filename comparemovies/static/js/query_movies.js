$("#query").submit(function(event) {
	submitQuery(event);
});


function submitQuery(event, title) {
	event.preventDefault();
	var url = "/query/";
	try {
		if (typeof(title)==='undefined') {
			title = $('#selector').select2('data').title;
		}
	}
	catch(exc){
		return;
	}
	$("#message").html();
	$.ajax({
		type: "POST",
		url: url,
		data: {
			movie: title,
			csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]')[0].value
		},
		success: function(data) {
			// check if data.success exists and is literally false
			// otherwise, add the rendered html to table
			if (data.success == false) {
				$("#message").html(data.message);
				resetForm();
			}
			else {
				$("#message").html();
				$('#theTable tbody').append(data);
				$("#theTable").trigger("update"); 
				resetForm();
				return;
			}
		},
		failure: function(data) {
			$("#messge").html("Error");
			resetForm();
			return;
		},
	});
}

$("#recent").click(function(event) {
	event.preventDefault();
	populateRecent(event);
});

function populateRecent(event) {
	$.getJSON("/recent", function(data){
		$.each(data.movies, function(i, movie_title){
			submitQuery(event, movie_title);
		});
		resetForm();
		return false;
	});
}

function resetForm() {
	$("#selector").select2('data', null)
}

function clearAll() {
	$("#message").html("");
	$("#theTableBody").empty();
	$("#theTable").trigger("update"); 
}

$("#clearAll").click(function(event){
	event.preventDefault();
	clearAll();
});