<<<<<<< HEAD
import express from "express";
import sqlite3 from "sqlite3";
import { open } from "sqlite";
import cors from "cors";
import path from "path";

const app = express();
app.use(cors());
app.use(express.json());

// Serve frontend files from 'public' folder
app.use(express.static(path.join(process.cwd(), "public")));

let db;

// Initialize SQLite database
(async () => {
  db = await open({
    filename: "./cashflow.db",
    driver: sqlite3.Database
  });

  await db.exec(`
    CREATE TABLE IF NOT EXISTS entries (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user TEXT,
      date TEXT,
      description TEXT,
      amount REAL,
      type TEXT
    )
  `);

  console.log("✅ Database ready (cashflow.db)");
})();

// --- API routes ---

// Get all entries for a user
app.get("/api/entries/:user", async (req, res) => {
  try {
    const user = req.params.user;
    const rows = await db.all(
      "SELECT * FROM entries WHERE user = ? ORDER BY date ASC",
      [user]
    );
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Failed to load entries" });
  }
});

// Add a new entry
app.post("/api/entries", async (req, res) => {
  try {
    const { user, date, description, amount, type } = req.body;
    if (!user || !date || !description || !amount || !type) {
      return res.status(400).json({ error: "Missing required fields" });
    }

    await db.run(
      "INSERT INTO entries (user, date, description, amount, type) VALUES (?, ?, ?, ?, ?)",
      [user, date, description, amount, type]
    );
    res.json({ status: "ok" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Failed to save entry" });
  }
});

// --- Start server ---
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
=======
import express from "express";
import sqlite3 from "sqlite3";
import { open } from "sqlite";
import cors from "cors";
import path from "path";

const app = express();
app.use(cors());
app.use(express.json());

// Serve frontend files from 'public' folder
app.use(express.static(path.join(process.cwd(), "public")));

let db;

// Initialize SQLite database
(async () => {
  db = await open({
    filename: "./cashflow.db",
    driver: sqlite3.Database
  });

  await db.exec(`
    CREATE TABLE IF NOT EXISTS entries (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user TEXT,
      date TEXT,
      description TEXT,
      amount REAL,
      type TEXT
    )
  `);

  console.log("✅ Database ready (cashflow.db)");
})();

// --- API routes ---

// Get all entries for a user
app.get("/api/entries/:user", async (req, res) => {
  try {
    const user = req.params.user;
    const rows = await db.all(
      "SELECT * FROM entries WHERE user = ? ORDER BY date ASC",
      [user]
    );
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Failed to load entries" });
  }
});

// Add a new entry
app.post("/api/entries", async (req, res) => {
  try {
    const { user, date, description, amount, type } = req.body;
    if (!user || !date || !description || !amount || !type) {
      return res.status(400).json({ error: "Missing required fields" });
    }

    await db.run(
      "INSERT INTO entries (user, date, description, amount, type) VALUES (?, ?, ?, ?, ?)",
      [user, date, description, amount, type]
    );
    res.json({ status: "ok" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Failed to save entry" });
  }
});

// --- Start server ---
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});


>>>>>>> origin/main
