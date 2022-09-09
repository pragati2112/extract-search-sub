# extract-search-sub
In this project, video(s) can be uploaded, processed in some manner (in the background) and searched using the subtitles in that video as keywords.

## Technology used
FastApi (Python framework)

Vuejs (Front-end)

DynamoDB (Database)



## Prerequisites
Download ccextractor (sudo apt install ccextractor) for linux users, Thats it!

Pull docker image of amazon/dynamodb-local 

mkvirtualenv venv

pip install -r requirements.txt


## How to run it

python main.py

Server will be running on localhost:8002

To check and try apis hit- http://localhost:8002/docs (This is fastapi provided openapi.json)
