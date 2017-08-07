#!/bin/bash
smbclient -t "$3" -U "$1" "//$2/c$" 2>&1 <<EOF
 mkdir Temp
 cd Temp
 put winmap.bat
EOF
