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
  console.log(req.body);
  let categories = req.body.categories
    .map(item => item.trim())
    .filter(val => val);
  writeCategories(categories);
  runCode();
  res.redirect("/");
});

module.exports = router;
