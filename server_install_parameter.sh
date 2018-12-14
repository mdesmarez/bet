###########################################
GIT_NAME="bet" 
PYTHON_NAME1="PS3838_scrap_parlay_schedule.py"
PYTHON_NAME2=""
PYTHON_NAME3=""
### without nohup
PYTHON_NAME4=""
PYTHON_NAME5=""


function install_additional(){
### SPECIFIC SECTION MORE THAN GITFILE
sudo apt-get install libmagickwand-dev
sudo apt-get install -y tzdata
echo 'Import Spacy Model French'
python -m spacy download fr
}

