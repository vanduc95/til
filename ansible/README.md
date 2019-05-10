# ansible-tutorial

### Inventory
```
[vm]
server1 ansible_host=192.168.122.46 ansible_user=root ansible_pass=abc@123
server2 ansible_host=192.168.122.151 ansible_user=ubuntu ansible_pass=abc@123

[localhost]

test ansible_host=127.0.0.1 ansible_user=ducnv ansible_pass=Ducmai1995
```
### Ansible Ad-hoc
```
$ ansible <HOST_GROUPS> -m <MODULE_NAME> -a "OPT_ARGS" -u <USERNAME>
ansible -i hosts vm -m ping all
ansible -i hosts vm -m shell -a ls 
```

