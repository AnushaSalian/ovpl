# Proper header for a Bash script
#!/bin/bash
#title : run_services.sh
#desciption :
#usage : bash run_services.sh

LOGGER='src/http_logging/http_logging_server.py'
ADAPTER='src/adapters/AdapterServer.py'
CONTROLLER='src/ControllerServer.py'
PID_FILE='/var/run/ads.pid'

# Start all the services
start_all() {
  touch $PID_FILE
  python $LOGGER &
  echo 'LOGGER' >> $PID_FILE
  #The variable "$!" has the PID of the last background process started. 
  echo $! >> $PID_FILE
  sleep 1
  python2 $ADAPTER &
  echo 'ADAPTER' >> $PID_FILE
  echo $! >> $PID_FILE
  sleep 1
  python2 $CONTROLLER &
  echo 'CONTROLLER' >> $PID_FILE
  echo $! >> $PID_FILE
}

# Stop all the services 
stop_all() {
  if [ -f $PID_FILE ]
  then
    kill -9 $(<"$PID_FILE")
    rm $PID_FILE
    echo 'done'
  else
    echo 'No services are running to be stopped'   
  fi
}

#Start an individual service
start_one() {
python $2 &
echo $2 >> $PID_FILE
echo $! >> $PID_FILE
echo started $2
}

#Stop an individual service
#stop_one() {
# do a grep based on arg,
# read the next line of the file 
# matching the pattern

#} 

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
  stop_all &&
  start_all
	
elif [ $# -eq '1' ]
then
  case "$1" in
  'start')
    pre_check &&
    stop_all &&
    start_all 
    ;;
  
  'stop')
    echo 'stopping all the services...'
    stop_all
    ;;   
  esac

elif [ $# -eq '2' ]
then
  if [ "$1" == "start" ]
  then
    var = $2
    echo $var
    python $var &
    echo $2 >> $PID_FILE
    echo $! >> $PID_FILE
  else
    echo 'need to write this '
  fi


else
  echo 'hopefully this works'
fi

