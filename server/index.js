const express = require('express');
const app = express();
const port = 3001;
const { exec } = require("child_process");

// Middleware to parse JSON request bodies
app.use(express.json());

// Basic health check
app.get('/', (req, res) => {
  res.send('Trading Agent API is running!');
});

// Endpoint to analyze a stock
app.post("/analyze", (req, res) => {
  const symbol = req.body.symbol || "NVDA";
  const date = req.body.date || "2024-05-10";

  exec(`python ../main.py ${symbol} ${date}`, (error, stdout, stderr) => {
    if (error) {
      return res.status(500).send(`Error: ${error.message}`);
    }
    if (stderr) {
      return res.status(500).send(`Stderr: ${stderr}`);
    }
    res.send(stdout);
  });
});

app.listen(port, () => {
  console.log(`Server is listening on http://localhost:${port}`);
});
