const puppeteer = require('puppeteer');
const fs = require('fs');

const chrome = { x: 0, y: 74 };   // comes from config in reality
const width = 1200;
const height = 960;

const invisible_nav = false

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





    // GO TO SEASON
    for (year_i = 2013; year_i < 2018; year_i++) { 
        var season = year_i + '-' + (parseInt(year_i) + 1);

        for (i = 1; i < 35; i++) { 
            console.log(season + ' / ' + i);
            const browser = await puppeteer.launch({
                headless: invisible_nav,
                timeout: 0
            });
        
            const page = await browser.newPage(timeout=0);
            //process.on("unhandledRejection", (reason, p) => {
            //    console.error("Unhandled Rejection at: Promise", p, "reason:", reason);
            //    browser.close();
            //    });
            //await page.waitFor(1 * 300);    
            page.goto('http://www.oddsportal.com/hockey/usa/nhl-' + season + '/results/#/page/' + i);    
            await page.waitForSelector('#logo-box > p > a > img');
            await page.waitFor(1 * 2000);
            await fs.writeFileSync('../dataset/local/Oddsportal/oddsportal_' + season + '_' + i + '.html', await page.evaluate(() => document.body.innerHTML));
            await page.waitFor(1 * 100);    
            await browser.close();
        }
    }

    


    // close browser
    browser.close();


    }


Oddsportal_scrap(invisible_nav);