var App = {
  setup: function() {
    App.network.connect();
    App.init();
  },

  init: function() {
    $('#tabs').tabs();
    $('body').on('change', '[data-route][data-event="change"]', App.sendData);
    $('body').on('click', '[data-category="climate"] [data-collection] > label', App.getHighchart);
  },

  sendData: function(e) {
    var data = {
      'path': $(this).data('route'),
      'values': {
        'device': $(this).attr('name'),
        'value': $(this).val()
      }
    };
    App.network.send(JSON.stringify(data));
  },

  getHighchart: function(e) {
    var data = {
      'path': 'highchart',
      'values': {
        'category': $(e.currentTarget).closest('[data-category]').data('category'),
        'collection': $(e.currentTarget).closest('[data-collection]').data('collection')
      }
    };
    App.network.send(JSON.stringify(data));
  },

  updateData: function(data) {
    $.each(data, function(category, collections) {
      $.each(collections, function(collection, values) {
        $.each(values, function(key, value){
          var selector = '[data-category="'+category+'"] [data-collection="'+collection+'"] .'+key;
          if ($(selector).prop("tagName") == 'SELECT')
            $(selector).val(value.value);
          else if ($(selector).prop("tagName") == 'INPUT')
            $(selector).filter('[value='+value.value+']').prop('checked', true);
          else
            $(selector).html(value.value);
          selector = '[data-collection="'+collection+'"] .'+key+'_date';
          $(selector).html(value.date);
        });
      });
    });
  },

  highchart: function(data) {
    console.log(data);
  },

  routes: function(data) {
    if (data.path != 'outputToJs') return;
    switch (data.values.type) {
      case 'values': return App.updateData(data.values.data);
      case 'highchart': return App.highchart(data.values.data);
    }
  },

  config: {
    ws: "ws" + (location.protocol == "https:" ? "s" : "") +
        "://"+document.location.host+"/ws"
  },

  events: {
    connected: function(event) {
    },
    disconnected: function(event) {
      App.network.reconnect();
    },
    message: function(event) {
      try {
        data = JSON.parse(event.data);
        App.routes(data);
      } catch (e) {}
    },
    error: function(event) {
      App.network.reconnect();
    }
  },

  network: {
    ws: null,
    connect: function() {
      if (App.network.ws && App.network.ws.readyState == WebSocket.OPEN) return;
      try {
        App.network.ws           = new WebSocket(App.config.ws);
        App.network.ws.onopen    = App.events.connected;
        App.network.ws.onclose   = App.events.disconnected;
        App.network.ws.onmessage = App.events.message;
        App.network.ws.onerror   = App.events.error;
      } catch (e) {}
    },
    reconnect: function() {
      setTimeout(function() {
        App.network.connect();
      }, 5000);
    },
    checkAndReconnect: function() {
      setInterval(function(){
        if (!App.network.ws || App.network.ws.readyState != WebSocket.OPEN)
          App.network.connect();
      }, 5000);
    },
    disconnect: function() {
      App.network.ws.close();
      App.network.ws = null;
    },
    send: function(message) {
      if (message && App.network.ws && App.network.ws.readyState == WebSocket.OPEN) {
        App.network.ws.send(message);
      } else {
        App.network.connect();
        var msg = message;
        setTimeout(function() {
          App.network.send(msg);
        }, 2000);
      }
    }
  }
};

$(function(){
  App.setup();
});
