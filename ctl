#!/bin/bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ] ; do SOURCE="$(readlink "$SOURCE")"; done
ROOT="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

PIDFILE=$ROOT/pid
WSPIDFILE=$ROOT/ws_pid

function do_start {
    $ROOT/run
}

function do_stop_pid {
	if [ -f $1 ]
	then
		PID=`cat $1`
		kill $PID
		sleep 2
		kill -9 $PID
		rm -f $1
	fi
}

function do_stop {
    do_stop_pid $PIDFILE
}


case "$1" in

"start")
	do_start
	exit $?
;;

"stop")
	do_stop
	exit $?
;;

"restart")
	do_stop && do_start
	exit $?
;;

*)
	echo "Usage: $0 {start|stop|restart}"
	exit 1
;;

esac