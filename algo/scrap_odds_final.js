const puppeteer = require('puppeteer');
const fs = require('fs');

const chrome = { x: 0, y: 74 };   // comes from config in reality
const width = 1200;
const height = 960;

const invisible_nav = true

var args = process.argv.slice(2);
console.log(args[0])

/*************************************************************************** */
/* Functions                                                                 */
/*************************************************************************** */


/*************************************************************************** */
/* Oddsportal                                                                */
/*************************************************************************** */
async function Oddsportal_scrap(invisible_nav) {
    var today = new Date();
    var day   = today.getDate().toString();
    var month = (today.getMonth()+1).toString();
    var year  = today.getFullYear().toString();
    const date_today = day + '_' + month + '_' + year;


    const browser = await puppeteer.launch({
        headless: invisible_nav,
        timeout: 0
    });

    const page = await browser.newPage(timeout=0);
    process.on("unhandledRejection", (reason, p) => {
        console.error("Unhandled Rejection at: Promise", p, "reason:", reason);
        browser.close();
        });


    // GO TO PAGE
    await page.goto(args[0]);    
    await fs.writeFileSync('/home/mathieu/Ascent/hockey/dataset/odds/last/' + args[1] + '.html', await page.evaluate(() => document.body.innerHTML));

    // close browser
    browser.close();

    }


Oddsportal_scrap(invisible_nav);