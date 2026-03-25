#!/bin/bash

echo "*********************************************************    green threads:"
# launch the command in the background
python green_threads.py &
# store its PID  in a variable
APP_PID=$!
# wait a bit
sleep 2
# check threads of process with given PID 
echo "---------------------------------------"
ps -M $APP_PID
echo "---------------------------------------"
# wait for process to finish
wait "$APP_PID"
echo "*********************************************************    os threads:"
# launch the command in the background
python os_threads.py &
# store its PID  in a variable
APP_PID=$!
# wait a bit
sleep 2
# check threads of process with given PID 
echo "---------------------------------------"
ps -M $APP_PID
echo "---------------------------------------"
# wait for process to finish
wait "$APP_PID"
