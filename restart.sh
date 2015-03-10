sudo service pilight stop
sudo killall -9 pilight-daemon
sudo service pilight start
nohup python app.py >& /dev/null &
