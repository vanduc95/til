# Usage
Add the following lines to `/etc/rsyslog.conf`:
```
# Send log messages to Fluentd
*.* @127.0.0.1:5140
```
Restart rsyslog service
```
$ sudo systemctl restart rsyslog.service
```
Run docker compose
```
$ cd syslog
$ docker-compose up
```

# Test
1. Test `in_tail` 
```
$ cd data
## Run script 
$ for ((i=1;i<=100;i++)); do  echo "Welcome $i times" >> tail.log; sleep 1; done
```

2. Test `in_syslog`
Run command with user root. Example
```
$ sudo apt update
## or
$ sudo su
```