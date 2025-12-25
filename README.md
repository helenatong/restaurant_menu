# Packages

## Create venv in Powershell
py -m venv .venv 

## Install packages
pip install -r requirements.txt

## Update packages
pip freeze > requirements.txt

# Launch app
## Command line
streamlit run app.py