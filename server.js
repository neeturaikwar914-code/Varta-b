import express from "express";
import cors from "cors";
import bodyParser from "body-parser";
import jwt from "jsonwebtoken";
import admin from "firebase-admin";
import dotenv from "dotenv";
import fs from "fs";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Firebase Admin SDK
const serviceAccount = JSON.parse(fs.readFileSync(process.env.FIREBASE_ADMIN_SDK_PATH, "utf-8"));
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();

// Middleware
app.use(cors());
app.use(bodyParser.json());

// JWT verification middleware
function verifyToken(req, res, next) {
  const token = req.headers["authorization"];
  if(!token) return res.status(401).json({ error: "No token provided" });

  jwt.verify(token, process.env.JWT_SECRET, (err, decoded) => {
    if(err) return res.status(401).json({ error: "Invalid token" });
    req.user = decoded;
    next();
  });
}

// Signup API
app.post("/signup", async (req, res) => {
  const { email, password, username } = req.body;
  try {
    const userRecord = await admin.auth().createUser({ email, password, displayName: username });
    await db.collection("users").doc(userRecord.uid).set({ email, username });
    const token = jwt.sign({ uid: userRecord.uid, email }, process.env.JWT_SECRET, { expiresIn: "7d" });
    res.json({ token, uid: userRecord.uid });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Login API
app.post("/login", async (req, res) => {
  const { email, password } = req.body;
  try {
    // Firebase Admin SDK cannot verify password, so use Firebase Client SDK in frontend
    // Here we can just check if user exists
    const user = await admin.auth().getUserByEmail(email);
    const token = jwt.sign({ uid: user.uid, email }, process.env.JWT_SECRET, { expiresIn: "7d" });
    res.json({ token, uid: user.uid, username: user.displayName });
  } catch (error) {
    res.status(401).json({ error: "Invalid email or password" });
  }
});

// Protected route example
app.get("/profile", verifyToken, async (req, res) => {
  const userDoc = await db.collection("users").doc(req.user.uid).get();
  if(!userDoc.exists) return res.status(404).json({ error: "User not found" });
  res.json({ profile: userDoc.data() });
});

app.listen(PORT, () => console.log(`Varta backend running on port ${PORT}`));
