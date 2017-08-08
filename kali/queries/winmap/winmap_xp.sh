#!/bin/sh

USERID_WIN=`wmic  -U "$1" //$2 "SELECT LogonId FROM Win32_LogonSession WHERE LogonType = 2 or LogonType = 10" | tail -n1`
if [ "$?" = "0" ]; then
    USERCAPTION=`wmic  -U "$1" //$2 "Associators Of {Win32_LogonSession.LogonId=$USERID_WIN} WHERE AssocClass=Win32_LoggedOnUser Role=Dependent"| awk -F "|" '{ print $2}' | tail -n1`
    if echo "$USERCAPTION" | grep -q "$3" ; then 
        echo "UserName=$USERCAPTION|Caption=Windows XP"
	exit 0
    fi
fi

echo 'False'
exit 2
