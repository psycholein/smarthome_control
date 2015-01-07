var App = {
  setup: function() {
    document.querySelector("template").view = 0;
    App.network.connect();

    $(window).bind('polymer-ready', App.init);
  },

  init: function() {
    $('body').on('change', '[data-route][data-event="change"]', App.sendData);
  },

  sendData: function(e) {
    var data = {
      'path':   $(this).data('route'),
      'values': {
        'device': $(this).attr('name'),
        'value': $(this).val()
      }
    };
    App.network.send(JSON.stringify(data));
  },

  updateData: function(data) {
    $.each(data, function(room, values){
      $.each(values, function(key, value){
        var selector = '[data-room="'+room+'"] .'+key;
        if ($(selector).prop("tagName") == 'SELECT')
          $(selector).val(value);
        else
          $(selector).html(value);
      });
    });
  },

  routes: function(data) {
    switch (data.path) {
      case 'outputToJs': return App.updateData(data.values);
    }
  },

  config: {
    ws: "ws://"+document.location.host+"/ws"
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
      }, 60000);
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
