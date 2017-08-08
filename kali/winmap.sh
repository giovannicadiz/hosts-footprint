#!/bin/bash

cd /queries/winmap

while :; do 
    ./winmap_to_es.py "$1" DOMINIO
    sleep 360
done
