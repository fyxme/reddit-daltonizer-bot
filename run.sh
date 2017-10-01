#!/usr/bin/env bash

# if [ $# -e 1 && "$1" == "stop" ] || [ -e '/tmp/daltonizer.pid' && ps -p `cat /tmp/daltonizer.pid` ]; then
#     # kill if already running or stop command issued
#     echo "Killing old bot"
#     kill -9 `cat /tmp/daltonizer.pid`
# elif [ $# -e 1 && "$1" == "status" ]; then
#     if [ -e /tmp/daltonizer.pid && ps -p `cat /tmp/daltonizer.pid` ]; then
#         echo "Bot is running."
#     else
#         echo "Bot is not running"
#     fi
# fi

echo "Attempting to kill old bot"
kill -9 `cat /tmp/daltonizer.pid`

echo "Starting new bot"
# if no command issued, run the program
echo $$ > /tmp/daltonizer.pid
nohup python /root/daltonizer/bot.py </dev/null >/tmp/daltonizer.error 2>&1 &
