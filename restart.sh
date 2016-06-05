sudo service pilight stop
sudo killall -9 pilight-daemon
sudo service pilight start
nohup sudo python app.py >& /dev/null &
