var express = require("express");
var router = express.Router();
let { getResults, getCategories } = require("../utils/algorithm");
let debug = require("debug")("server-express:index");

/* GET home page. */
router.get("/:id", function(req, res, next) {
  const articles = getResults()[req.params.id];
  let categories = getCategories();
  console.log(JSON.stringify(articles));
  //   debug(categories.length)
  res.render("category", {
    title: categories[req.params.id],
    categories,
    articles,
    articlesStr: JSON.stringify(articles)
  });
});

module.exports = router;
