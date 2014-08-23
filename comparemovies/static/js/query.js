$("#query").submit(function(event) {
	submitQuery(event);
});


function submitQuery(event) {
	event.preventDefault();
	var url = "/query/";
	var title = null;
	try {
		title = $('#selector').select2('data').title;
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
				return false;
			}
		},
		failure: function(data) {
			$("#messge").html("Error");
			resetForm();
		},
	});
}

function resetForm() {
	$("#selector").select2('data', null)
}

$("#clearAll").click(function(event){
	event.preventDefault();
	$("#theTableBody").empty();
});