var express = require("express");
var router = express.Router();
let { getResults, getCategories } = require("../utils/algorithm");
let debug = require("debug")("server-express:index");

/* GET home page. */
router.get("/:id", function(req, res, next) {
  const articles = getResults();
  let categories = getCategories();
  //   debug(categories.length)
  res.render("category", {
    title: categories[req.params.id],
    categories,
    articles
  });
});

module.exports = router;
