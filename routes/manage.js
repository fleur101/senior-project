var express = require("express");
var { getCategories, writeCategories, runCode } = require("../utils/algorithm");
var router = express.Router();

/* GET users listing. */
router.get("/", function(req, res, next) {
  let categories = getCategories();
  res.render("manage", {
    categories: categories.join("\n")
  });
});

router.post("/", function(req, res, next) {
  let categories = req.body.categories
    .split("\r\n")
    .map(item => item.trim())
    .filter(val => val);
  writeCategories(categories);
  runCode();
  res.redirect("/");
});

module.exports = router;
