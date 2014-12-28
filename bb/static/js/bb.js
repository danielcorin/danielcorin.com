var ESC_KEY = 27;
var app = app || {
	Models: {},
	Views: {},
	Collections: {},
	editing: undefined
};

String.prototype.nl2br = function() {
	var br;
	if( typeof arguments[0] != 'undefined' ) {
		br = arguments[0];
	}
	else {
		br = '<br />';
	}
	return this.replace( /\r\n|\r|\n/g, br );
}
 
String.prototype.br2nl = function() {
	var nl;
	if( typeof arguments[0] != 'undefined' ) {
		nl = arguments[0];
	}
	else {
		nl = '\r\n';
	}
	return this.replace( /\<br(\s*\/|)\>/g, nl );
}

$(function() {

	app.Models.Entry = Backbone.Model.extend({
		defaults: {
			entry: '',
			created: new Date(),
			date: moment().format("YYYY-MM-DD"), // date of entry
			user: '/bb/api/v1/user/1/'
		},

		url: function() {
			var id = this.id || '';
			return id;
		},
	});

	var EntryList = Backbone.Collection.extend({
		model: app.Models.Entry,
		meta: {}, // for TastyPie
		url: '/bb/api/v1/entry',
		parse: function(response) {
			this.meta = response.meta;
			return response.objects;
		},
		comparator: function(m1, m2) {
			// sort by date and most recently created entry first
			if (m1.get('date') === m2.get('date')) {
				return true;
			}
			else {
				return m1.get('created') < m2.get('created');
			}
		}
	});

	app.Collections.Entry = new EntryList();

	app.Views.Entry = Backbone.View.extend({
		tagName: 'li',
		
		template: _.template($('#entry-template').html()),

		events: {
			'click .destroy': 'delete',
			'click .edit': 'edit',
			'click .update': 'update',
			'click .cancel': 'cancel',
			'keydown .entry-item': 'revertOnEscape'
		},
		initialize: function() {
			this.listenTo(this.model, 'change', this.render);
			this.listenTo(this.model, 'destroy', this.remove);
		},

		render: function() {
			var self = this;
			this.$el.attr('id', this.model.get('id'));
			this.$el.html(this.template({
				date: _.escape(this.model.attributes.date),
				entry: _.escape(this.model.attributes.entry).nl2br()
			}));
			return this;
		},

		delete: function(e) {
			e.preventDefault();
			this.model.destroy();
		},
		// replace the entry text with a form containing it for editing
		edit: function(e) {
			e.preventDefault();
			// check if an entry is already being edited
			if (app.editing) {
				app.editing.render();
				app.editing = undefined;
			}
			var editTemplate = _.template($('#edit-entry-template').html());

			this.$el.html(editTemplate({
				date: _.escape(this.model.attributes.date),
				entry: _.escape(this.model.attributes.entry)
			}));
			this.$input = $("#edit-field");
			this.$input.focus();
			// set this entry to the current one being edited
			app.editing = this;
			return this;
		},
		// get the edited entry, save it to the database, and re-render
		update: function(e) {
			e.preventDefault();
			var entry = this.$input.val();
			this.model.save(
				{entry: entry.br2nl()}
				);
			this.render();
			app.editing = undefined;
		},
		cancel: function(e) {
			e.preventDefault();
			this.render();
			app.editing = undefined;
		},
		revertOnEscape: function (e) {
			if (e.which === ESC_KEY) {
				this.cancel(e);
			}
		}
	});

	app.Views.App = Backbone.View.extend({
		el: '#life-app',
		initialize: function() {
			$.ajaxPrefilter(function(options){
				_.extend(options, {format: 'json'});
			});

			// this.listenTo(app.Collections.Entry, 'add', this.addOne);
			this.listenTo(app.Collections.Entry, 'reset', this.addAll);

			app.Collections.Entry.fetch({reset:true});
		},

		events: {
			'click .add': 'addNew'
		},
		// add model pulling text from new entry field
		addNew: function(e) {
			e.preventDefault();
			var field = $("#new-entry-field");
			var newEntry = field.val();
			field.val("");
			var entry = app.Collections.Entry.create(
				{entry: newEntry},
				{url: '/bb/api/v1/entry/'}
			);
			var self = this;
			app.Collections.Entry.fetch({
				success: function(resp) {
					self.addAll();
				}
			});
		},
		addOne: function(entry) {
			var view = new app.Views.Entry({model: entry});
			$('#entry-list').append(view.render().el);
		},

		addAll: function() {
			this.$('#entry-list').html('');
			app.Collections.Entry.each(this.addOne, this);
		}
	});

	new app.Views.App();
});

