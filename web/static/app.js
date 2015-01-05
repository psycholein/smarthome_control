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
      'path': $(this).data('route'),
      'values': {
        'device': $(this).attr('name'),
        'value': $(this).val()
      }
    };
    App.network.send(JSON.stringify(data));
  },

  config: {
    ws: "ws://"+document.location.host+"/ws"
  },

  events: {
    connected: function(event) {
    },
    disconnected: function(event) {
    },
    message: function(event) {
      // event.data
    },
    error: function(event) {
      // event.data
    }
  },

  network: {
    ws: null,
    connect: function() {
      App.network.ws           = new WebSocket(App.config.ws);
      App.network.ws.onopen    = App.events.connected;
      App.network.ws.onclose   = App.events.disconnected;
      App.network.ws.onmessage = App.events.message;
      App.network.ws.onerror   = App.events.error;
    },
    disconnect: function() {
      App.network.ws.close();
      App.network.ws = null;
    },
    send: function(message) {
      if (message && App.network.ws)
        App.network.ws.send(message);
    }
  }
};

$(function(){
  App.setup();
});
