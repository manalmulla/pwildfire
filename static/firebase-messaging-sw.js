// firebase-messaging-sw.js
importScripts("https://www.gstatic.com/firebasejs/11.0.1/firebase-app-compat.js");
importScripts("https://www.gstatic.com/firebasejs/11.0.1/firebase-messaging-compat.js");

firebase.initializeApp({
  apiKey: "AIzaSyD8ZxEXAMPLE",
  authDomain: "wildfire-alerts.firebaseapp.com",
  projectId: "wildfire-alerts",
  storageBucket: "wildfire-alerts.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abc123xyz456"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
  console.log("[firebase-messaging-sw.js] Received background message:", payload);
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: "/static/fire.png" // optional icon
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});
