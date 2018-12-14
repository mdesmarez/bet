const puppeteer = require('puppeteer');
const fs = require('fs');

const chrome = { x: 0, y: 74 };   // comes from config in reality
const width = 1200;
const height = 960;

const invisible_nav = true

var args = process.argv.slice(2);
console.log(args[0])
console.log(args[1])

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
    await page.goto("https://www.ps3838.com/en/euro/sports/soccer");    
    await page.waitFor(1 * 2000);
    await fs.writeFileSync('../dataset/local/single_soccer.html', await page.evaluate(() => document.body.innerHTML));
    await page.waitFor(1 * 1000);

    await page.goto("https://www.ps3838.com/en/euro/sports/tennis");    
    await page.waitFor(1 * 2000);
    await fs.writeFileSync('../dataset/local/single_tennis.html', await page.evaluate(() => document.body.innerHTML));
    await page.waitFor(1 * 1000);

    await page.goto("https://www.ps3838.com/en/euro/sports/basketball");    
    await page.waitFor(1 * 2000);
    await fs.writeFileSync('../dataset/local/single_basketball.html', await page.evaluate(() => document.body.innerHTML));
    await page.waitFor(1 * 1000);

    await page.goto("https://www.ps3838.com/en/euro/sports/football");    
    await page.waitFor(1 * 2000);
    await fs.writeFileSync('../dataset/local/single_football.html', await page.evaluate(() => document.body.innerHTML));
    await page.waitFor(1 * 1000);

    await page.goto("https://www.ps3838.com/en/euro/sports/baseball");    
    await page.waitFor(1 * 2000);
    await fs.writeFileSync('../dataset/local/single_baseball.html', await page.evaluate(() => document.body.innerHTML));
    await page.waitFor(1 * 1000);

    await page.goto("https://www.ps3838.com/en/euro/sports/golf");    
    await page.waitFor(1 * 2000);
    await fs.writeFileSync('../dataset/local/single_golf.html', await page.evaluate(() => document.body.innerHTML));
    await page.waitFor(1 * 1000);


    await page.goto("https://www.ps3838.com/en/euro/sports/hockey");    
    await page.waitFor(1 * 2000);
    await fs.writeFileSync('../dataset/local/single_hockey.html', await page.evaluate(() => document.body.innerHTML));
    await page.waitFor(1 * 1000);

    await page.goto("https://www.ps3838.com/en/euro/sports/volleyball");    
    await page.waitFor(1 * 2000);
    await fs.writeFileSync('../dataset/local/single_volleyball.html', await page.evaluate(() => document.body.innerHTML));
    await page.waitFor(1 * 1000);

    await page.goto("https://www.ps3838.com/en/euro/sports/mixed-martial-arts");    
    await page.waitFor(1 * 2000);
    await fs.writeFileSync('../dataset/local/single_mixed-martial-arts.html', await page.evaluate(() => document.body.innerHTML));
    await page.waitFor(1 * 1000);

    await page.goto("https://www.ps3838.com/en/euro/sports/handball");    
    await page.waitFor(1 * 2000);
    await fs.writeFileSync('../dataset/local/single_handball.html', await page.evaluate(() => document.body.innerHTML));
    await page.waitFor(1 * 1000);

    await page.goto("https://www.ps3838.com/en/euro/sports/e-sports");    
    await page.waitFor(1 * 2000);
    await fs.writeFileSync('../dataset/local/single_e-sports.html', await page.evaluate(() => document.body.innerHTML));
    await page.waitFor(1 * 1000);

    await page.goto("https://www.ps3838.com/en/euro/sports/cricket");    
    await page.waitFor(1 * 2000);
    await fs.writeFileSync('../dataset/local/single_cricket.html', await page.evaluate(() => document.body.innerHTML));
    await page.waitFor(1 * 1000);

    await page.goto("https://www.ps3838.com/en/euro/sports/bandy");    
    await page.waitFor(1 * 2000);
    await fs.writeFileSync('../dataset/local/single_bandy.html', await page.evaluate(() => document.body.innerHTML));
    await page.waitFor(1 * 1000);

    await page.goto("https://www.ps3838.com/en/euro/sports/boxing");    
    await page.waitFor(1 * 2000);
    await fs.writeFileSync('../dataset/local/single_boxing.html', await page.evaluate(() => document.body.innerHTML));
    await page.waitFor(1 * 1000);

    await page.goto("https://www.ps3838.com/en/euro/sports/snooker");    
    await page.waitFor(1 * 2000);
    await fs.writeFileSync('../dataset/local/single_snooker.html', await page.evaluate(() => document.body.innerHTML));
    await page.waitFor(1 * 1000);

    await page.goto("https://www.ps3838.com/en/euro/sports/alpine-skiing");    
    await page.waitFor(1 * 2000);
    await fs.writeFileSync('../dataset/local/single_alpine-skiing.html', await page.evaluate(() => document.body.innerHTML));
    await page.waitFor(1 * 1000);

    await page.goto("https://www.ps3838.com/en/euro/sports/cross-country");    
    await page.waitFor(1 * 2000);
    await fs.writeFileSync('../dataset/local/single_cross-country.html', await page.evaluate(() => document.body.innerHTML));
    await page.waitFor(1 * 1000);


    // close browser
    browser.close();

    }


Oddsportal_scrap(invisible_nav);