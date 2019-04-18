var express = require("express");
var router = express.Router();
let { getResults, getCategories } = require("../utils/algorithm");
let debug = require("debug")("server-express:index");

/* GET home page. */
router.get("/:id", function(req, res, next) {
  //   const articles = getResults();
  //   let categories = getCategories();
  //   debug(categories.length)
  res.render("category", {
    title: "Politics",
    categories: ["politics", "sport", "business", "academia"],
    articles: [
      {
        id: 0,
        title: "Presidential race in Ukraine went far",
        category: "politics",
        categories: [80, 20, 50, 10]
      },
      {
        id: 1,
        title: "Kazakhstan spends 100000000 dollars on new name",
        category: "politics",
        categories: [70, 10, 60, 10]
      },
      {
        id: 2,
        title: "Russia is good at hockey politics",
        category: "politics",
        categories: [80, 70, 30, 20]
      }
    ]
  });
});

module.exports = router;
