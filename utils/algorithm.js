const fs = require('fs');
const path = require('path');
let debug = require("debug")("server-express:algorithm");
var execSync = require('child_process').execSync;

const RESULTS_PATH = path.join(__dirname, '../data/categorizedArticles.json');
const CATEGORIES_PATH = path.join(__dirname, '../data/userCategories.json');

function getResults() {
  return JSON.parse(fs.readFileSync(RESULTS_PATH, 'utf8'));
}

function getCategories() {
  return JSON.parse(fs.readFileSync(CATEGORIES_PATH, 'utf8'));
}

function runCode() {
  debug("starting execution");
  execSync('cd ' + __dirname + '/../python && python algorithm.py');
  debug("executed");
}

function writeCategories(categories) {
  fs.writeFileSync(CATEGORIES_PATH, JSON.stringify(categories));
}

module.exports = {
  getResults,
  getCategories,
  writeCategories,
  runCode
}