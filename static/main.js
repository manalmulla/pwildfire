const firebaseConfig = {
  apiKey: "AIzaSyClttRdIKgGNAippwACVnnIk-R5CSp8blQ",
  authDomain: "wildfire-alert-d7468.firebaseapp.com",
  projectId: "wildfire-alert-d7468",
  storageBucket: "wildfire-alert-d7468.appspot.com", 
  messagingSenderId: "387792405495",
  appId: "1:387792405495:web:3072b509c3711547a964f2"
};

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

document.getElementById("alertBtn").addEventListener("click", async () => {
  try {
    const permission = await Notification.requestPermission();
    if (permission !== "granted") {
      alert("Please allow notifications to get alerts.");
      return;
    }

    const registration = await navigator.serviceWorker.ready;

    const token = await messaging.getToken({
      vapidKey: "BK11-muydgKpG5xyyGOxnUPCnObnxdnmBL2D32IhkjEY4uotqBaCK72yYVUwhuXMFBt7Pu7Qk3DzijygiPZAHyQ",
      serviceWorkerRegistration: registration
    });

    console.log("Token:", token);

    await fetch("/register_token", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token }),
    });

    alert("✅ Push alerts enabled!");
  } catch (err) {
    console.error("Error enabling alerts:", err);
  }
});
