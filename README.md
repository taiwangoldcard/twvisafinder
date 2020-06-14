# twvisafinder
Taiwan Visa Finder - a site to demystify potential visa options for Taiwan

## Pre-requis
```
# Install Python3 on Mac
brew install python3
```

## Setup
```
# Install all dependencies
pip3 install requirements.txt

# DB init
python3 manage.py makemigrations && python3 manage.py migrate
```

ps: You'll likely want to run this in a virtualenv

## Run
```
python3 manage.py runserver

# Then head to http://127.0.0.1:8000 
```
