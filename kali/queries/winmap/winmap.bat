@echo off

wmic baseboard get Model,Product,Manufacturer,version,serialnumber /value | findstr "="

wmic os get osarchitecture,Caption,FreePhysicalMemory /value | findstr "="

wmic csproduct get Name,identifyingnumber,UUID /value | findstr "="

wmic cpu get Name,loadPercentage /value | findstr "="

wmic computersystem get username,TotalPhysicalMemory,NumberOfProcessors,NumberOfLogicalProcessors /value | findstr "="

echo hostname=%COMPUTERNAME% | findstr "hostname"
