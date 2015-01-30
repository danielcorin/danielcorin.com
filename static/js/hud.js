var api_array = ['github', 'goodreads', 'kippt', 'lastfm', 'strava', 'twitter', 'untappd', 'swarm'];
var date_keys = ['created_at', 'date', 'start_date', 'updated_at', 'created', 'episode_watched']

function api_tag(api_name) {
	return "#" + api_name;
}

function template_id(api_name) {
	return "#" + api_name + "_template";
}

function api_url(api_name) {
	return '/hud/' + api_name;
}

function convert_date(data) {
	for(var i = 0, l = date_keys.length; i < l; i++) {
		if (data[date_keys[i]] !== undefined) {
			var d = new Date(data[date_keys[i]]);
			data[date_keys[i]] = d.toLocaleString();
		}
		if (data['currently_reading'] !== undefined) {
			var d  = new Date(data['currently_reading'][0]['started_at']);
			data['currently_reading'][0]['started_at'] = d.toLocaleString();
		}
	}
	return data;
}

function render_api(api_name) {
	$.getJSON(api_url(api_name), function(data){
		data.data = convert_date(data.data);
		var template_html = $(template_id(api_name)).html();
		var t = _.template(template_html);
		$(api_tag(api_name)).html(t(data));
	});
}

$(document).ready(function(){
	for (var i = 0, l = api_array.length; i < l; i++) {
		render_api(api_array[i]);
	}
});
