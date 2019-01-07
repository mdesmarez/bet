const puppeteer = require('puppeteer');
const fs = require('fs');

const chrome = { x: 0, y: 74 };   // comes from config in reality
const width = 1200;
const height = 960;

const invisible_nav = true

var args = process.argv.slice(2);
console.log(args[0])
console.log(args[1])
console.log(args[2])

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
    
    // 
    var list_bet = args[0].split(",") //[["soccer","918043169|0|1|0|0|0"]];
    console.log(list_bet);
    var list_sport = args[1].split(",") //[["soccer","918043169|0|1|0|0|0"]];
    console.log(list_sport);
    var list_money = args[2].split(",") //[["soccer","918043169|0|1|0|0|0"]];
    console.log(list_money);


    async function select_sport(sport) {
        if (sport == 'soccer') {
                            await page.goto("https://www.ps3838.com/en/euro/sports/soccer");    
                            await page.waitFor(1 * 2000);
                                }
        if (sport == 'tennis') {
                            await page.goto("https://www.ps3838.com/en/euro/sports/tennis");    
                            await page.waitFor(1 * 2000);
                                }
        if (sport == 'basketball') {
                            await page.goto("https://www.ps3838.com/en/euro/sports/basketball");    
                            await page.waitFor(1 * 2000);
                                }
        if (sport == 'football') {
                            await page.goto("https://www.ps3838.com/en/euro/sports/football");    
                            await page.waitFor(1 * 2000);
                                }
        if (sport == 'baseball') {
                            await page.goto("https://www.ps3838.com/en/euro/sports/baseball");    
                            await page.waitFor(1 * 2000);
                                }
        if (sport == 'golf') {
                            await page.goto("https://www.ps3838.com/en/euro/sports/golf");    
                            await page.waitFor(1 * 2000);
                                }
        if (sport == 'hockey') {
                            await page.goto("https://www.ps3838.com/en/euro/sports/hockey");    
                            await page.waitFor(1 * 2000);
                                }
        if (sport == 'volleyball') {
                            await page.goto("https://www.ps3838.com/en/euro/sports/volleyball");    
                            await page.waitFor(1 * 2000);
                                }
        if (sport == 'mixed martial arts') {
                            await page.goto("https://www.ps3838.com/en/euro/sports/mixed-martial-arts");    
                            await page.waitFor(1 * 2000);
                                }
        if (sport == 'handball') {
                            await page.goto("https://www.ps3838.com/en/euro/sports/handball");    
                            await page.waitFor(1 * 2000);
                                }
        if (sport == 'e sports') {
                            await page.goto("https://www.ps3838.com/en/euro/sports/e-sports");    
                            await page.waitFor(1 * 2000);
                                }
        if (sport == 'cricket') {
                            await page.goto("https://www.ps3838.com/en/euro/sports/cricket");    
                            await page.waitFor(1 * 2000);
                                }
        if (sport == 'bandy') {
                            await page.goto("https://www.ps3838.com/en/euro/sports/bandy");    
                            await page.waitFor(1 * 2000);
                                }
        if (sport == 'boxing') {
                            await page.goto("https://www.ps3838.com/en/euro/sports/boxing");    
                            await page.waitFor(1 * 2000);
                                }
        if (sport == 'snooker') {
                            await page.goto("https://www.ps3838.com/en/euro/sports/snooker");    
                            await page.waitFor(1 * 2000);
                                }
        if (sport == 'alpine skiing') {
                            await page.goto("https://www.ps3838.com/en/euro/sports/alpine-skiing");    
                            await page.waitFor(1 * 2000);
                                }
        if (sport == 'cross country') {
                            await page.goto("https://www.ps3838.com/en/euro/sports/cross-country");    
                            await page.waitFor(1 * 2000);
                                }

};




    

    //
    let item_number = 0
    await asyncForEach(list_bet, async (element) => {
        const sport = list_sport[item_number].trim();
        const money = list_money[item_number].trim();
        console.log(sport);
        item_number = item_number + 1;
        await waitFor(300);
        await select_sport(sport)
        await waitFor(300);
        const bet_id = '//*[@id="' + element + '"]'
        console.log(bet_id);
        clickByXPATH(page, bet_id);
        await waitFor(1000);
        clickByXPATH(page, '//*[@id="betslip-content"]/div/form/div[2]/div[7]/div/div[2]/input');
        await waitFor(1000);
        await page.keyboard.down( 'Control' );
        await page.keyboard.press( 'A' );
        await page.keyboard.up( 'Control' );
        await page.keyboard.press( 'Backspace' );
        await page.keyboard.type(money);
        await waitFor(1000);
        clickByXPATH(page, '//*[@id="betslip-content"]/div/form/div[7]/div/input');
        await waitFor(1500);
        //clickByXPATH(page, '//*[@id="euro-sports"]/div[4]/div[3]/div/button[1]/span');
        await waitFor(1000);
      });
      console.log('Done');


    //
    await page.waitFor(1 * 10000);

    // close browser
    browser.close();
    

    }


Oddsportal_scrap(invisible_nav);