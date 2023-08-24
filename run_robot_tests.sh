#!/bin/bash

#start jupyter notebook and save output into "noteout"
poetry run jupyter notebook --no-browser &> noteout &
R2D2=$!     #Get jupyter process id

#Wait for notebook to start
while :
    do
        echo "Waiting notebook to start...."
        sleep 1;
        running=$(cat noteout) 2> /dev/null
        if  [ -n "$running" ]
        then
            break
        fi
    done

sleep 2

#extract notebook address token
httptoken=$(cat noteout |grep -Eo -m 1 "http://127.0.0.1:[0-9]{4}/[?]token[=]{1}[0-9, a-f]{48}")
echo 'URL='$httptoken > .env

#run robot tests
echo "Executing robot tests..."
#poetry run robot --variable URL:$httptoken tests
poetry run npx playwright test

#terminate test notebook process
kill -15 $R2D2

#remove files created by robottests
if [ -f './Untitled.ipynb' ];
  then
    echo "Test files removed:"
    ls -1 ./Untitled*.ipynb
    
    rm ./Untitled*.ipynb
  else
    echo "No Untitled.ipynb files found."
fi

#remove slides
rm ./*.pptx


#remove noteout
rm noteout

