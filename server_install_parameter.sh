###########################################
GIT_NAME="bet" 
PYTHON_NAME1="PS3838_scrap_parlay_schedule.py"
PYTHON_NAME2=""
PYTHON_NAME3=""
### without nohup
PYTHON_NAME4="PS3838_main.py"
PYTHON_NAME5="PS3838_analysis.py"


function install_additional(){
### SPECIFIC SECTION MORE THAN GITFILE
##sudo apt-get install libmagickwand-dev
sudo apt-get install gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget
sudo apt-get install python-tk
curl -sL https://deb.nodesource.com/setup_8.x | sudo bash -
sudo apt install nodejs
npm i puppeteer
}

