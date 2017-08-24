#!/bin/sh

LUSER="$1"
LHOST="$2"
LDOMAIN="$3"

get_so(){
    echo "Caption=Windows XP"
    echo "OSArchitecture=32-bit"
}

get_user() {
    USERID_WIN=`wmic  -U "$LUSER" //$LHOST "SELECT LogonId FROM Win32_LogonSession WHERE LogonType = 2 or LogonType = 10" | tail -n1`
    if [ "$?" = "0" ]; then
	USERCAPTION=`wmic  -U "$LUSER" //$LHOST "Associators Of {Win32_LogonSession.LogonId=$USERID_WIN} WHERE AssocClass=Win32_LoggedOnUser Role=Dependent"| awk -F "|" '{ print $2}' | tail -n1`
	if echo "$USERCAPTION" | grep -q "$LDOMAIN" ; then 
	    header_user=$(printf '%s\n' "UserName")            
	    value_user=$(printf '%s\n' "$USERCAPTION")
	fi
    fi
}

get_cs(){
    w32_cs=$(wmic -U "$LUSER" //$LHOST "SELECT Manufacturer,Model,NumberOfLogicalProcessors,NumberOfProcessors,TotalPhysicalMemory,Caption FROM Win32_ComputerSystem" | grep "|")
    header_cs=$(echo "$w32_cs" | head -n1)
    value_cs=$(echo "$w32_cs" | tail -n1)
}

get_csp(){
    w32_csp=$(wmic -U "$LUSER" //$LHOST "SELECT IdentifyingNumber,Name,Version FROM Win32_ComputerSystemProduct" | grep "|")
    header_csp=$(echo "$w32_csp" | head -n1)
    value_csp=$(echo "$w32_csp" | tail -n1)

}

## mac address y IP
#wmic -U "$LUSER" //$LHOST "SELECT * FROM Win32_NetworkAdapterSetting"
##wmic -U "$LUSER" //$LHOST "SELECT * FROM Win32_NetworkAdapterConfiguration"
#echo "----------------"
##wmic -U "$LUSER" //$LHOST "SELECT * FROM Win32_NetworkAdapter"
##wmic -U "$LUSER" //$LHOST "SELECT * FROM Win32_Printer"

get_user;
get_cs;
get_csp;

echo "$header_user|$header_cs|$header_csp"
echo "$value_user|$value_cs|$value_csp"
#get_so;
