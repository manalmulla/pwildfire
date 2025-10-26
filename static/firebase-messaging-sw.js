importScripts("https://www.gstatic.com/firebasejs/11.0.1/firebase-app-compat.js");
importScripts("https://www.gstatic.com/firebasejs/11.0.1/firebase-messaging-compat.js");

firebase.initializeApp({
  apiKey: "AIzaSyClttRdIKgGNAippwACVnnIk-R5CSp8blQ",
  authDomain: "wildfire-alert-d7468.firebaseapp.com",
  projectId: "wildfire-alert-d7468",
  storageBucket: "wildfire-alert-d7468.appspot.com",
  messagingSenderId: "387792405495",
  appId: "1:387792405495:web:3072b509c3711547a964f2"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
  console.log("[SW] Background message:", payload);
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: "/static/fire.png"
  };
  self.registration.showNotification(notificationTitle, notificationOptions);
});
