var App = {
  setup: function() {
    App.init();
    App.network.connect();
  },

  init: function() {
    document.querySelector("template").view = 0;
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
