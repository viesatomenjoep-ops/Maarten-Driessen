const fs = require('fs');
const { JSDOM } = require('jsdom');
const html = fs.readFileSync('index.html', 'utf8');
const dom = new JSDOM(html, { runScripts: "dangerously" });
if (dom.window.document.errors) {
    console.log("Errors:", dom.window.document.errors);
}
console.log("If this works, no major errors in parsing.");
