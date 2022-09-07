# extract-search-sub
In this project, video(s) can be uploaded, processed in some manner (in the background) and searched using the subtitles in that video as keywords.

## Technology used
FastApi (Python framework)

Vuejs (Front-end)

DynamoDB (Database)



## Prerequisites
Download ccextractor (sudo apt install ccextractor) for linux users, Thats it!

Pull docker image of amazon/dynamodb-local 

## How to run it

pip install -r requirements.txt

uvicorn main:app
