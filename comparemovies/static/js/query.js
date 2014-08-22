$("#query").submit(function(event) {
	event.preventDefault();
	var url = "/query/";
	$("#message").html();
	$.ajax({
		type: "POST",
		url: url,
		data: $("#query").serializeArray(),
		success: function(data) {
			// check if data.success is literally false
			// otherwise, add the rendered html to table
			if (data.success == false) {
				$("#message").html(data.message);
				resetElement("query");
			}
			else {
				$("#message").html();
				$('#theTableBody').append(data);
				resetElement("query");
			}
		},
		failure: function(data) {
			$("#messge").html("Error");
			resetElement("query");
		},
	});
});

function resetElement(element) {
	document.getElementById(element).reset();
}

$("#clearAll").click(function(event){
	event.preventDefault();
	$("#theTableBody").html();
});