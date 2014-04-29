#!/bin/bash

echo $(whoami)
function move_files {
	echo "move_files"
	mv client.py file_watcher.py transfer_manager.py /home/$(whoami)/OneDir/monitor/
}
function run {
    cd /home/$(whoami)/OneDir/monitor/
	python client.py
	echo "running"
}

if [ -d /home/$(whoami)/OneDir/ ]
then
	if [ -d /home/$(whoami)/OneDir/monitor/ ]
	then
		if [ -e client.py -a -e file_watcher.py -a -e transfer_manager.py ]
		then
			echo "we're here"
			run

		else
			move_files
			run
			
		fi
	else
		mkdir "/home/$(whoami)/OneDir/monitor/"
		move_files
		run	
	fi
else
	mkdir "/home/$(whoami)/OneDir/"
	mkdir "/home/$(whoami)/OneDir/monitor/"
	move_files
	run	
fi