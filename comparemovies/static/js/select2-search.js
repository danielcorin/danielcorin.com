function movieFormatResult(movie) {
	var markup = "<table class='movie-result'><tr>";
	if (movie.posters !== undefined && movie.posters.thumbnail !== undefined) {
		markup += "<td class='movie-image'><img src='" + movie.posters.thumbnail + "'/></td>";
	}
		markup += "<td class='movie-info'><div class='movie-title'>" + movie.title + "</div>";
	if (movie.critics_consensus !== undefined) {
		markup += "<div class='movie-synopsis'>" + movie.critics_consensus + "</div>";
	}
	else if (movie.synopsis !== undefined) {
		markup += "<div class='movie-synopsis'>" + movie.synopsis + "</div>";
	}
	markup += "</td></tr></table>";
	return markup;
}
function movieFormatSelection(movie) {
	return movie.title;
}

$(document).ready(function() {
	var apiKey = "z5meb653tvgu62a8m7kp8b6h";
	$("#selector").select2({
		placeholder: "Search for a movie",
		minimumInputLength: 1,
		ajax: {
			url: "http://api.rottentomatoes.com/api/public/v1.0/movies.json",
			dataType: 'jsonp',
			data: function (term, page) {
				return {
					q: term,
					page_limit: 10,
					apikey: apiKey,
				};
			},
			results: function (data, page) {
				return {results: data.movies};
			}	
		},
		initSelection: function(element, callback) {
			var id=$(element).val();
			if (id!=="") {
				$.ajax("http://api.rottentomatoes.com/api/public/v1.0/movies/"+id+".json", {
					data: {
						apikey: apiKey,
					},
					dataType: "jsonp"
				}).done(function(data) { callback(data); });
			}
		},
		formatResult: movieFormatResult,
		formatSelection: movieFormatSelection,
		dropdownCssClass: "bigdrop",
		dropdownAutoWidth : true,
		escapeMarkup: function (m) { return m; }
	});
	$(".select2-input").on('keyup', function(e) {
		if(e.keyCode === 13) {
			submitQuery(e);
			resetForm();
		}
	});

});