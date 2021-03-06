$(function() {
      var THREAT_LLC_LOADS = 10000000;

      window.ImageView = Backbone.View.extend(
          {
              tagName: 'div',

              initialize: function() {
                  this.el = $(this.el);
                  this.el.append($('<div style="display: none"></div>'));
                  this.src = '';
              },

              render: function()
              {
                  this.el.find('> img').remove();
                  this.el.append(this.el.find('div img').detach());
                  this.el.find('div').append($('<img src="' + this.src + '" />'));
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

              template: _.template('<input type="checkbox" name="guest" value="<%= name %>" /><span id="span_<%= name %>"><%= name %></span><br />'),

              initialize: function() {
                  this.el = $(this.el);
                  this.guests = [];
              },

              setGuests: function(guests) {
                  this.guests = guests;
                  this.render();
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
              },

              setRed: function(guest)
              {
                  this.el.find('span[id="span_' + guest + '"]').addClass('red');

              },

              unsetRed: function(guest)
              {
                  this.el.find('span[id="span_' + guest + '"]').removeClass('red');
              }
          });

      window.MeasureView = Backbone.View.extend(
          {
              tagName: 'fieldset',

              template: _.template('<input type="radio" name="measure" value="<%= name %>" /><%= name %><br />'),

              initialize: function() {
                  this.el = $(this.el);
                  this.measures = [];
              },

              setMeasures: function(measures) {
                  this.measures = measures;
                  this.render();
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
      var guestView = new window.GuestView();
      var measureView = new window.MeasureView();

      $(document.body).append(guestView.render().el);
      $(document.body).append(measureView.render().el);
      $(document.body).append(imageView.render().el);

      $.get('/graph/guests', function(guests)
            {
                guestView.setGuests(guests);
            });
      $.get('/graph/measures', function(measures)
            {
                measureView.setMeasures(measures);
            });

      var count = 0;
	  var old_threat_guest;
      var refresh = function()
      {
          var guests = guestView.getValues();
          var measure = measureView.getValue();
          measure = measure ? measure : '';
          imageView.setSrc('/graph/graph.png?count=' + (++count) + '&duration=100&guests=' + guests + '&measure=' + measure);

          $.get('/graph/threat_llc_loads', function(threat)
                {
                    if (threat.value > THREAT_LLC_LOADS)
                    {
                        guestView.unsetRed( old_threat_guest );
						old_threat_guest = threat.max_guest;
                        guestView.setRed( threat.max_guest );
                    }
                    else
                    {
                        guestView.unsetRed( old_threat_guest );
                    }
                });
      };

      setInterval(refresh, 1000);
  }
);
