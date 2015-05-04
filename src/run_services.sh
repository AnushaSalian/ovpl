# Proper header for a Bash script
#!/bin/bash
#title : run_services.sh
#desciption :
#usage : bash run_services.sh

LOGGER='http_logging/http_logging_server.py'
ADAPTER='adapters/AdapterServer.py'
CONTROLLER='ControllerServer.py'

# Start all the services
start_all() {
  touch /var/run/services.pid
  python $LOGGER &
  #The variable "$!" has the PID of the last background process started. 
  echo $! >> /var/run/services.pid
	sleep 1
  python2 $ADAPTER &
  echo $! >> /var/run/services.pid
  sleep 1
  python2 $CONTROLLER &
  echo $! >> /var/run/services.pid
}

# Stop all the services 
stop_all() {
  if [ -f /var/run/services.pid ]
  then
    killall python
    killall python2
    rm /var/run/services.pid
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
    echo "service mongod is not running"
    stop_mongod
    echo "stopping mongod"
    repair_mongod
    echo "restarting mongod"
    start_mongod
    echo "service mongod successfully restarted" 
  fi
}


if [ $# -ne '1' ]
then
  echo 'Please give one of the following arguments:
     1. start-services
     2. stop-services'
	
else
  case "$1" in
  'start-services')
    pre_check &&
    stop_all &&
    start_all 
    ;;
  
  'stop-services')
    echo 'stopping all the services...'
    stop_all
    ;;   

  'start-')

    ;;

  'stop-')

    ;;
  esac

fi


