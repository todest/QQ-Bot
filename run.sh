#!/bin/bash
cd $(cd "$(dirname "$0")"; pwd)
while getopts ":e:u:k:g" opt
do
    case $opt in
    e)
        executor = $OPTARG
    ;;
    u)
        upgrade = true
    ;;
    k)
        shutdown = true
    ;;
    g)
        group = $OPTARG
    ;;
    esac
done

args = $executor

killall python3 -u todest
if [ $? -ne 0 ]; then
    args = '$args --kill'
fi

if $shutdown; then
    exit
fi

if $upgrade; then
    git pull
    if [ $? -ne 0 ]; then
        args = '$args --upgrade'
    fi
fi



if $group; then
    args = '$args --group $group'

nohup python3 main.py $args &
