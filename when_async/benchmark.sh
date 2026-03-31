#!/bin/bash

# threads → number of OS threads
# csw → context switches (key for scheduler overhead)
# cpu → CPU usage
# mem → memory
# top -pid 12345 -stats pid,command,cpu,threads,time,mem,csw

echo "*********************************************************    threading:"
# launch the command in the background
python mem_threading.py &
# store its PID  in a variable
APP_PID=$!
# wait a bit
sleep 2
# check stats
while kill -0 "$APP_PID" 2>/dev/null; do
    top -pid "$APP_PID" -l 1 -stats pid,threads,mem,csw,cpu >> log_threading.txt
    sleep 1
done
#top -pid $APP_PID -stats pid,command,cpu,threads,time,mem,csw
# wait for process to finish
wait "$APP_PID"

echo "*********************************************************    asyncio:"
# launch the command in the background
python mem_asyncio.py &
# store its PID  in a variable
APP_PID=$!
# wait a bit
sleep 2
# check stats
while kill -0 "$APP_PID" 2>/dev/null; do
    top -pid "$APP_PID" -l 1 -stats pid,threads,mem,csw,cpu >> log_async.txt
    sleep 1
done
#top -pid $APP_PID -stats pid,command,cpu,threads,time,mem,csw
# wait for process to finish
wait "$APP_PID"

