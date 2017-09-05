@echo off

----------
wmic baseboard get Model,Product,Manufacturer,version,serialnumber /value | findstr "="
OK
____________



------------
wmic os get osarchitecture,Caption,FreePhysicalMemory /value | findstr "="
OK
---------------

--------------
wmic csproduct get Name,identifyingnumber,UUID /value | findstr "="
OK
-------------


-------------
wmic cpu get Name,loadPercentage /value | findstr "="
OK
----------------

--------------------------------------------------------------------------------------
-------
wmic computersystbem get username,TotalPhysicalMemory,NumberOfProcessors,NumberOfLogicalProcessors /value | findstr "="
ok
---------

echo hostname=%COMPUTERNAME% | findstr "hostname"
