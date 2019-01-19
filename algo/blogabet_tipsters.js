const puppeteer = require('puppeteer');
const fs = require('fs');

const chrome = { x: 0, y: 74 };   // comes from config in reality
const width = 1200;
const height = 960;

const invisible_nav = false

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
    await page.setViewport({ width: 1900, height: 1000});

    process.on("unhandledRejection", (reason, p) => {
        console.error("Unhandled Rejection at: Promise", p, "reason:", reason);
        browser.close();
        });

    async function autoScroll(page){
        await page.evaluate(async () => {
            await new Promise((resolve, reject) => {
                var totalHeight = 0;
                var distance = 100;
                var timer = setInterval(() => {
                    var scrollHeight = document.body.scrollHeight;
                    window.scrollBy(0, distance);
                    totalHeight += distance;
    
                    if(totalHeight >= scrollHeight){
                        clearInterval(timer);
                        resolve();
                    }
                }, 100);
            });
        });
    }

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
    await page.goto('https://blogabet.com/tipsters', {timeout : 0});    
    var selector = '#page-content > div > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(3) > div > div > div > button'
    await page.waitForSelector(selector)
    
    // FOOTBALL
    clickByXPATH(page, '//*[@id="page-content"]/div/div[1]/div/div[2]/div[3]/div/div/div/button');
    await page.waitFor(1 * 500);
    await page.keyboard.type('Football');
    await page.waitFor(1 * 500);
    clickByXPATH(page, '//*[@id="page-content"]/div/div[1]/div/div[2]/div[3]/div/div/div/div/ul/li[26]/a');
    var selector = '#_marketResults > div:nth-child(2) > div.tipster-info.col-lg-10.no-padding > div.col-md-12.col-lg-5.no-padding > div.col-xs-12.col-lg-4.col-xlg-3.text-center.no-padding.avatar > a > img'
    await page.waitForSelector(selector, {timeout : 20000})
    await page.waitFor(1 * 500);

    // MORE 1000
    clickByXPATH(page, '//*[@id="page-content"]/div/div[1]/div/div[2]/div[6]/div/div/div/button');
    await page.waitFor(1 * 500);
    await page.keyboard.press('ArrowUp');
    await page.waitFor(1 * 500);
    await page.keyboard.press('Enter');
    var selector = '#_marketResults > div:nth-child(2) > div.tipster-info.col-lg-10.no-padding > div.col-md-12.col-lg-5.no-padding > div.col-xs-12.col-lg-4.col-xlg-3.text-center.no-padding.avatar > a > img'
    await page.waitForSelector(selector, {timeout : 20000})
    await page.waitFor(1 * 500);
    
    // PRE MATCH
    clickByXPATH(page, '//*[@id="page-content"]/div/div[1]/div/div[2]/div[2]/div/div/div/button');
    await page.waitFor(1 * 500);
    clickByXPATH(page, '//*[@id="page-content"]/div/div[1]/div/div[2]/div[2]/div/div/div/div/ul/li[2]/a');
    await page.waitFor(1 * 500);
    var selector = '#_marketResults > div:nth-child(2) > div.tipster-info.col-lg-10.no-padding > div.col-md-12.col-lg-5.no-padding > div.col-xs-12.col-lg-4.col-xlg-3.text-center.no-padding.avatar > a > img'
    await page.waitForSelector(selector, {timeout : 20000})
    await page.waitFor(1 * 500);
    
    // ACTIVE
    clickByXPATH(page, '//*[@id="page-content"]/div/div[1]/div/div[2]/div[7]/div/div/div/button');
    await page.waitFor(1 * 500);
    clickByXPATH(page, '//*[@id="page-content"]/div/div[1]/div/div[2]/div[7]/div/div/div/div/ul/li[1]/a');
    await page.waitFor(1 * 500);
    var selector = '#_marketResults > div:nth-child(2) > div.tipster-info.col-lg-10.no-padding > div.col-md-12.col-lg-5.no-padding > div.col-xs-12.col-lg-4.col-xlg-3.text-center.no-padding.avatar > a > img'
    await page.waitForSelector(selector, {timeout : 20000})
    await page.waitFor(1 * 500);
    

    
    for (let index = 0; index < 10; index++) {
        await autoScroll(page);
        clickByXPATH(page, '//*[@id="_loadMore"]/a');
        await page.waitFor(1 * 10000);
        await fs.writeFileSync('../dataset/local/blogabet_menu.html', await page.evaluate(() => document.body.innerHTML));
    }
    



    // close browser
    browser.close();
    

    }


Oddsportal_scrap(invisible_nav);