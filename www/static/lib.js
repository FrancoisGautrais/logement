/*

import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.3/firebase-app.js";
import { getMessaging, getToken } from 'https://www.gstatic.com/firebasejs/9.6.3/firebase-messaging.js';

const firebaseConfig = {
    apiKey: "AIzaSyAap-Z8-VkpcdbbTnRT3cPIZm9KtrJUdYM",
    authDomain: "notif-3e564.firebaseapp.com",
    projectId: "notif-3e564",
    storageBucket: "notif-3e564.appspot.com",
    messagingSenderId: "230684092901",
    appId: "1:230684092901:web:c8093c4b4996e5cac9670c"
};

// firebase Firebase
const app = initializeApp(firebaseConfig);

const messaging = getMessaging();
function subscribe(){

Notification.requestPermission().then(function(result) {
  getToken(messaging, { vapidKey: 'BNCGiu1tHl6CpIN4x7WUVVaHsTBoxn2L9DJorIe09Nn_St2uN8Eik9XPFqN3p_dV4wLYs2491I1oUn1AgiKyOVw' }).then((currentToken) => {
    if (currentToken) {
      console.log("token:", currentToken);
      $.get("/token?token="+currentToken)
      alert("ok")
    } else {
      console.log('No registration token available. Request permission to generate one. ',cu);
      alert("error 1 "+cu)
    }
  }).catch((err) => {
      console.log('An error occurred while retrieving token. ', err);
      alert("error "+err)
  });

});
}
navigator.serviceWorker.register('/firebase-messaging-sw.js', { type: 'module' });
window.subscribe = subscribe;

if ('serviceWorker' in navigator) {
navigator.serviceWorker.register('../firebase-messaging-sw.js')
  .then(function(registration) {
    console.log('Registration successful, scope is:', registration.scope);
  }).catch(function(err) {
    console.log('Service worker registration failed, error:', err);
  });
}


export { subscribe };
*/

/*
*
*  Push Notifications codelab
*  Copyright 2015 Google Inc. All rights reserved.
*
*  Licensed under the Apache License, Version 2.0 (the "License");
*  you may not use this file except in compliance with the License.
*  You may obtain a copy of the License at
*
*      https://www.apache.org/licenses/LICENSE-2.0
*
*  Unless required by applicable law or agreed to in writing, software
*  distributed under the License is distributed on an "AS IS" BASIS,
*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*  See the License for the specific language governing permissions and
*  limitations under the License
*
*/

/* eslint-env browser, es6 */

'use strict';

const applicationServerPublicKey = 'AAAANbXX6eU:APA91bESfJafSJ0rHH9c4-FXexHK8Gold4mArFmxuuaMcO1EcufmtIx1r9hbKVxkWcs4_JTPBjoyvVRCcrKG1iIUTGpMqgJZ4n1rFr3FyAgGvnI10sUBPND9ZrpmOHedXdTSmkrZzjTL';

const pushButton = document.querySelector('.js-push-btn');

let isSubscribed = false;
let swRegistration = null;

function urlB64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

function updateBtn() {
  if (Notification.permission === 'denied') {
    pushButton.textContent = 'Push Messaging Blocked.';
    pushButton.disabled = true;
    updateSubscriptionOnServer(null);
    return;
  }

  if (isSubscribed) {
    pushButton.textContent = 'Disable Push Messaging';
  } else {
    pushButton.textContent = 'Enable Push Messaging';
  }

  pushButton.disabled = false;
}

function updateSubscriptionOnServer(subscription) {
  // TODO: Send subscription to application server

  const subscriptionJson = document.querySelector('.js-subscription-json');
  const subscriptionDetails =
    document.querySelector('.js-subscription-details');

  if (subscription) {
    subscriptionJson.textContent = JSON.stringify(subscription);
    subscriptionDetails.classList.remove('is-invisible');
  } else {
    subscriptionDetails.classList.add('is-invisible');
  }
}

function subscribeUser() {
  const applicationServerKey = urlB64ToUint8Array(applicationServerPublicKey);
  swRegistration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: applicationServerKey
  })
  .then(function(subscription) {
    console.log('User is subscribed.');

    updateSubscriptionOnServer(subscription);

    isSubscribed = true;

    updateBtn();
  })
  .catch(function(err) {
    console.log('Failed to subscribe the user: ', err);
    updateBtn();
  });
}

function unsubscribeUser() {
  swRegistration.pushManager.getSubscription()
  .then(function(subscription) {
    if (subscription) {
      return subscription.unsubscribe();
    }
  })
  .catch(function(error) {
    console.log('Error unsubscribing', error);
  })
  .then(function() {
    updateSubscriptionOnServer(null);

    console.log('User is unsubscribed.');
    isSubscribed = false;

    updateBtn();
  });
}

function initializeUI() {
  pushButton.addEventListener('click', function() {
    pushButton.disabled = true;
    if (isSubscribed) {
      unsubscribeUser();
    } else {
      subscribeUser();
    }
  });

  // Set the initial subscription value
  swRegistration.pushManager.getSubscription()
  .then(function(subscription) {
    isSubscribed = !(subscription === null);

    updateSubscriptionOnServer(subscription);

    if (isSubscribed) {
      console.log('User IS subscribed.');
    } else {
      console.log('User is NOT subscribed.');
    }

    updateBtn();
  });
}

if ('serviceWorker' in navigator && 'PushManager' in window) {
  console.log('Service Worker and Push is supported');

  navigator.serviceWorker.register('sw.js')
  .then(function(swReg) {
    console.log('Service Worker is registered', swReg);

    swRegistration = swReg;
    initializeUI();
  })
  .catch(function(error) {
    console.error('Service Worker Error', error);
  });
} else {
  console.warn('Push messaging is not supported');
  pushButton.textContent = 'Push Not Supported';
}
