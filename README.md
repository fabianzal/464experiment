# 464experiment

{"method":"calendar","value":"1998-04-21","timeTaken":1023.44,"error":false,"timestamp":"2025-10-22T02:15:12.000Z"}
{"method":"manual","value":"2020-10-10","timeTaken":589.22,"error":false,"timestamp":"2025-10-22T02:15:45.000Z"}


const express = require("express");
const cors = require("cors");
const fs = require("fs");
const app = express();
const port = 5000;

app.use(cors());
app.use(express.json());

// Receive experiment results
app.post("/api/log", (req, res) => {
  const entry = { ...req.body, timestamp: new Date().toISOString() };
  console.log(entry);
  fs.appendFileSync("results.json", JSON.stringify(entry) + "\n");
  res.json({ status: "ok" });
});

app.listen(port, () => console.log(`Backend running on http://localhost:${port}`));



running frontend command: python -m http.server 8000
running backend command: uvicorn main:app --reload --port 5000
in browser: http://localhost:8000/

