const express = require("express");
const { exec } = require("child_process");
const jwt = require("jsonwebtoken");
const app = express();
const API_KEY = "demo-not-a-real-key-0123456789";

app.get("/search", (req, res) => {
  db.collection("users").find(req.query).toArray((e, r) => res.json(r));
});
app.get("/greet", (req, res) => {
  document.getElementById("out").innerHTML = req.query.name;
  res.send("ok");
});
app.get("/zip", (req, res) => {
  exec("zip -r out.zip " + req.query.dir, () => res.send("done"));
});
app.get("/calc", (req, res) => res.send(String(eval(req.query.expr))));
app.get("/file", (req, res) => res.send(require("fs").readFileSync("./uploads/" + req.query.name)));
app.use(require("cors")({ origin: "*" }));
const claims = jwt.decode(token, { algorithms: ["none"] });
