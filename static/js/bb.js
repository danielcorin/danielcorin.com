
// $(document).ready(function(){
// 	$.getJSON('http://localhost:8000/bb/api/v1/entry/', function(data){
// 		console.log(data);
// 	});
// });


var app = app || {
	Models: {},
	Views: {},
	Collections: {}
};

$(function() {


	app.Models.Entry = Backbone.Model.extend({
		defaults: {
			entry: '',
			date: new Date(),
		},

		url: function() {
			var id = this.id || '';
			return '/bb/api/v1/entry/' + id;
		}
	});

	var EntryList = Backbone.Collection.extend({
		model: app.Models.Entry,
		meta: {}, // for TastyPie
		url: '/bb/api/v1/entry/',
		parse: function(response) {
			this.meta = response.meta;
			return response.objects;
		}
	});

	app.Collections.Entry = new EntryList();

	app.Views.Entry = Backbone.View.extend({
		tagName: 'li',
		
		template: _.template($('#entry-template').html()),

		events: {
			'click .destroy': 'delete',
			'click .edit': 'edit',
			'click .update': 'update'
		},

		initialize: function() {
			this.listenTo(this.model, 'change', this.render);
			this.listenTo(this.model, 'destroy', this.remove);

		},

		render: function() {
			var self = this;
			this.$el.attr('id', this.model.get('id'));
			this.$el.html(this.template(this.model.attributes));
			return this;
		},

		delete: function() {
			this.model.destroy();
		},
		edit: function() {
			// this.$el.addClass('editing');
			this.$input.focus();
		},
		update: function() {
			var entry = this.$input.val();
			this.model.save({entry: entry});
		}
	});

	app.Views.App = Backbone.View.extend({
		el: '#life-app',
		initialize: function() {
			$.ajaxPrefilter(function(options){
				_.extend(options, {format: 'json'});
			});

			this.listenTo(app.Models.Entry, 'add', this.addOne);
			this.listenTo(app.Collections.EntryList, 'reset', this.addAll);

			app.Collections.fetch();

		},

		addOne: function(entry) {
			var view = new app.Models.Entry({model: entry});
			$('#entry-list').append(view.render().el);
		},

		addAll: function() {
			this.$('entry-list').html('');
			app.Collections.Entry.each(this.addOne, this);
		}
	});

	new app.Views.App();
});

