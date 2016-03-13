if ('serviceWorker' in navigator) {
  console.log('Service Worker is supported');
  navigator.serviceWorker.register('/static/sw.js').then(function(reg) {
    console.log(':^)', reg);
    reg.pushManager.subscribe({
      userVisibleOnly: true
    }).then(function(sub) {
      console.log('endpoint:', sub.endpoint);
    });
  }).catch(function(err) {
    console.log(':^(', err);
  });
}
