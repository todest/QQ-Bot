#!/bin/bash
cd $(cd "$(dirname "$0")"; pwd)
while getopts "rkut:g:" opt
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

# 进程升级
if [ $bot_upgrade ]; then
    git pull
    if [ $? -ne 0 ]; then
        args="$args --upgrade=false"
    else
        args="$args --upgrade=true"
    fi
fi

killall python3 -u todest

# 进程退出失败
if [ $? -ne 0 ]; then
    args="$args --kill"
fi

# 来自群组
if [ $bot_group ]; then
    args="$args --group=$bot_group"
fi

# 进程退出
if [ $bot_shutdown ]; then
    exit
fi

# 进程重启
if [ $bot_reboot ]; then
    args="$args --reboot"
fi

nohup python3 main.py $args > nohup.out 2>&1 &
