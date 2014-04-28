#!/bin/bash
 
echo $(whoami)
function create_directory {
	mkdir "monitor/"
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
		fi
	else
		mkdir "/home/$(whoami)/OneDir/"
		create_directory
		"created it"	
	fi
else
	mkdir "/home/$(whoami)/OneDir/"
	create_directory
	"created it"	
fi
 
#python client.py



