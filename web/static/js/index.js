$(function() {
      window.ImageView = Backbone.View.extend(
          {
              tagName: 'div',

              initialize: function(options) {
                  this.el = $(this.el);
                  this.src = '';
              },

              render: function()
              {
                  this.el.children().remove();
                  this.el.append($('<img src="' + this.src + '" />'));
                  return this;
              },

              setSrc: function(src)
              {
                  this.src = src;
                  this.render();
              }
          }
      );

      window.GuestView = Backbone.View.extend(
          {
              tagName: 'fieldset',

              template: _.template('<input type="checkbox" name="guest" value="<%= name %>" /><%= name %><br />'),

              initialize: function(options) {
                  this.el = $(this.el);
                  this.guests = options.guests;
              },

              render: function() {
                  this.el.children().remove();
                  this.el.append('<legend>Guests</legend>');
                  var self = this;
                  _.each(this.guests, function(guest)
                         {
                             self.el.append(self.template(
                                            {
                                                name: guest
                                            }));
                         });
                  return this;
              },

              getValues: function()
              {
                  var result = [];
                  this.el.find('input:checked').each(
                      function()
                      {
                          result.push($(this).val());
                      });
                  return result;
              }
          });

      window.MeasureView = Backbone.View.extend(
          {
              tagName: 'fieldset',

              template: _.template('<input type="radio" name="measure" value="<%= name %>" /><%= name %><br />'),

              initialize: function(options) {
                  this.el = $(this.el);
                  this.measures = options.measures;
              },

              render: function() {
                  this.el.children().remove();
                  this.el.append('<legend>Measures</legend>');
                  var self = this;
                  _.each(this.measures, function(measure)
                         {
                             self.el.append(self.template(
                                            {
                                                name: measure
                                            }));
                         });
                  return this;
              },

              getValue: function()
              {
                  return this.el.find('input:checked').val();
              }
          });

      var imageView = new window.ImageView();

      var guestView = new window.GuestView(
          {
              // TODO: we should update the guest list.
              guests: ['guest-0', 'guest-1'] 
          });
      var measureView = new window.MeasureView(
          {
              // TODO: we should update the measure list.
              measures: ['measure-0', 'measure-1'] 
          });

      $(document.body).append(guestView.render().el);
      $(document.body).append(measureView.render().el);
      $(document.body).append(imageView.render().el);

      var refresh = function()
      {
          // TODO: we should update the src.
          imageView.setSrc('/graph/graph.png');
      };

      setInterval(refresh, 1000);
  }
);
