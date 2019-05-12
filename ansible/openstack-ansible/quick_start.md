### **Quick start**

---

#### **1. Install Ansible**

Thông qua apt:

```sh
$ sudo apt-get install ansible
```

#### **2. Setup to run role lb**


Thông tin về host trong file `openstack-ansible/lb_inventory`:

```sh
# group host of Load Balance nodes

[group_lb]
lb1 ansible_host=192.168.20.191 ansible_ssh_user=root ansible_ssh_pass=Ec0net@!2017
```

Thông tin về các card mạng trong file `openstack-ansible/roles/lb/vars/main.yml`

Để chạy playbook install bonding:

```sh
$ cd ~/openstac-ansible
$ ansible-playbook -i lb_inventory lb.yml
```
