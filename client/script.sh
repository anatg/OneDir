#!/bin/bash

echo $(whoami)
function create_directorys {
	mkdir "/home/OneDir/monitor/"
	#mv client.py file_watcher.py transfer_manager.py /home/$(whoami)/OneDir/monitor/
}
if [ -d /home/$(whoami)/OneDir/ ]
then
	if [ -d /home/$(whoami)/OneDir/monitor/ ]
	then
		if [ -e 'file_list.txt']
		then
			#mv client.py file_watcher.py transfer_manager.py /home/$(whoami)/OneDir/monitor/
			echo "we're here"
		
	else
		mkdir "/home/$(whoami)/OneDir/monitor/"
		echo "created it"	
	
else
	create_directorys
	echo "created it"	
 
#python client.py