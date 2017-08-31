#!/bin/bash

cd /hostfootprint
LOG=/tmp/loopint.txt

while :; do
    echo "starting looping: $(date)" >> $LOG
    for i in `echo "$COUNTRIES"`; do
	echo "$i: $(date)" >> $LOG
	./manage.py nmap_subnets -c "$i" &
	sleep 10
    done

    while ps -ef | grep -v grep | grep nmap_subnets; do
	echo "running...."
	sleep 30
    done
    echo "ciclo Ok: $(date)" >> $LOG
    sleep 360
done
