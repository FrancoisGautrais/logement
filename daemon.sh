#!/bin/bash


DIR=$(dirname $BASH_SOURCE )
cd $DIR
VENV=.venv
PID_FILE=logement.pid
LOGFILE=logement.log
PYTHON_MAIN=manage.py
PYTHON=python3
PORT=7093
HOST=LOCALHOST

. $VENV/bin/activate


function fct_start {
	nohup $PYTHON -u  manage.py runserver $HOST:$PORT  > $LOGFILE 2>&1 &
	echo -n $! > $PID_FILE
}

function fct_stop {
	fuser -k $PORT/tcp || true
}

function fct_restart {
	fct_stop
	fct_start
}

function fct_update {
	fct_stop
	git pull
	fct_start
}

function fct_pid {
	cat $PID_FILE
}

function fct_alive {
  kill -0 $(fct_pid) 2> /dev/null
  ret=$?
	if [ $ret -eq 0 ]; then
	  echo "true"
	  exit 0
	else
	  echo "false"
	  exit -1
  fi
}

if [[ $# -eq 0 ]]; then
	fct_start
	exit 0
elif [[ "$1" == "start" ]]; then
	fct_start
	exit 0
elif [[ "$1" == "restart" ]]; then
	fct_restart
	exit 0
elif [[ "$1" == "stop" ]]; then
	fct_stop
	exit 0
elif [[ "$1" == "update" ]]; then
	fct_update
elif [[ "$1" == "pid" ]]; then
	fct_pid
elif [[ "$1" == "alive" ]]; then
	fct_alive
else
	echo "Error on command line: $*"
	exit 1
fi
