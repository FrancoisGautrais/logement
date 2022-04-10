// Scripts for firebase and firebase messaging

importScripts('https://www.gstatic.com/firebasejs/8.2.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.2.0/firebase-messaging.js');

// Initialize the Firebase app in the service worker by passing the generated config
var firebaseConfig = {
    apiKey: "AIzaSyAap-Z8-VkpcdbbTnRT3cPIZm9KtrJUdYM",
    authDomain: "notif-3e564.firebaseapp.com",
    projectId: "notif-3e564",
    storageBucket: "notif-3e564.appspot.com",
    messagingSenderId: "230684092901",
    appId: "1:230684092901:web:c8093c4b4996e5cac9670c"
};

firebase.initializeApp(firebaseConfig);

// Retrieve firebase messaging

const messaging = firebase.messaging();
/*
messaging.onBackgroundMessage(function(payload) {
  console.log('Received background message ', payload);

  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
  };

//  self.registration.showNotification(notificationTitle,
//    notificationOptions);
});

self.addEventListener('push', function(event) {
  console.log('[Service Worker] Push Received.');
  console.log(`[Service Worker] Push had this data: "${event.data.text()}"`);

  const title = 'Push Codelab';
  const options = {
    body: 'Yay it works.',
    icon: 'images/icon.png',
    badge: 'images/badge.png'
  };

  event.waitUntil(self.registration.showNotification(title, options));
});*/