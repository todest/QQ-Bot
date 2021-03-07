#!/bin/bash
cd $(cd "$(dirname "$0")"; pwd)
while getopts "rku:g:t:" opt
do
    case $opt in
        t) bot_target=$OPTARG ;;
        r) bot_reboot=true ;;
        u) bot_upgrade=true ;;
        k) bot_shutdown=true ;;
        g) bot_group=$OPTARG ;;
    esac
done

args="--target=$bot_target"

killall python3 -u todest

if [ $? -ne 0 ]; then
    args="$args --kill"
fi

if [ $bot_shutdown ]; then
    exit
fi

if [ $bot_reboot ]; then
    args="$args --reboot"
fi

if [ $bot_upgrade ]; then
    git pull
    if [ $? -ne 0 ]; then
        args="$args --upgrade=false"
    else
        args="$args --upgrade=true"
    fi
fi

if [ $bot_group ]; then
    args="$args --group=$bot_group"
fi

nohup python3 main.py $args &
