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
        args: ['--start-maximized'],
        timeout: 0
    });

    
    const page = await browser.newPage(timeout=0);
    await page.setViewport({ width: 1920, height: 1080});

    process.on("unhandledRejection", (reason, p) => {
        console.error("Unhandled Rejection at: Promise", p, "reason:", reason);
        browser.close();
        });


    const clickByXPATH = async (page, Xtext) => {
        try {
            const linkHand = await page.$x(Xtext);
            //await page.waitFor(1 * parseInt(Math.random()*10000));
            if (linkHand.length > 0) {
                                    await linkHand[0].click();
                                    } 
            else                    {
                                    //throw new Error("Link not found");
                                    console.log(Xtext);
                                    console.log("Link not found");
                                    }
            }
        catch(err) {
            console.log("Link not found");
            }
        
    };

    
    const waitFor = (ms) => new Promise(r => setTimeout(r, ms));
    
    async function asyncForEach(array, callback) {
        for (let index = 0; index < array.length; index++) {
          await callback(array[index], index, array);
        }
      }


    // GO TO PAGE
    await page.goto('https://www.ps3838.com/en/euro/account/results');    
    await page.waitFor(1 * 3000);
    
    // 
    var list_sport = args[0].split(",");
    console.log(list_sport);


    async function asyncForEach(array, callback) {
        for (let index = 0; index < array.length; index++) {
          await callback(array[index], index, array);
        }
      }

    //
    await asyncForEach(list_sport, async (sport) => {
        console.log(sport)
        await page.click('#btn-today')
        await waitFor(500);
        await page.click('#selSports')
        await waitFor(500);
        await page.keyboard.type(sport);
        await waitFor(500);
        await page.click('#body > div.contain-wrapper.noMenu > div > form > div:nth-child(4) > button');
        await waitFor(500);
        await fs.writeFileSync('../dataset/local/result_mix_parlay_'+sport+'.html', await page.evaluate(() => document.body.innerHTML));       
        await waitFor(500);
        await page.click('#btn-yesterday')
        await waitFor(500);
        await fs.writeFileSync('../dataset/local/result_mix_parlay_'+sport+'_yesterday.html', await page.evaluate(() => document.body.innerHTML));       
        await waitFor(500);
        });
        console.log('Done');


    // close browser
    browser.close();

    }


Oddsportal_scrap(invisible_nav);