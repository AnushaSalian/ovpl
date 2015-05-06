#!/bin/bash

LOGGER='src/http_logging/http_logging_server.py'
ADAPTER='src/adapters/AdapterServer.py'
CONTROLLER='src/ControllerServer.py'

SERVICES=(LOGGER ADAPTER CONTROLLER)

PID_FILE='/var/run/ads.pid'

# Start the services
start_service() {
  touch $PID_FILE
  if [ -z $args ]
  then
    python $LOGGER &
    #The variable "$!" has the PID of the last background process started. 
    echo "LOGGER:$!" >> $PID_FILE
    sleep 1
    python2 $ADAPTER &
    echo "ADAPTER:$!" >> $PID_FILE
    sleep 1
    python2 $CONTROLLER &
    echo "CONTROLLER:$!" >> $PID_FILE

  else
    for i in "$args";
    do
      j=$i
      echo $($j)
      echo inside for 
      echo $i
      python $j &
      echo "$i:$!" >> $PID_FILE
    done 
  fi
}

# Stop the services 
stop_service() {
  if [ -f $PID_FILE ]
  then
    for i in `cat $PID_FILE`;
    do
      kill `echo $i | cut -d ":" -f 2`;
    done
    rm $PID_FILE
    echo 'done'
  else
    echo 'No services are running to be stopped'   
  fi
}

# Start mongod service
start_mongod() {
  service mongodb start
}

# Stop mongod service
stop_mongod() {
  service mongodb stop
}

# Repair mongod service
repair_mongod() {
  mongodb --repair
}

# Check if the service mongod is already running
pre_check() {
  service mongodb status
  if [ $? -ne 0 ]
  then
    echo 'service mongod is not running'
    stop_mongod
    echo 'stopping mongod'
    repair_mongod
    echo 'restarting mongod'
    start_mongod
    echo 'service mongod successfully restarted' 
  fi
}


if [ $# -eq '0' ]
then
  pre_check &&
  stop_service &&
  start_service
	
elif [ $# -eq '1' ]
then
  args=""
  case "$1" in
  'start')
    pre_check &&
    stop_service &&
    start_service 
    ;;
  
  'stop')
    echo 'stopping all the services...'
    stop_service
    ;;   
  esac
  
else
  input_args=($@)
  action=${input_args[0]}
  args=${input_args[@]:1}

  if [ "$action" == "start" ]
  then
    pre_check &&
   # stop_service - here also ??
    start_service "$args"

  elif [ "$action" == "stop" ]
  then
    echo 'stop works'
    stop_service "$args"

  else
    echo 'Incorrect usage of arguments'
  fi

fi

