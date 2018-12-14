const puppeteer = require('puppeteer');
const fs = require('fs');

const chrome = { x: 0, y: 74 };   // comes from config in reality
const width = 1200;
const height = 960;

const invisible_nav = false

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
    await page.goto('https://www.ps3838.com/en/euro/sports/mix-parlay');    
    await page.waitFor(1 * 4000);
    
    
    // LOG SECTION
    clickByXPATH(page, '//*[@id="login-panel"]/form/div[1]/input');
    await page.waitFor(1 * 400);
    await page.keyboard.type('AC88000IN1');
    await page.waitFor(1 * 400);
    await page.keyboard.press('Tab');    
    await page.waitFor(1 * 400);
    await page.keyboard.type('1A!FeXiSmLc!A1');
    await page.waitFor(1 * 400);
    await page.keyboard.press('Tab');
    await page.waitFor(1 * 400);
    await page.keyboard.press('Enter');
    await page.waitFor(1 * 3000);
    await page.goto('https://www.ps3838.com/en/euro/sports/mix-parlay');    
    await page.waitFor(1 * 1000);
    
    // 
    var list_bet = args[0].split(",") //[["soccer","918043169|0|1|0|0|0"]];
    console.log(list_bet);
    var list_sport = args[1].split(",") //[["soccer","918043169|0|1|0|0|0"]];
    console.log(list_sport);


    async function select_sport(sport) {
        for (let i = 1; i <= 7; i++) {
            const click_page = '#sportFilter > td > ul > li:nth-child('+i.toString()+') > a';
            await page.click(click_page);
            await page.waitFor(1 * 300);
            const textContent = await page.evaluate(() => document.querySelector('#sportFilter > td > ul > li.selected > a').innerText);
            await page.waitFor(1 * 300);
            if (textContent == sport) {
                console.log("YOUHOUHOUHOUHOHUHOUHOHUHOU");
                console.log(sport);
                return 'ee';
            }
                                      }
        for (let i = 2; i <= 20; i++) {
            const click_page = '#sportFilter > td > ul > li:nth-child('+i.toString()+') > a';
            await page.click(click_page);
            await page.waitFor(1 * 300);
            const textContent = await page.evaluate(() => document.querySelector('#sportFilter > td > ul > li.selected > a').innerText);
            if (textContent == sport) {
                console.log("YOUHOUHOUHOUHOHUHOUHOHUHOU");
                console.log(sport);         
                return 'ee';
                                    }
    }
};


    

    //
    let item_number = 0
    await asyncForEach(list_bet, async (element) => {
        const sport = list_sport[item_number].trim();
        console.log(sport);
        item_number = item_number + 1;
        await waitFor(300);
        await select_sport(sport)
        await waitFor(300);
        const bet_id = '//*[@id="' + element + '"]'
        console.log(bet_id);
        clickByXPATH(page, bet_id);
      });
      console.log('Done');

    //
    await page.waitFor(1 * 60000);



    /*
    // close browser
    browser.close();
    */

    }


Oddsportal_scrap(invisible_nav);