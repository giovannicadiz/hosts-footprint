#!/bin/bash

cd /queries/winmap

while :; do 
    ./wmi_to_es.py
    sleep 60
done
