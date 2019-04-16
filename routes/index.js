var express = require('express');
var router = express.Router();
let {
  getResults,
  getCategories
} = require('../utils/algorithm');
let debug = require("debug")("server-express:index");

/* GET home page. */
router.get('/', function (req, res, next) {
  const articles = getResults();
  let categories = getCategories();
  debug(categories.length)
  res.render('index', {
    title: 'Categorized articles',
    categories,
    articles: articles
  });
});

module.exports = router;