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

#run robot tests
echo "Executing robot tests..."
poetry run robot --variable URL:$httptoken tests

#terminate test notebook process
kill -15 $R2D2

#remove noteout
rm noteout
