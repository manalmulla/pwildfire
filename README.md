# pwildfire

git add .
git commit -m "message"
git push

// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyClttRdIKgGNAippwACVnnIk-R5CSp8blQ",
  authDomain: "wildfire-alert-d7468.firebaseapp.com",
  projectId: "wildfire-alert-d7468",
  storageBucket: "wildfire-alert-d7468.firebasestorage.app",
  messagingSenderId: "387792405495",
  appId: "1:387792405495:web:3072b509c3711547a964f2"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
