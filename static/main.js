// Firebase setup
const firebaseConfig = {
  apiKey: "AIzaSyD8ZxEXAMPLE",
  authDomain: "wildfire-alerts.firebaseapp.com",
  projectId: "wildfire-alerts",
  storageBucket: "wildfire-alerts.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abc123xyz456"
};

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

document.getElementById("enable-push").addEventListener("click", async () => {
  try {
    const token = await messaging.getToken({ vapidKey: "YOUR_VAPID_KEY" });
    console.log("User token:", token);
    alert("Push enabled! You’ll receive wildfire alerts.");

    // send token to backend
    await fetch("/register_token", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token })
    });
  } catch (e) {
    console.error("Push setup failed:", e);
  }
});
