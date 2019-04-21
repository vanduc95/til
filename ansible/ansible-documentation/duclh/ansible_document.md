# Learning Ansible 2
# Table of Contents
- [Chương 1: Giới thiệu về Ansible](#introduction)
  - [1.1. IT automation](#itautomation)
  - [1.2. Ansible là gì?](#whatisansible)
  - [1.3. Kiến trúc của Ansible](#ansiblearchitecture)
  - [1.4. Cài đặt Ansible](#ansibleinstallation)
  - [1.5. Cấu hình Ansible](#ansibleconfiguration)
    - [1.5.1. Cấu hình qua biến môi trường](#variableEvn)
    - [1.5.2. Cấu hình qua file cấu hình](#configurationfile)
- [Chương 2: Cơ bản về Ansible](#ansiblebasic)
  - [2.1. YAML](#yaml)
  - [2.2. Hello Ansible](#helloansible)
- [Chương 3: Playbook](#playbook)
  - [3.1. Một playbook cơ bản](#basicplaybook)
  - [3.2. Tạo user bằng Ansible](#createuseransible)
  - [3.3. Jinja2 template](#jinja2template)
- [Chương 4: Quản lý multiple host với Ansible](#multihostmanage)
  - [4.1. Inventory file](#inventoryfile)
  - [4.2. Variables](#variables)
  - [4.3. Vòng lặp trong Ansible](#ansibleloop)
- [Chương 5: Ansible trong các triển khai phức tạp](#complexdeployment)
  - [5.1. local_action](#localaction)
  - [5.2. delegate_to](#delegateto)
  - [5.3. Conditional](#conditional)
  - [5.4. Boolean conditional](#Booleanconditional)
  - [5.5. Include](#include)
  - [5.6. Handler](#handler)
- [Chương 6: Role](#role)

<a name="introduction"></a>
## Chương 1: Giới thiệu về Ansible
Trước khi đi vào tìm hiểu các khái niệm cơ bản và nâng cao trong ansible, trước tiên, chúng ta cần hiểu được ansible là gì? vì sao dùng ansible? kiến trúc của ansible như thế nào?... Trả lời những câu hỏi này sẽ giúp chúng ta xác định được tốt hơn mục tiêu để học ansible phục vụ cho những dự án của mình.
<a name='itautomation'></a>
## 1.1. IT automation 
Đầu tiên, chúng ta sẽ thảo luận qua về khái niệm **IT automation**.

**IT automation** hiểu một cách cơ bản là những process và những software giúp quản lý cơ sở hạ tầng công nghệ thông tin (các cở sở hạ tầng này có thể là networking, các server hoặc là storage).

Trong những giai đoạn đầu của công nghệ thông tin, chúng ta cần rất nhiều người để quản lý một cụm nhiều máy chủ (server), họ phải làm việc tập trung và chính xác. Càng về sau, các server trở nên đánh tin cậy hơn và dễ dàng để quản lý hơn, do đó, có thể chỉ cần một người quản trị có thể quản lý cả một cụm server. Tuy nhiên, tại thời điểm đó, người quản trị cần phải cài đặt các phần mềm một cách thủ công, cập nhập một cách thủ công, và thay đổi cấu hình một cách thủ công. Việc này tốn rất nhiều thời gian và dễ bị lỗi. Vì vậy, họ bắt đầu viết các kịch bản (script) để đơn giản hóa công việc của họ. Tuy nhiên, những script đó lại rất phức tạp và không phù hợp triển khai trong quy mô lớn.

Những năm gần đây, các trung tâm dữ liệu phát triển mạnh về các quy mô lẫn mức độ phức tạp, nguyên nhân là do nhu cầu của các doanh nghiệp tăng lên. Do vậy, cần có những công cụ mới để thay thế các script đã được sử dụng trước đó, đó chính là nguyên nhân ra đời của các IT automation tool.

IT automation được chia ra làm hai loại chính. Đó là: **agent-based system ** và **agent-less system**.
### Agent-based system
Agent-based system là một hệ thống có hai thành phần chính: một **server** và một client được gọi là một **agent**.

Hệ thống chỉ có một **server** sẽ chứa tất cả thông tin cấu hình trong toàn bộ môi trường của bạn (toàn bộ cơ sở hạ tầng của bạn), trong khi **agent** là các server nằm trong môi trường đó. Theo chu kỳ, các **agent** sẽ kết nối đến **server** để kiểm tra các cấu hình của nó có thay đổi hay không? Nếu có, **agent** sẽ download những thay đổi và cập nhật.

Có thể có nhiều **server** trong trường hợp **high availability**, tuy nhiên cấu hình của các server này là giống nhau.
### Agent-less system
Trong các hệ thống **agent-less**, không có sự tồn tại của **agent**. Các hệ thống **agent-less** không hoàn toàn tuân theo mô hình **server/client**, bởi vì có thể có nhiều server, thậm chí số lượng server và client có thể bằng nhau. Kết nối giữa server và client sẽ được khởi tạo bởi **server** và kết nối đến **client** thông qua một số giao thức chuẩn chẳng hạn SSH, PowerShell.

Từ đây, chúng ta cũng có thể thấy được, các hệ thống **agent-based** khác với các hệ thống **agent-less** về một số vấn đề. Đối với vấn đề bảo mật, rõ ràng agent-based system cho phép tất cả các client kết nối đến, server có thể bị tấn công bất cứ lúc nào. Ngược lại, agent-less system sẽ ngăn chặn điều này bằng cách sử dụng firewall để chống lại một số truy cập nguy hiểm. Đối với vấn đề hiệu năng, agent-based system sẽ gây ra hiện tượng quá tải tại server, để cải thiện cần dùng high availability. Ngược lại, agent-less system sẽ cân bằng tải lên nhiều server trong toàn bộ môi trường.
## 1.2. Ansible là gì? <a name='whatisansible'></a>
Ansible là một IT automation tool, thuộc vào hệ thống agent-less. Mục tiêu của ansible là: đơn giản hóa, nhất quán, bảo mật, tin tưởng cao và dễ sử dụng.

Ansible sử dụng chủ yếu chế độ **push** thông qua kết nối SSH. Chúng ta có thể sử dụng ansible để thực hiện các hoạt động song song trên các host khác nhau. Ansible vô cùng đơn giản để cài đặt và cấu hình. Ansible có thể giúp bạn quản lý cấu hình, triển khai các ứng dụng, và các thực hiện các hoạt động một các tự động. Bên cạnh đó, Ansible cũng hỗ trợ cơ chế điều phối, khi đó bạn có thể chạy một chuỗi hoặc một tập các sự kiện nào đó trên các server khác nhau.

Không giống như Puppet hay Chef, ansible không sử dụng một **angent** tại remote host. Thay vào đó, ansible sử dụng SSH với giả sử tất cả các host muốn quản lý đều đã cài đặt SSH server và Python cũng được cài trên remote host. Điều này có nghĩa là chúng ta không cần phải thiết lập môi trường tại remote host.

## 1.3. Kiến trúc Ansible <a name='ansiblearchitecture'></a>
Ansible được thiết kế theo kiến trúc sau đây:

![](https://www.packtpub.com/graphics/9781783550630/graphics/0630OT_01_01.jpg)

Ý tưởng về kiến trúc của ansible ở đây là có một hoặc nhiều Command Center (hiểu cơ bản là các server cài đặt ansible), nơi sẽ phát ra các câu lệnh đến các remote host hoặc chạy một tâp các hoạt động thông qua các playbook.

Host inventory file xác định các remote host sẽ thực hiện các hành động. Playbook là nơi chứa một hoặc nhiều task mà được thực hiện bởi một core module của ansible cung cấp hoặc là một module được định nghĩa bởi người dùng.

<a name='ansibleinstallation'></a>
## 1.4. Cài đặt Ansible 
Cài đặt ansible rất đơn giản, chúng ta có thể thực hiện một trong số các cách sau:

Cài thông qua `yum`:
```
$ sudo yum install ansible
```
Cài thông qua `pip`:
```
sudo pip install ansible
```
Trong tài liệu này, chúng ta sẽ tìm hiểu về ansible version 2.0.
<a name='ansibleconfiguration'></a>
## 1.5. Cấu hình Ansible 
File cấu hình của ansible sử dụng format là INI để lưu trữ dữ liệu cấu hình. Bạn có thể overwrite gần như tất cả cấu hình của ansible thông qua các tùy chọn khi thực hiện các playbook (khái niệm này sẽ được nói đến chi tiết sau) hoặc thông qa các biến môi trường.

Khi một câu lệnh ansible được chạy, câu lệnh này sẽ nhìn vào các file cấu hình của nó trong một thứ tự nhất định đã được định nghĩa trước đó như sau:
- **ANSIBLE_CONFIG**: Đầu tiên, ansible sẽ kiểm tra biến môi trường này. Biến môi trường này sẽ trỏ đến file config.
- **./ansible.cfg**: Tiếp theo, nó sẽ kiểm tra file này trong thư mục hiện tại.
- **~/.ansible.cfg**: Thứ ba, nó sẽ kiểm tra file này trong thư mục /home của user
- **/etc/ansible/ansible.cfg**: Cuối cùng, nó sẽ kiểm tra file này. Đây là file được tạo ra mặc định khi cài đặt ansible thông qua một package manager.

Nếu cài đặt ansible thông qua một package manager hoặc thông qua pip, một **ansible.cfg** file sẽ được tạo ra trong thư mục **/etc/ansible**. Nếu ansible được cài đặt thông qua Git repository thì bạn sẽ tìm thấy **ansible.cfg** file trong thư mục mà bạn clone Git repo của ansible.

### Config thông qua biến môi trường
Chúng ta có thể config ansible thông qua biến môi trường có biến bắt đầu từ **ANSIBLE_**. Một ví dụ như sau:
```
    $ export ANSIBLE_SUDO_USER=root
```
Các biến môi trường có thể được sử dụng trong các playbooks
## Config sử dụng ansible.cfg
Ansible có nhiều tham số cấu hình, nhưng chúng ta có thể không cần đến tất cả. Dưới đây là nhưng tham số hay được sử dụng trong khi làm việc với ansible:
- **hostfile**: Biến này có giá trị là đường dẫn đến `inventory` file, đây là file chứa thông tin về các host và group mà ansible có thể kết nối đến. Ví dụ:
```
hostfile = /etc/ansible/hosts
```
- **library**: Bất cứ khi nào thực hiện một hành động bởi ansible, cho dù là thực hiện trên local host (máy đang cài đặt ansible) hay là trên một remote host. Nó sẽ sử dụng một phần code để thực hiện hành động đó, phần code này gọi là **module**. Biến **library** này có giá trị là đường dẫn đến thư mục chứa các module. Mặc định các thư viện của ansible được lưu trữ ở thư mục có đường dẫn sau:
```
library = /usr/share/ansible
```
- **forks**: Biến này cho biết số lượng process mặc định được sinh ra khi chạy các câu lệnh của ansible. Mặc định là sử dụng tối đa 5 tiến trình chạy song song.
```
forks = 5
```
- **sudo_user**: Biến này xác định người dùng mặc định để thực thi các câu lệnh. Biến này có thể được overwrite trong playbooks (xem chi tiết ở phần sau).
```
sudo_user = root
```
- **remote_port**: Biến này xác định port được sử dụng để kết nối SSH, mặc định là 22. Bạn không cần phải thay đổi giá trị này, trừ khi port SSH của bạn bị thay đổi thành một giá trị khác.
```
remote_port = 22
```
- **host_key_checking**: Biến này được sử dụng để vô hiệu hóa quá trình kiểm tra key của SSH host, mặc định là **True**.
```
host_key_checking = False
```
- **timeout**: Đây là giá trị mặc định cho timeout của kết nối SSH.
```
timeoute = 60
```
- **log_path**: Mặc định, ansible không ghi log vào bất kỳ một file nào. Nếu chúng ta muốn ghi output của ansible đến 1 file nào đó, hãy gán giá trị cho biến này là đường dẫn đến file bạn muốn lưu. Ví dụ:
```
log_path = /var/log/ansible.log
```

<a name='ansiblebasic'></a>
## Chương 3: Cơ bản về ansible 
Nhưng chúng ta cũng đã biết, ansible được sử dụng cho cả hai nhiệm vụ là tạo ra và quản lý toàn bộ một cơ sở hạ tầng, cũng có thể được tích hợp vào một cơ sở hạ tầng đã có trước đó.

Trong chương này, chúng ta sẽ tìm hiểu các vấn đề sau:
- Một playbook là gì? Cách playbook hoạt động như thế nào?
- Cách tạo ra một webserver sử dụng ansible
- Kiến thức cơ bản về Jinja 2 template engine

Đầu tiên, chúng ta sẽ tìm hiểu về YAML (YAML Ain't Markup Language), một ngôn ngữ tuần tự hóa dữ liệu (serialization language) được sử dụng rộng rãi trong ansible.

<a name='yaml'></a>
## 3.1. YAML 
YAML cũng tương tự như các ngôn ngữ tuần tự hóa dữ liệu khác (chẳng hạn như JSON, XML,...) có một số định nghĩa cơ bản sau:
- Declaration
- List
- Associative arrays

Khai báo biến trong YAML cũng tương tự như các ngôn ngữ lập trình khác, đó là:
```
	name: 'This is the name'
```

Để tạo ra một list, sử dụng dấu ` - `:
```
	- item 1
    - item 2
    - item 3
```

Sử dụng **thụt vào đầu dòng** để tạo ra các dictionary, nếu chúng ta muốn tạo ra một chuỗi liên kết, chỉ cần thêm một thụt vào đầu dòng:
```
	item:
    	name: TheName
        location: TheLocation
```

Cuối cùng, chúng ta có thể kết hợp tất cả lại với nhau:
```
	people:
    	- name: Albert
          number: +1000000
          country: USA
        - name: David
		  number: +4400000
          country: UK
```

Còn rất nhiều kiến thức về YAML, nhưng ở đây chúng ta chỉ cần hiểu cách khai báo và định nghĩa các biến, các list và dictionary để phục vụ cho việc học ansible.

<a name='helloansible'></a>
## 3.2. Hello Ansible 
Đầu tiên, chúng ta sẽ tạo ra 1 task cơ bản là ping đến 2 host và sau đó sẽ echo 'Hello Ansible' lên các host. Các bước thực hiện như sau:
- Tạo ra một `inventory` file. File này định nghĩa các host hoặc nhóm các host được dùng để thực hiện các task. Mỗi nhóm được định nghĩa trong một dấu ngoặc vuông. Ví dụ sau chúng ta có 1 group:
```
	$ cat inventory
    [servers]
	192.168.1.83 ansible_user=vm3
	25.9.172.231  ansible_user=ubuntu

```
- Bây giờ, chúng ta sẽ thực hiện ping 2 máy với nhau. Sử dụng thêm câu lệnh `ansible --help` để biết thêm về các option của ansible. Để kiểm tra ping giữa 2 máy, thực hiện câu lệnh sau:
```
	$ ansible servers -i inventory -m ping
    192.168.1.83 | SUCCESS => {
    "changed": false,
    "ping": "pong"
    }
    25.9.172.231 | SUCCESS => {
        "changed": false,
        "ping": "pong"
    }

```
- Sau khi ping được giữ 2 máy thành công, chúng ta sẽ thực hiện in dòng chữ **Hello Ansible** đến các host trong group **servers**:
```
    $ ansible servers -i inventory -m command -a '/bin/echo Hello Ansible'
    192.168.1.83 | SUCCESS | rc=0 >>
    Hello Ansible

    25.9.172.231 | SUCCESS | rc=0 >>
	Hello Ansible

```

Như vậy là chúng ta đã in được dòng chữ **Hello Ansible** lên các host trong group **servers** (kết quả như trong output của câu lệnh trên). Bây giờ, hãy xem xét các câu lệnh đã dùng ở trên:
```
	ansible servers -i inventory -m command -a '/bin/echo Hello Asible'
```
Trong câu lệnh này, **servers** là tên của group hoặc host muốn thực thi task, tùy chọn `-i inventory` sẽ là cung cấp file chứa thông tin về các group và host (trong trường hợp này inventory file chứa group server). Để thực hiện trên tất cả các hosts trong `inventory` file, thay thế **servers** bằng **all**. Tùy chọn m là tên module được sử dụng để thực thi (chúng ta sẽ nói nhiều hơn về module ở phần sau). và cuối cùng là tùy chọn a được sử dụng để cung cấp tham số cho module để thực thi, với lệnh `/bin/echo Hello Ansible`.

Ngoài ra, để cung cấp thông tin thêm về quá trình thực thi cũng như troubleshot, chúng ta có thể sử dụng thêm tùy chọn **v**, **vv** hoặc là **vvv** để output sẽ cung cấp thêm các thông tin chi tiết hơn về quá trình thực thi.
<a name='playbook'></a>
## Chương 3: Playbook 
Playbook là một trong các tính năng chính của ansible, nó nói cho ansible biết những gì cần thực hiện. Playbook giống như một **TODO** list của ansible để chứa danh sách các task. Mỗi task sẽ liên kết đến một **module** để thực hiện nhiệm vụ này. Playbook có cấu trúc rất đơn giản, dễ hiểu (được viết theo định dạng YAML), trong đó, module là một phần code của ansible hoặc được định nghĩa bởi người dùng bằng bất cứ ngôn ngữ lập trình nào, với điều kiện là output dưới dạng JSON. Có thể có nhiều task trong một playbook, các task này sẽ được thực hiện theo thứ tự từ trên xuống dưới.
<a name='basicplaybook'></a>
## 3.1. Một playbook cơ bản 
Playbook có thể có một danh sách các host, user variable, handler, task,.... Playbook cũng có thể overwrite hầu hết các cấu hình được định nghĩa trong các file cấu hình (như được nói đến ở phần trước). Bây giờ, hãy nhìn vào một ví dụ sau.

Chúng ta sẽ tạo ra một playbook để đảm bảo rằng apache package sẽ được cài đặt, dịch vụ phải được **enabled** và **started**. Dưới đây là nội dung của một playbook có tên là `setup_apache.yml`:
```
- hosts: all
  remote_user: centos
  tasks:
	- name: Ensure the HTTPd package is installed
	  yum:
		name: httpd
		state: present
		become: True
	- name: Ensure the HTTPd service is enabled and running
	  service:
		name: httpd
		state: started
		enabled: True
		become: True
```

File `setup_apache.yml` là ví dụ cho một playbook. File này bao gồm 3 thành phần chính sau:
- **hosts**: Đây là danh sách các host hoặc các group mà chúng ta muốn thực hiện task. Trường này là bắt buộc và mỗi playbook phải có trường này. Nó sẽ nói với ansible rằng những host nào sẽ chạy danh sách các task này. Khi một host hoặc một group host được cung cấp, ansible sẽ tìm kiếm thông tin của host trong **inventory** file được cung cấp. Nếu không tìm thấy, ansible sẽ bỏ qua tất cả các task đối với host hoặc group host này.
- **remote_user**: Đây là một tham số cấu hình của ansible mà được overwrite ở playbook, tham số này xác định cụ thể user nào thực hiện các task trong remote host.
- **tasks**: Cuối cùng là các task. Task là một danh sách các hoạt động mà chúng ta muốn thực hiện. Mỗi trường task chứa tên của task (trường **name**), một module để thực thi task, và các tham số được yêu cầu đối với mỗi module.

Trong ví dụ trên, chúng ta có hai task. Tham số **name** đại diện cho những task nào đang thực thi và được hiển thị cho người dùng có thể đọc được, như chúng ta có thể thấy được trong khi playbook chạy. Tham số **name** là tùy chọn. Các module, chẳng hạn như **yum**,**service** đều có một tập các tham số của nó. Hầu hết các module đều có tham số **name** (có một số module không có tham số này chẳng hạn module **debug**), tham số này cho biết những thành phần gì của module mà hành động sẽ thực hiện lên. Tiếp tục nhìn vào các tham số khác:
- Trong trường hợp module **yum**, tham số **state** có giá trị latest và nó chỉ ra rằng gói **httpd** latest cần phải được cài đặt. Nó tương tự với câu lệnh: `yum install httpd`
- Trong kịch bản của module **service**, tham số **state** có giá trị là started và nó chỉ rằng dịch vụ httpd cần phải được start. Nó tương tự với câu lệnh: `/etc/init.d/httpd start`
- **become: True** để xác định rằng các task nên được chạy dưới quyền sudo.

Nhưng vậy là chúng ta đã có được một playbook đơn giản, thực hiện 2 task là cài đặt và khởi động dịch vụ apache. Bây giờ, chúng ta sẽ thực hiện chạy playbook này.
### Chạy playbook
Chúng ta sẽ dụng câu lệnh sau để chạy playbook:
```
$ ansible-playbook -i inventory setup_apache.yml
```
Câu lệnh này có một ít thay đổi so với câu lệnh được dùng trong phần trước. Câu lệnh **ansible-playbook** được dùng để thực thi một playbook, với tùy chọn **i** là đường dẫn đến file chứa thông tin của remote host. và **setup_apache.yml** là đường dẫn đền playbook muốn chạy. Và kết quả thu được như sau:
```
PLAY [servers] ***************************************************

TASK [Gathering Facts] *******************************************
ok: [192.168.1.192]

TASK [Ensure the HTTPd package is installed] *********************
changed: [192.168.1.192]

TASK [Ensure the HTTPd service is enabled and running] ***********
changed: [192.168.1.192]

PLAY RECAP *******************************************************
192.168.1.192  : ok=3     changed=2   unreachable=0     failed=0
```

Như vậy là playbook đã hoạt động như mong muốn. Bây giờ, trên remote host, hãy kiểm tra xem **httpd** pakage đã được cài đặt và được start chưa. Chúng ta sử dụng câu lệnh sau:
```
$ rpm -qa | grep httpd
```
Kết quả thu được sẽ là:
```
httpd-tools-2.4.6-45.el7.centos.4.x86_64
httpd-2.4.6-45.el7.centos.4.x86_64
```
Và thực hiện check status của httpd service:
```
$ systemctl status httpd
```
Kết quả thu được như sau:
```
httpd.service - The Apache HTTP Server
Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
Active: active (running) since Tue 2017-07-18 09:43:26 ICT; 15min ago
     Docs: man:httpd(8)
           man:apachectl(8)
Main PID: 4588 (httpd)
   Status: "Total requests: 0; Current requests/sec: 0; Current traffic:   0 B/sec"
   CGroup: /system.slice/httpd.service
           ├─4588 /usr/sbin/httpd -DFOREGROUND
           ├─4589 /usr/sbin/httpd -DFOREGROUND
           ├─4590 /usr/sbin/httpd -DFOREGROUND
           ├─4591 /usr/sbin/httpd -DFOREGROUND
           ├─4592 /usr/sbin/httpd -DFOREGROUND
           └─4593 /usr/sbin/httpd -DFOREGROUND
```

Bây giờ, chúng ta hãy xem xét chuyện gì đã xảy ra khi playbook chạy. Đâu tiên, quan sát output ở trên ta thấy:
```
PLAY [servers] ***************************************************

TASK [Gathering Facts] *******************************************
ok: [192.168.1.192]
```

Dòng đầu tiên mà playbook biểu diễn để nói với chúng ta rằng playbook sẽ được bắt đầu và thực thi trên các host thuộc group **servers**. Tiếp theo là **Gathering Facts**, đây là task mặc định của ansible trước khi thực thi các task được liệt kê trong playbook. Task này thực hiện thu thập thông tin của remote host, những thông tin này sẽ được lưu vào trong một tập các biến được bắt đầu bằng **ansible_** và có thể được sử dụng sau này. Kết quả trả về là **ok**, tức là task đã hoàn thành và không có thay đổi gì xảy ra trên host **192.168.1.192**.
```
TASK [Ensure the HTTPd package is installed] *********************
changed: [192.168.1.192]

TASK [Ensure the HTTPd service is enabled and running] ***********
changed: [192.168.1.192]
```

Hai task này được liệt kê trong playbook và được thực hiện thành công. Kết quả là trạng thái của host **192.168.1.192** đã thay đổi, vì đã cài thêm httpd package và khởi động dịch vụ này.

Cuối cùng là dòng output sau:
```
PLAY RECAP *******************************************************
192.168.1.192  : ok=3     changed=2   unreachable=0     failed=0
```

Dòng này sẽ tổng kết lại các kết quả đã đạt được sau khi playbook thực hiện xong task. **ok=3** là số task hoàn thành trên remote host **192.168.1.192**, **changed=2** là trạng thái của remote host đã thay đổi 2 lần, **unreachable=0** là số lượng host không thể kết nối đến được là 0, **failed=0** là số lượng lỗi xảy ra trên remote host trong quá trình thực hiện các task.

Bây giờ, hãy thực hiện lại câu lệnh chạy playbook lần thứ 2. Kết quả thu được như sau:
```
PLAY RECAP *******************************************************
192.168.1.192  : ok=3     changed=0   unreachable=0     failed=0
```

Chúng ta có thể thấy, trạng thái **changed** cho thấy số lượng thay đổi trạng thái trên remote host bây giờ là 0. Nguyên nhân là do remote host **192.168.1.192** đã đạt được trạng thái mong muốn, các task này đã được thực hiện thành công bởi lần chạy trước đó.

Như vậy là chúng ta đã biết được những kiến thức cơ bản về một playbook. Bây giờ, chúng ta sẽ đi sâu vào từng thành phần để hỗ trợ thêm kiến thức về playbook.

### Ansible verbosity
Nhưng đã được nói qua trong phần trước, câu lệnh **ansible-playbook** có một tùy chọn debug. Tùy chọn này sẽ hiển thị thông tin output nhiều hơn, để chúng ta có thể dễ dàng biết được những gì đang diễn ra khi playbook chạy. Mỗi một **v** được thêm vào sẽ cung cấp nhiều thông tin ouput hơn.

Hãy thử chạy câu lệnh **ansible-playbook** với tùy chọn debug để xem chúng ta sẽ thu được gì. Ví dụ:
```
$ ansible-playbook -i inventory setup_apache.yml -vvv
```
### Variables in playbooks
Playbook hỗ trợ cho chúng ta khả năng có thể định nghĩa và sử dụng các biến tương tự như các ngôn ngữ lập trình. Mục đích là để playbook có thể được sử dụng một cách mềm dẻo hơn, có khả năng tái sử dụng và đơn giản hóa một playbook.

Hãy xem xét một ví dụ để biết được cách sử dụng biến trong playbook:
```
- hosts: servers
  remote_user: centos
  tasks:
	- name: Set variable 'name'
	  set_fact:
		name: Test machine
	- name: Print variable 'name'
	  debug:
		msg: '{{ name }}'
```
Chạy playbook với cách thông thường:
```
$ ansible-playbook -i inventory variables.yml
```

Kết quả sẽ được trả lại như sau:
```
PLAY [servers] *************************************************************

TASK [Gathering Facts] *****************************************************
ok: [192.168.1.192]

TASK [Set variable 'name']**************************************************
ok: [192.168.1.192]

TASK [Print variable 'name']************************************************
ok: [192.168.1.192] => {
    "msg": "Test machine"
}

PLAY RECAP******************************************************************
192.168.1.192              : ok=3    changed=0    unreachable=0    failed=0
```

Một biến trong ansible được gọi là một **fact**. Trong ví dụ trên, chúng ta đã định nghĩa một biến là **name: Test machine** và sau đó sử dụng module **debug** để in ra biến **name** vừa được định nghĩa.

Ansible cho phép chúng ta thiết lập các biến trong nhiều cách khác nhau: Định nghĩa trong một file, sau đó include vào playbook; định nghĩa ngay trong playbook; truyền biến thông qua command **ansible-playbook** sử dụng tùy chọn **-e**; hoặc có thể định nghĩa trong file **inventory**.

Ngoài ra, chúng ta cũng có thể sử dụng thông tin metadata mà ansible thu thập được trong giai đoạn thu thập thông tin. Sử dụng câu lệnh sau để xem thông tin metadata mà ansible thu thập được:
```
ansible all -i HOST, -m setup
```
Kết quả hiển thị như sau ( thông tin quá nhiều nên ở đây bị cắt bỏ một số phần):
```
192.168.1.192 | SUCCESS => {
    "ansible_facts": {
        "ansible_all_ipv4_addresses": [
            "192.168.1.192"
        ], 
        "ansible_all_ipv6_addresses": [
            "fe80::a852:2a2c:5a1:674a"
        ], 
        "ansible_apparmor": {
            "status": "disabled"
        }, 
        "ansible_architecture": "x86_64", 
        "ansible_bios_date": "12/01/2006", 
        "ansible_bios_version": "VirtualBox", 
        "ansible_cmdline": {
            "BOOT_IMAGE": "/vmlinuz-3.10.0-514.el7.x86_64", 
            "LANG": "en_US.UTF-8",
            "crashkernel": "auto",
            "quiet": true,
            "rd.lvm.lv": "cl/swap",
            "rhgb": true,
            "ro": true,
            "root": "/dev/mapper/cl-root"
        },
        "ansible_date_time": {
            "date": "2017-07-18",
            "day": "18",
            "epoch": "1500350715", 
            "hour": "11",
            "iso8601": "2017-07-18T04:05:15Z", 
            "iso8601_basic": "20170718T110515004017", 
            "iso8601_basic_short": "20170718T110515", 
            "iso8601_micro": "2017-07-18T04:05:15.004125Z", 
            "minute": "05", 
            "month": "07", 
            "second": "15", 
            "time": "11:05:15", 
            "tz": "ICT", 
            "tz_offset": "+0700", 
            "weekday": "Thứ ba", 
            "weekday_number": "2", 
            "weeknumber": "29", 
            "year": "2017"
        }, 
        "ansible_default_ipv4": {
            "address": "192.168.1.192", 
            "alias": "enp0s3", 
            "broadcast": "192.168.1.255",
            "gateway": "192.168.1.254",
            "interface": "enp0s3",
		....
```
Chúng ta có thể thấy một danh sách rất lớn các thông tin của remote host. Bây giờ, chúng ta sẽ sử dụng các biến này trong playbook để in ra tên và version của OS của remote host. Playbook có nội dung như sau:
```
- hosts: servers
  remote_user: centos
  tasks:
    - name: Print OS and version
      debug:
           msg: '{{ ansible_distribution }} {{ ansible_distribution_version }}'
```
Chạy playbook và chúng ta sẽ thu được kết quả như sau:
```
$ ansible-playbook playbooks/os_info.yml -i inventory
PLAY [servers] ************************************************************

TASK [Gathering Facts]*****************************************************
ok: [192.168.1.192]

TASK [Print OS and version]************************************************
ok: [192.168.1.192] => {
    "msg": "CentOS 7.3.1611"
}

PLAY RECAP*****************************************************************
192.168.1.192              : ok=2    changed=0    unreachable=0    failed=0

```
Kết quả in ra mà thông tin về OS và version của remote host đang được kết nối đến. Và đây là một ví dụ về truyền biến thông qua command **ansible-playbook** với tùy chọn **-i**:
```
$ ansible-playbook playbooks/os_info.yml -i inventory -e 'name=test01'
```

Bây giờ chúng ta đã có những kiến thức cơ bản về playbook. Tiếp theo, hãy đi vào một số ví dụ phức tạp hơn.
<a name='createuseransible'></a>
## 3.2. Tạo một user bằng Ansible 
Mục tiêu của playbook này là tạo một user mà có khả năng truy cập được với một SSH key, và có thể thực hiện được các hành động như các người dùng khác mà không cần hỏi password, tức là có quyền root. Playbook sẽ có nội dung như sau:
```
- hosts: servers
  user: root
  tasks:
   - name: Ensure ansible user exist
     user:
        name: ansible
        state: persent
        comment: Ansible
   - name: Ensure ansible user accepts the SSH key
     authorized_key:
        user: ansible
        key: /home/huynhduc/.ssh/id_rsa.pub
        state: present
   - name: Ensure the ansible user is sudoers with no password required
     lineinfile:
        dest: /etc/sudoers
        state: present
        regexp: '^ansible ALL\='
        line: 'ansible ALL=(ALL) NOPASSWD:ALL'
        validate: 'visudo -cf %s'

```
Trước khi chạy, chúng ta sẽ nói qua một chút về playbook này. Ở đây, chúng ta sử dụng 3 module là: **user**, **autorized_key**, **lineinfile**. Đối với module **user**, như tên gọi của nó, module này thực hiện thêm, sửa hoặc xóa user.

Đối với module **authorized_key**, module này cho phép sao chép public SSH key đến một user cụ thể ở remote host. Trong trường hợp này, chúng ta sẽ sao chép public key của máy đang chạy ansible (được gọi là local host) đến user có tên là **ansible** trong remote host. Tham số **key** là một string (public key của local host) hoặc là 1 url chẳng hạn như https://github.com/username.keys. Module này không thay đổi tất cả SSH key của user, mà chỉ đơn giản là thêm hoặc xóa (phụ thuộc vào tham số **state** là present hay là absent) một key cụ thể nào đó.

Đối với module **lineinfile**, module này cho phép chúng ta có thể thay đổi nội dung của một file. Nó làm việc tương tự với câu lệnh **sed** trong command line. Bạn sẽ xác định biểu thức chính quy để tìm đến dòng phù hợp thông qua tham số **regexp**, và sau đó là xác định dòng mới cần thêm thay thế nếu như tìm thấy dòng phù hợp với biểu thức chính quy. Trong trường hợp không tìm thấy, dòng mới sẽ được thêm đến cuối file.

Bây giờ, hãy chạy playbook này:
```
$ ansible-playbook -i inventory playbooks/firstrun.yml

PLAY [servers]*************************************************************

TASK [Gathering Facts]*****************************************************
ok: [192.168.1.192]

TASK [Ensure ansible user exist]*******************************************
ok: [192.168.1.192]

TASK [Ensure ansible user accepts the SSH key]*****************************
changed: [192.168.1.192]

TASK [Ensure the ansible user is sudoers with no password required]********
changed: [192.168.1.192]

PLAY RECAP ****************************************************************
192.168.1.192              : ok=4    changed=2    unreachable=0    failed=0
```
Như vậy là chúng ta đã có một user **ansible**, copy ssh key đến user này và thực hiện gán quyền thực hiện các hành động không cần hỏi password.

Tiếp theo, chúng ta sẽ xem xét qua một nội dung khá của ansible, đó là **Jinja2 template**

<a name='jinja2template'></a>
## 3.3. Jinj2 template 
Jinja2 template là một template engine được sử dụng rộng rãi trong python. Jinja2 template cũng được sử dụng để tạo ra các file trên remote host. Ở trong bài viết này, chúng ta chỉ tìm hiểu những khái niệm cơ bản cần thiết để làm việc với ansible.
### Variables
Chúng ta có thể in ra nội dung của một biến với cú pháp đơn giản sau:
```
{{ VARIABLE_NAME }}
```
Chúng ta có thể in ra nội dung của một phần tử trong một array:
```
{{ ARRAY_NAME['KEY'] }}
```
Nếu muốn in ra một thuộc tính của một object, sử dụng câu lệnh sau:
```
{{ OBJECT_NAME.PROERTY_NAME }}
```
### Conditional
Một tính năng thường xuyên được sử dụng trong template nữa đó là câu điều kiện. Nó sẽ in ra các giá trị khác nhau tùy vào điều kiện cụ thể. Dưới đây là một ví dụ:
```
<html>
	<body>
		<h1>Hello World!</h1>
		<p>This page was created on {{ ansible_date_time.date}}.</p>
		{% if ansible_eth0.active == True %}
			<p>eth0 address {{ ansible_eth0.ipv4.address }}.</p>
		{% endif %}
	</body>
</html>
```
Đây là một template đơn giản, nó sẽ in ra thời gian là ngày hiện tại của remote host thông qua cú pháp `{{ ansible_data_time.date }}`. Tiếp theo, là một câu điều kiện, kiểm tra nếu thuộc tính *active* của object *ansible* là `ansible_eth0.active == True` thì sẽ in ra địa chỉ mạng của eth0 thông qua cú pháp `{{ ansible_eth0.ipv4.address }}`
### Cycles
Jinja2 template cũng hỗ trợ khar năng để tạo ra các vòng lặp. Dưới đây sẽ mở rộng cho ví dụ trên, chúng ta sẽ in ra địa chỉ IPv4 của mỗi card mạng có trong remote host. Đây là nội dung của file `template.html`
```
<html>
	<body>
        <h1>Hello World!</h1>
        <p>This page was created on {{ ansible_date_time.date}}.</p>
        <p>This machine can be reached on the following IPaddresses</p>
        <ul>
            {% for address in ansible_all_ipv4_addresses %}
                <li>{{ address }}</li>
            {% endfor %}
        </ul>
	</body>
</html>
```
Cú pháp của vòng lặp cũng tương tự như cú pháp trong python. Tiếp theo, chúng ta sẽ xem xét một ví dụ của Jinja2 template.
### Example with Jinja2 template
Chúng ta sẽ thực hiện tạo ra một file trên remote host với `template.html` đã tạo ra ở phần trước. Playbook sẽ có nội dung như sau:
```
- hosts: servers
  remote_user: centos
  tasks:
    - name: User template to create file in home directory
      template:
         src: template/template.html
         dest: /var/www/html/index.html
         owner: root
         group: root
         mode: 0644
      become: True
```
Chạy playbook và output như sau:
```
ansible-playbook -i inventory playbooks/template.yml

PLAY [servers]**************************************************************

TASK [Gathering Facts]******************************************************
ok: [192.168.1.192]

TASK [User template to create file in home directory]***********************
changed: [192.168.1.192]

PLAY RECAP******************************************************************
192.168.1.192              : ok=2    changed=1    unreachable=0    failed=0

```
Bây giờ, chúng ta đã tạo ra một file `/var/www/html/index.html` trên remote host.
Có thể kiểm tra bằng câu lệnh sau, chúng ta sẽ thu được nội dung như sau:
```
$ cat /var/www/html/index.html
<html>
	<body>
	<h1>Hello World!</h1>
	<p>This page was created on 2017-07-18.</p>
	<p>This machine can be reached on the following IPaddresses</p>
	<ul>
					<li>192.168.1.192</li>
	</ul>
</body>
</html>

```
Như vậy là file cuối cùng thu được có nội dung đúng như mong muốn.
## Chương 4: Quản lý multiple host với Ansible <a name='multihostmanage'></a>
Trong chương trước chúng ta đã xác định được các host để thực hiện các hành động. Nhưng chúng ta vẫn chưa quản lý được các host này. Chương này sẽ nói rõ về nội dung này. Nội dung của chương này có các phần sau:
- Ansible inventories
- Ansible host/group variables
- Ansible loops

<a name='inventoryfile'></a>
## 4.1. Inventory file 
Inventory là một file được định dạng theo format INI (Initiaization) và sẽ nói với Ansible các hosts sẽ được sử dụng để thực hiện các task.

Ansible có thể chạy các tasks trên nhiều host song song với nhau. Để làm được điều này, ansible cho phép chúng ta gom nhóm các host vào các group trong inventory file, sau đó sẽ truyền tên của group đến ansible. Ansible sẽ tìm kiếm group trong inventory file và chạy các task trên các host trong group song song với nhau.

Chúng ta có thể truyền inventory file đến ansible sử dụng tùy chọn **-i** theo sau là đường dẫn đến inventory file. Nếu inventory file không được xác định, thì mặc định ansible sẽ sử dụng đường dẫn trong tham số `host_file` trong file cấu hình `ansible.cfg` của ansible. Nếu giá trị của tùy chọn **-i** là một list (chứa tối thiểu 1 dấu phẩy), ansible sẽ xem đó là một danh sách inventory file, còn lại ansible sẽ xem đó là đường dẫn đến inventory file.

### Basic inventory file
Trước khi đi sâu vào khái niệm này, chúng ta sẽ nhìn vào một inventory file cơ bản có tên là **hosts**, với nội dung như sau:
```
host1.foo.io
host2.foo.io
host3.foo.io
```
Chạy playbook với tùy chọn `-i` có giá trị là đường dẫn đến file **hosts** trong câu lệnh sau:
```
$ ansible-playbook -i hosts webserver.yml
```
Khi thực thi, ansible sẽ tìm đến file **hosts** để lấy thông tin của host được chỉ đến trong tham số **hosts** được định nghĩa ở file playbook.
### Groups in inventory file
Một group là đại diện cho một danh sách các host mà khi ansible gọi đến tên của group, thì các task của ansible sẽ được thực hiện song song trên các host trong group. Group được định nghĩa trong dấu ngoặc vuông. File **hosts** sẽ được thay đổi như sau:
```
$ cat hosts
[webserver]
ws01.fale.io
ws02.fale.io
ws03.fale.io
ws04.fale.io

[database]
db01.fale.io
```
Để gọi đến group trong playbook, chúng ta chỉ cần gán giá trị cho tham số **hosts** trong playbook là tên của group. Ví dụ như sau:
```
- hosts: webserver
  ....

- hosts: database
  ....
```
### Regular expression in inventory file
Khi chúng ta có một lượng lớn các host trong inventory file với các tên tương tự nhau. Ví dụ, các server có tên là WEB01, WEB02, WEB03,... Chúng ta có thể giảm số lượng dòng trong file **hosts** bằng cách sử dụng regular expression. File **hosts** sẽ được thay đổi như sau:
```
[webserver]
ws[01:04].fale.io

[database]
db01.fale.io
```
Như vậy là thay vì chúng ta phải sử dụng 4 dòng để liệt kê ra các host thì bây giờ chỉ cần 1 dòng. Việc này sẽ có tác dụng khi số lượng host lớn.
 <a name='variables'></a>
## 4.2. Variables
Chúng ta có thể định nghĩa các biến theo nhiều cách:
- Định nghĩa bên trong playbook
- Định nghĩa trong 1 file riêng biệt, sau đó include vào playbook
- Truyền từ command ansible với tùy chọn `-e`
- Định nghĩa từ inventory file. Chúng ta có thể định nghĩa các biến trên từng host, hoặc là trên từng group.

Bây giờ, sẽ đi lần lượt từng cách định nghĩa khác nhau.
### Host variables
Chúng ta có thể định nghĩa các biến trên các host cụ thể, bên trong inventory file. Cho ví dụ như chúng ta muốn xác định các port khác nhau trên từng host cho webserver. Chúng ta có thể thực hiện định nghĩa các biến như sau trong file **hosts**
```
[webserver]
ws01.fale.io webserverport=10000
ws02.fale.io webserverport=10001
ws03.fale.io webserverport=10002
ws04.fale.io webserverport=10003

[database]
db01.fale.io
```
Như vậy, các host sẽ chạy webserver trên các port khác nhau.
### Group variables
Trong trường hợp chúng ta muốn định nghĩa một biến được sử dụng trong tất cả các host của một group. Chúng ta sẽ thực hiện như sau:
```
[webserver]
ws01.fale.io
ws02.fale.io
ws03.fale.io
 webserverport=10003

[webserver:vars]
httpd_enalbed=True

[database]
db01.fale.io
```
### Variable files
Trường hợp chúng ta có quá nhiều biến cho mỗi host hay quá nhiều biến cho một group cần phải định nghĩa. Chúng ta có thể tạo ra một file riêng để khai báo các biến đó, sau đó sẽ `include` vào trong inventory file. Thông thường, chúng ta sẽ đặt các file chứa các host variable vào trong một folder là `host_vars`, và tương tự với file chứa các group variable là `group_vars`.

**NOTE:** Các biến của inventory cũng tuân theo một thứ tự phân cấp, cụ thể là: các host variable sẽ ghi đè các group variable; và các group variable sẽ ghi đè các biến trong các group variable file. Chúng ta có thứ tự độ ưu tiên như sau:
```
host variable > host variable file > group variable > group variable file > playbook variable > command_line option -u
```
### Ghi đè biến thông qua một inventory file
Chúng ta cũng có thể ghi đè các tham số cấu hình thông qua một inventory file. Các tham số cấu hình này sẽ ghi đè lại tất các các tham số cấu hình tương tự mà được định nghĩa trong file cấu hình `ansible.cfg`, trong biến môi trường, và trong các playbooks. Các biến được khai báo trong inventory file này được truyền đến các câu lệnh `ansible-playbook` và `ansible` có quyền ưu tiên cao hơn các biến khác.

Dưới đây là các tham số mà chúng ta có thể ghi đè trong một inventory file:
- **ansible_user**: Tham số này được sử dụng để ghi đè tên user mà được sử dụng để kết nối đến remote host. Trong trường hợp mỗi host có một user khác nhau, tham số này sẽ giúp bạn.
- **ansible_port**: Tham số này sẽ ghi đè cổng port SSH mặc định đối với mỗi user xác định.
- **ansible_host**: Tham số này sẽ ghi đè tên bí danh của host
- **ansible_connection**: Tham số này xác định loại kết nối đến remote host. Các giá trị có thể đó là SSH, Paramiko hoặc local.
- **ansible_private_key_file**: Tham số này xác định private key được sử dụng cho SSH.

<a name='ansibleloop'></a>
## 4.3. Sử dụng vòng lặp trong ansible 
Cũng như trong các ngôn ngữ lập trình khác, trong một số trường hợp, chúng ta có một số task mà có các tham số tương tự nhau, chỉ khác mỗi giá trị. Lúc đó, chúng ta sẽ sử dụng một danh sách các giá trị của các tham số tương tự đó. Ví dụ, để đảm bảo http và https có thể truyền qua firewall. Nếu không sử dụng danh sách thì chúng ta có playbook như sau:
```
- hosts: webserver
  remote_user: ansible
  tasks:
	- name: Ensure HTTP can pass the firewall
	  firewalld:
		service: http
	    state: enabled
	    permanent: True
	    immediate: True
      become: True
	- name: Ensure HTTPS can pass the firewall
  	  firewalld:
	  	service: https
		state: enabled
		permanent: True
		immediate: True
	  become: True
```
Để sử dụng danh sách, ansible hỗ trợ vòng danh sách đơn giản với cú pháp là `with_items`. Ví dụ sẽ được viết lại như sau:
```
- hosts: webserver
  remote_user: ansible
  tasks:
	- name: Ensure HTTP and HTTPS can pass the firewall
	  firewalld:
		service: '{{ item }}'
	    state: enabled
	    permanent: True
	    immediate: True
      become: True
      with_items:
		- http
		- https
```
Khi chạy playbook, chúng ta sẽ thu được kết quả như sau:
```
$ ansible-playbook -i hosts webserver.yaml
PLAY [webserver] ***********************************************************
TASK [Gathering Facts] *****************************************************
ok: [192.168.1.59]

TASK [Ensure HTTP and HTTPS can pass the firewall] *************************
ok: [192.168.1.59] => (item=http)
ok: [192.168.1.59] => (item=https)
PLAY RECAP *****************************************************************
192.168.1.59        : ok=2      changed=0 unreachable=0             failed=0
```
Như trong ví dụ, `with_items` là một danh sách các giá trị của tham số `item` được gọi đến bằng cú pháp ``{{ item }}``. Khi chạy playbook, task này sẽ chạy lần lượt với từng giá trị của tham số item, và kết quả được in ra như output ở trên.
### Nested loop
Có nhiều trường hợp, chúng ta muốn lặp qua các thành phần của một list, và mỗi item lại là một list khác (tức là vòng chuỗi lồng nhau). Cho ví dụ, bây giờ, chúng ta muốn tạo ra các folder `mail` và folder `public_html` trong folder `home` cho hai user là `alice` và `bob`. Bạn có thể thực hiện việc này bằng cách sử dụng vòng lặp lồng nhau. Playbook sẽ có nội dung như sau:
```
- hosts: all
  remote_user: ansible
  vars:
	users:
		- alice
		- bob
	folders:
		- mail
        - public_html
  tasks:
	- name: Ensure the users exist
	  user:
		name: '{{ item }}'
	  become: True
	  with_items:
		- '{{ users }}'

	- name: Ensure the folders exist
	  file:
		path: '/home/{{ item.0 }}/{{ item.1 }}'
		state: directory
	  become: True
	  with_nested:
		- '{{ users }}'
		- '{{ folders }}'
```
Xem xét ví dụ trên ta thấy, trong task `Ensure the users exist` sử dụng `with_items` tương tự phần trước với users list. Trong task `Ensure the folder exist`, chúng ta đã sử dụng vòng lặp lồng nhau với cú pháp `with_nested` và có giá trị là danh sách hai list là users list và folders list. Tương tự như trong các ngôn ngữ lập trình, chỉ số sẽ được đánh từ 0. Do vậy, để gọi đến users list sẽ dùng cú pháp `item.0` và để gọi đến folder list sẽ dùng đến `item.1`.
### Fileglobs loop với with_fileglobs
Đôi khi, chúng ta muốn thực hiện mốt số hành động lên một file trong một folder nhất định nào đó. Cho ví dụ như, chúng ta muốn copy những file có tên bắt đầu bởi `rt_` từ một folder này đến một folder khác. Để làm điều này, chúng ta có playbook sau:
```
- hosts: all
  remote_user: ansible
  tasks:
	- name: Ensure the folder /tmp/iproute2 is present
	  file:
		dest: '/tmp/iproute2'
		state: directory
	  become: True
	- name: Copy files that start with rt to the tmp folder
	  copy:
		src: '{{ item }}'
		dest: '/tmp/iproute2'
		remote_src: True
	  become: True
	  with_fileglob:
		- '/etc/iproute2/rt_*'
```
Thực hiện playbook trên, ta sẽ có được các file bắt đầu với `rt_` được chứa trong thư mục `/etc/iproute2/` được tạo ra ở task trước.
### Interger loop với with_sequence
Trong trường hợp chúng ta cần thực hiện lặp trong một phạm vi số nguyên nào đó (ví dụ từ 0 đến 10). Cụ thể, chúng ta muốn tạo ra một tập các folder có tên là `folderXY` với XY là các số từ 1 đến 10. Để làm điều này, chúng ta có file `with_sequence.yml` sau:
```
- hosts: all
  remote_user: ansible
  tasks:
	- name: Create the folders /tmp/dirXY with XY from 1 to 10
	  file:
		dest: '/tmp/dir{{ item }}'
		state: directory
	  with_sequence: start=1 end=10
	  become: True
```

Như vậy là chúng ta đã tìm hiểu qua những kiến thức cơ bản nhắt của ansible. Đến đây, chúng ta có thể hiểu được các nội dung sau:
- Ansible là gì? kiến trúc của ansible như thế nào?
- Viết chương trình in ra dòng chữ 'Hello Ansible'
- Làm quen với playbook và các thành phần trong playbook
- Tìm hiểu được một số module và cách sử dụng chúng trong ansible
- Tìm hiểu các khái niệm như variable, inventory file, template Jinja2, iterator.

Tiếp theo, chúng ta sẽ đi vào những kiến thức phức tạp hơn để có được sức mạnh thực sự của ansible.

<a name='complexdeployment'></a>
## Chương 5: Ansible trong các triển khai phức tạp 
Trong các chương trước, chúng ta chỉ mới tìm hiểu qua các khái niệm và triển khai các playbook đơn giản. Trong môi trường sản xuất, chúng ta thường xuyên đối mặt với nhiều trường hợp phức tạp. Những trường hợp phức tạp này bao gồm việc tương tác giữa hàng trăm hoặc hàng ngàn host và các host là phụ thuộc vào các group khác nhau, hay là các group lại thực hiện các trao đổi với nhau chẳng hạn backup hay replicate. Chương này sẽ cung cấp cho chúng ta về các tính năng cốt lõi của ansible để giải quyết các bài toán trên trong môi trường doanh nghiệp. Và mục tiêu của chương này sẽ giúp chúng ta có được một tương tưởng rõ ràng về cách viết một playbook trong môi trường sản xuất.

Đầu tiên, chúng ta sẽ tìm hiểu về tính năng `local_action`.
<a name='localaction'></a>
## 5.1. Local action 
Tính năng `local_action` của Ansible giúp chúng ta có thể thực hiện các task trên local host (tức là host đang chạy ansible).

Xem xét các vấn đề sau:
- Sinh ra một host mới.
- Quản lý các câu lệnh của bạn trong việc cài đặt các pakage và thiết lập cấu hình.

Có một số task có thể chạy trên local machine, nơi mà đang chạy câu lệnh `ansible-playbook` hơn là việc login vào một remote host và thực hiện câu lệnh này. Ví dụ, chúng ta muốn thực hiện một lệnh shell trên local host. Chúng ta sẽ truyền tên module và các tham số của module đó đến `local_action`, Ansible sẽ thực thi task tại máy local. Hãy xem cách hoạt động của `local_action` với module `shell` thông qua ví dụ sau:
```
- hosts: servers
  remote_user: centos
  tasks:
    - name: Count processes running on the remote system
      shell: ps | wc -l
      register: remote_processes_number

    - name: Print remote running processes
      debug:
         msg: '{{ remote_processes_number.stdout }}'

    - name: Count processes running on the local system
      local_action: shell ps | wc -l
      register: local_processes_number

    - name: Print local running processes
      debug:
         msg: '{{ local_processes_number.stdout }}'
```

Ở trong ví dụ trên, task đầu tiên thực hiện câu lệnh `ps | wc -l` trên remote host để đếm số process đang chạy và task thứ hai in ra số lượng process được trả về task đầu tiên thông qua tham số `remote_process_number`. Tiếp theo, task thứ 3 thực hiện cùng câu lệnh đếm số lượng process, nhưng được thực hiện trên local host. Chúng ta sử dụng module `local_action` với tham số là module `shell` và các tham số của module `shell`. Kết quả chạy playbook như sau:
```
$ ansible-playbook -i inventory playbooks/local_action.yml

PLAY [servers]************************************************************

TASK [Gathering Facts] ****************************************************
ok: [192.168.1.192]

TASK [Count processes running on the remote system] ***********************
changed: [192.168.1.192]

TASK [Print remote running processes] *************************************
ok: [192.168.1.192] => {
    "msg": "7"
}

TASK [Count processes running on the local system] ************************
changed: [192.168.1.192 -> localhost]

TASK [Print local running processes] **************************************
ok: [192.168.1.192] => {
    "msg": "11"
}

PLAY RECAP ****************************************************************
192.168.1.192              : ok=5    changed=2    unreachable=0    failed=0
```
Rõ ràng, hai kết quả là khác nhau, vì chúng ta đang đếm số process trên hai host.

Tiếp theo, Ansible cũng cung cấp một tính năng khác để phân chia một số hành động cụ thể đến một máy xác định: đó là tính năng `delegate_to`.

<a name='delegateto'></a>
## 5.2. Delegate_to
Đôi khi, chúng ta muốn thực hiện một hành động trên các host khác nhau. Cho ví dụ, trong khi bạn **đang triển khai** một số hành động trên application server node, bạn muốn chạy một lệnh trên database để lấy thông tin nào đấy cần thiết trên database node. Chúng ta sẽ sử dụng câu lệnh `delegate_to: HOST` để thực hiện công việc trên database node. Dưới đây là một ví dụ:
```
- hosts: servers
  remote_user: centos
  tasks:
    - name: Count processes running on the remote system
      shell: ps | wc -l
      register: remote_processes_number

    - name: Print remote running processes
      debug:
         msg: '{{ remote_processes_number.stdout }}'

    - name: Count processes running on the local system
      shell: ps | wc -l
      delegate_to: localhost
      register: local_processes_number

    - name: Print local running processes
      debug:
         msg: '{{ local_processes_number.stdout }}'

```
Như vậy, kết quả của playbook này sẽ tương tự như playbook sử dụng `local_action` ở phần trước. Ở đây, `delegate_to` là một mở rộng của `local_action`, có nghĩa là có thể thực hiện trên các host khác không chỉ trên local host.
<a name='conditional'></a>
### 5.3. Conditions 
Cho đến bây giờ, chúng ta đã học được cách các playbook hoạt động và cách các task được thực hiện. Đó là khi chạy một playbook thì các task sẽ được thực hiện lần lượt từ trên xuống dưới. Trong một số trường hợp, chúng ta chỉ muốn thực hiện một số task trong danh sách các task của playbook. Hoặc là, trong trường hợp khác tên package khác nhau trên các OS khác nhau, ví dụ như Apache Httpd server trên RedHat thì package có tên là `httpd`, còn trên Ubuntu là `apache2`. Đối với những trường hợp này, Ansible hỗ trợ câu điều kiện để có thể thực hiện những task nhất định nếu điều kiện được thỏa mãn.

Dưới đây là một ví dụ, chúng ta sẽ cài đặt Apache Httpd server trên remote host, nhưng chưa xác định được OS của remote host là Centos hay là Ubuntu. Do đó, playbook sẽ có nội dung như sau:
```

```
Trong playbook trên, task đầu tiên chúng ta sẽ đưa ra thông tin về OS của remote host. Trong trường hợp, biến `ansible_os_family` (đây là biến của việc thu thập thông tin remote từ task mặc định `Gathering Fact` được nói ở phần trước đây) có giá trị là `RedHat` thì task hai thực hiện, ngược lại, nếu `ansible_os_family` là `Ubuntu` thì task thứ ba sẽ được thực hiện.

Chạy playbook và kết quả thu được như sau:
```
$ ansible-playbook -i inventory playbooks/conditions.yml

PLAY [servers] ****************************************************************

TASK [Gathering Facts] ********************************************************
ok: [192.168.1.192]

TASK [Print the ansible_os_family value] **************************************
ok: [192.168.1.192] => {
    "msg": "RedHat"
}

TASK [Ensure the httpd package is updated] ************************************
ok: [192.168.1.192]

TASK [Ensure the apache2 package is updated] **********************************
skipping: [192.168.1.192]

PLAY RECAP ********************************************************************
192.168.1.192                  : ok=3    changed=0    unreachable=0    failed=0
```
Như output trên thể hiện, do OS của remote host là `RedHat` nên task hai được thực hiện và task ba có trạng thái là **Skipping**.

Tương tự như vậy, đối với các điều kiện khác. Ansible cũng hỗ hợ các toán tử `!=`, `>`, `<`, `>=`, `<=`. Bên cạnh đó, Ansible cũng hỗ trợ các toán tử kết hợp như `AND` và `OR`
<a name='Booleanconditional'></a>
## 5.4. Boolean Conditional 
Ngoài so sánh các string, Ansible cũng cho phép kiểm tra xem một biến là `True` hay `False`. Loại điều kiện này giúp bạn kiểm tra xem một biến có được định nghĩa hay không.

Dưới đây là một ví dụ:
```
- hosts: servers
  remote_user: foo
  vars:
     backup: True
  tasks:
	- name: Copy the crontab in tmp if the backup variable is true
	  copy:
		src: /etc/crontab
		dest: /tmp/crontab
		remote_src: True
	  when: backup
```
Kết quả hiển thị ra màn hình sau khi chạy playbook này như sau:
```
$ ansible-playbook -i inventory playbooks/boolean_conditional.yml

PLAY [all] ********************************************************************

TASK [Gathering Facts] ********************************************************
ok: [192.168.1.192]

TASK [Copy the crontab in tmp if the backup variable is true] *****************
changed: [192.168.1.192]

PLAY RECAP ********************************************************************
192.168.1.192              : ok=2    changed=1    unreachable=0    failed=0
```
Trong trường hợp set lại `backup: False` thì output như sau:
```
$ ansible-playbook -i inventory playbooks/boolean_conditional.yml

PLAY [all] ****************************************************************

TASK [Gathering Facts] ****************************************************
ok: [192.168.1.192]

TASK [Copy the crontab in tmp if the backup variable is true] **************
skipping: [192.168.1.192]

PLAY RECAP *****************************************************************
192.168.1.192              : ok=1    changed=0    unreachable=0    failed=0
```
Như vậy, task thứ hai đã bị skip do `backup` được set là `False`.

**Note:** Trường hợp biến không được định nghĩa, Asible sẽ coi giá trị của nó là `False`.

Dưới đây là ví dụ để kiểm tra trong trường hợp biến không được định nghĩa và biến được định nghĩa. Playbook có nội dung như sau:
```
- hosts: all
  remote_user: ansible
  vars:
	backup: True
  tasks:
	- name: Check if the backup_folder is set
	  fail:
		 msg: 'The backup_folder needs to be set'
	  when: backup_folder is not defined

    - name: Copy the crontab in tmp if the backup variable is true
	  copy:
		 src: /etc/crontab
		 dest: '{{ backup_folder }}/crontab'
		 remote_src: True
	  when: backup
```
Bây giờ chúng ta sẽ chuyển sang một khái niệm khác rất thường xuyên được sử dụng trong các project lớn của Ansible đó là **include**
 <a name='include'></a>
## 5.5. Include
Ansible hỗ trợ **include** để giúp chúng ta giảm số lượng code phải viết lặp lại nhiều lần, tăng khả năng tái sử dụng code trong Ansible. Tính năng này giúp chúng ta đảm bảo được nguyên lý **DRY (DON'T REPEAT YOURSELF) **.

Để tích hợp một file khác vào playbook, chúng ta sẽ thực hiện đặt dòng sau dưới các task object:
```
- include: FILENAME.yml
```
Chúng ta cũng có thể truyền một số biến đến file được include. Chúng ta sẽ thực hiện như sau:
```
- include: FILENAME.yml variable1='value1' variable2='value2'
```
Chúng ta cũng có thể thêm điều kiện cho việc include. Ví dụ, chúng ta sẽ include file `RedHat.yml` nếu OS của remote host là `RedHat`:
```
- name: Include the file only for Red Hat OSes
  include: redhat.yaml
  when: ansible_os_family == "RedHat"
```
Chúng ta sẽ tiếp tục nói đến **include** trong phần **handler** sau đây.
<a name='handler'></a>
## 5.6. Handler 
Trong nhiều trường hợp, bạn có một task hoặc một danh sách các task làm thay đổi tài nguyên trên remote host, và để các task này có hiệu lực thì phải kích hoạt một sự kiện nào đó. Cho ví dụ, khi chúng ta thay đổi cấu hình của một service thì chung ta cần restart service đó. Ansible có thể kích hoạt sự kiện restart service đó bằng hành động `notify`.

Mọi handler task sẽ chạy cuối cùng trong playbook, nếu như có thông báo, tức là có hành động `notify` gọi đến.

**NOTE:** Ansible chỉ chạy mỗi handler task **duy nhất một lần** ở cuối playbook **nếu như nhận được thông báo**. Có nghĩa là có thể có nhiều task thông báo đến handler task, nhưng handler task cũng chỉ chạy duy nhất một lần sau khi các task của playbook đã thực hiện xong.

Bây giờ, hãy xem xét ví dụ sau, chúng ta muốn có các task sau:
- Đảm bảo httpd package được cài đặt trên remote host.
- Đảm bảo httpd service được enable và start
- Đảm bảo HTTP đi qua được firewall
- Đảm bảo HTTPd configuration được update

Chúng ta có playbook để thực hiện các task trên như sau:
```
- hosts: webserver
  remote_user: ansible
  tasks:
    - name: Ensure the HTTPd package is installed
      yum:
         name: httpd
         state: present
      become: True
    - name: Ensure the HTTPd service is enabled and running
      service:
         name: httpd
         state: started
         enabled: True
      become: True
    - name: Ensure HTTP can pass the firewall
      firewalld:
         service: http
         state: enabled
         permanent: True
         immediate: True
      become: True
    - name: Ensure HTTPd configuration is updated
      copy:
         src: website.conf
         dest: /etc/httpd/conf.d
      become: True
      notify: Restart HTTPd

  handlers:
    - name: Restart HTTPd
      service:
         name: httpd
         state: restarted
      become: True
```

Như vậy là trong ví dụ trên, chúng ta đã `handlers` để restart HTTPd service sau khi các cấu hình của service này được cập nhật. Chạy playbook này và kết quả thu được như sau:
```
$ ansible-playbook -i inventory playbooks/handler.yml

PLAY [servers]*************************************************************

TASK [Gathering Facts]*****************************************************
ok: [192.168.1.192]

TASK [Ensure the HTTPd package is installed]*******************************
ok: [192.168.1.192]

TASK [Ensure the HTTPd service is enabled and running] ********************
ok: [192.168.1.192]

TASK [Ensure HTTP can pass the firewall]***********************************
ok: [192.168.1.192]

TASK [Ensure HTTPd configuration is updated] ******************************
changed: [192.168.1.192]

RUNNING HANDLER [Restart HTTPd]********************************************
changed: [192.168.1.192]

PLAY RECAP ****************************************************************
192.168.1.192              : ok=6    changed=2    unreachable=0    failed=0
```
Trong output, chúng ta có thể thấy handler `Restart HTTPd` đã được kích hoạt từ việc thay đổi cấu hình của task `Ensure HTTPd configuration is updated`. Tiếp tục thực hiện chạy playbook này lần 2, kết quả sẽ thu được như sau:
```
$ ansible-playbook -i inventory playbooks/handler.yml

PLAY [servers] **************************************************************

TASK [Gathering Facts] ******************************************************
ok: [192.168.1.192]

TASK [Ensure the HTTPd package is installed] ********************************
ok: [192.168.1.192]

TASK [Ensure the HTTPd service is enabled and running] **********************
ok: [192.168.1.192]

TASK [Ensure HTTP can pass the firewall] ************************************
ok: [192.168.1.192]

TASK [Ensure HTTPd configuration is updated] ********************************
ok: [192.168.1.192]

PLAY RECAP ******************************************************************
192.168.1.192              : ok=5    changed=0    unreachable=0    failed=0
```

Do cấu hình không thay đổi sau khi thực hiện task `Ensure HTTPd configuration is updated` nên handler không được thông báo, suy ra handler không được thực thi. Theo mặc định, các handler chỉ chạy một lần tại thời điểm cuối playbook cho dù được thông báo nhiều lần từ các task trong playbook.
<a name='role'></a>
## Chương 6: Role 
Cho đến bây giờ chúng ta đã có thể tạo được các playbook phức tạp, tuy nhiên vẫn chưa giải quyết được tất cả các vấn đề. Trong môi trường sản xuất thực tế, nhưng project ansible thực sự rất lớn so với những gì chúng ta tìm hiểu ở đâu, do đó, việc tổ chức các playbook, các variable file, các host file, ... là rất quan trọng. Để giải quyết vấn đề này, ansible đã cung cấp cho chúng ta một khái niệm đó là **role**.

**Role** được định nghĩa một cách đơn giản là một tập các playbook, các template, các file hoặc là các variable nhằm thực hiện một mục đích cụ thể nào đó. Mục đích đó cài đặt, và cấu hình một service, một application. Cho ví dụ, chúng ta có thể có database role, web server role,...

Trước khi đi vào role, chúng ta sẽ thảo luận về cách tổ chức một project trong thực tế đối với các dự án lớn.
## 6.1. Tổ chức project
Có khá nhiều template khác nhau để tổ chức nên một project dễ quản lý. Trong tài liệu này, chúng ta sẽ tìm hiểu về một template hay được sử dụng.

Đầu tiên, tạo ra một folder, nơi chứa tất cả project của bạn:
```
$ mkdir my_project
$ cd my_project
```
Tiếp theo, chúng ta sẽ tạo ra 3 file với các chức năng như sau:
- **ansible.cfg**: Đây là một file cấu hình của Ansible để chỉ ra nơi tìm ra các file trong cấu trúc project của chúng ta.
- **inventory**: Đây là inventory mà chúng ta đã nói đến ở chương trước.
- **master.yml**: Là một playbook dùng để sắp xếp toàn bộ toàn bộ cấu trúc project.

Tiếp theo, chúng ta tạo ra thêm các folder sau cùng folder với 3 file vừa được tạo ra với từng chức năng như sau:
- **playbooks**: Folder này sẽ chứa các playbook. Trong folder này, tạo thêm `groups` folder để quản lý các groups host.
- **roles**: Folder này chứa các role mà chúng ta cần.
- **group_vars**: Chứa các group variable file được nói đến ở chương trước.
- **host_vars**: Chứa các host variable file được nói đến trong chương trước.

Và đây là cấu trúc project chúng ta thu được:
```
├── ansible.cfg
├── group_vars
│   ├── database
│   └── servers
├── host_vars
│   ├── host1
│   └── host2
├── inventory
├── master.yml
├── playbooks
│   ├── firtrun.yml
│   └── groups
│       ├── database.yml
│       └── webserver.yml
└── roles
    ├── common
    │   ├── files
    │   ├── tasks
    │   └── templates
    └── database

10 directories, 10 files
```
Trong cấu trúc trên, chúng ta để ý trong folder `roles` có folder `common`. Đây là common role rất hữu ích để chứa tất cả hoạt động cần được thực hiện trên mỗi host. Ví dụ, các dịch vụ NTP, motd được định nghĩa trong role này.

## 6.2. Role
Cấu trúc của các folder trong role là không được thay đổi, chúng bắt buộc có một cấu trúc chuẩn.

Folder quan trọng nhất trong mỗi role là folder **tasks**, vì đây là folder bắt buộc. Trong folder **tasks** này, chứa một file **main.yml** có nhiệm vụ liệt kê các task sẽ được thực hiện. Ngoài ra, chúng ta thường hay định nghĩa thêm các folder khác chẳng hạn folder `template` được dùng để lưu trữ các template cho `template` module; folder `files` sẽ chứa các file cho `copy` module.

Bây giờ, hãy xem xét cách chuyển các playbook mà chúng ta sử dụng để thiết lập cơ sở hạ tầng web (có playbook đó là `common_tasks.yml`,`firstrun.yml` và `webserver.yml` )để phù hợp với cấu trúc file của project. Chúng ta cũng sử dụng một số file bổ sung cho `template` và `copy` module, các file này cũng cần được chuyển đến một folder phù hợp trong cấu trúc project này.

Đầu tiên, chúng ta chuyển playbook `firstrun.yml` bằng cách copy vào `playbooks` folder. Chú ý rằng, đây vẫn là một playbook vì chúng ta không thay đổi nội dung của file `firstrun.yml`.

Cho đến lúc này, cấu trúc của project như sau:
```
├── ansible.cfg
├── group_vars
│   ├── database
│   └── servers
├── host_vars
│   ├── host1
│   └── host2
├── inventory
├── master.yml
├── playbooks
│   ├── firtrun.yml
│   └── groups
│       ├── database.yml
│       └── webserver.yml
└── roles
    ├── common
    │   ├── files
    │   ├── tasks
    │   └── templates
    └── database

10 directories, 10 files
```
Chúng ta sẽ tạo ra `main.yml`  với nội dung như sau:
```
- name: Ensure EPEL is enabled
  yum:
     name: epel-release
     state: present
  become: True
- name: Ensure libselinux-python is present
  yum:
     name: libselinux-python
     state: present
  become: True
- name: Ensure libsemanage-python is present
  yum:
     name: libsemanage-python
     state: present
  become: True
- name: Ensure we have last version of every package
  yum:
     name: "*"
     state: latest
  become: True
- name: Ensure NTP is installed
  yum:
     name: ntp
     state: present
  become: True
- name: Ensure the timezone is set to UTC
  file:
     src: /usr/share/zoneinfo/GMT
     dest: /etc/localtime
     state: link
  become: True
- name: Ensure the NTP service is running and enabled
  service:
     name: ntpd
     state: started
     enabled: True
  become: True
- name: Ensure FirewallD is installed
  yum:
     name: firewalld
     state: present
  become: True
- name: Ensure FirewallD is running
  service:
     name: firewalld
     state: started
     enabled: True
  become: True
- name: Ensure SSH can pass the firewall
  firewalld:
     service: ssh
     state: enabled
     permanent: True
     immediate: True
  become: True
- name: Ensure the MOTD file is present and updated
  template:
     src: motd
     dest: /etc/motd
     owner: root
     group: root
     mode: 0644
  become: True
- name: Ensure the hostname is the same of the inventory
  hostname:
     name: "{{ inventory_hostname }}"
  become: True
```
Như bạn có thể thấy, đây là playbook tương tự như playbook `common_task.yml`. Nó chỉ có 2 điểm khác biệt sau:
- Các dòng: `hosts, remote_user` và `tasks` đã bị xóa.
- Thay đổi lại để các dấu thụt dòng hợp lệ.

Trong role này, chúng ta đã sử dụng một `template task` để tạo ra một `motd` file trên remote host với IP của remote host và một số thông tin bổ sung. Để làm được điều này, chúng ta tạo ra file `motd` trong folder `roles/common/templates`.

Tại thời điểm này, folder **roles** có cấu trúc như sau:
```
├── common
│   ├── files
│   ├── tasks
│   │   └── main.yml
│   └── templates
│       └── motd
└── database

5 directories, 2 files
```
Bây giờ, chúng ta cần hướng dẫn ansible biết những host nào cần phải thực hiện tất cả task đã được xác định trong `common` role. Để làm điều này, chúng ta hãy nhìn vào folder `/playbooks/groups`. Trong folder này, chúng ta sẽ tạo ra các file được cho mỗi một group các host cùng thực hiện một hoạt động chẳng hạn như group các host thực thi database và group các host thực thi web server.

Tạo ra một file `database.yml` trong thư mục `playbooks/groups` với nội dung sau:
```
- hosts: database
  user: ansible
  roles:
    - common
```

Tạo ra một file `webserver.yml` trong cùng thư mục `playbooks/groups` với nội dung sau:
```
- hosts: webserver
  user: ansible
  roles:
    - common
```
Như chúng ta có thể thấy, các file này xác định group các host mà chúng ta muốn thực hiện các task, xác định remote user và các role mà chúng ta muốn thực thi.
## 6.3. Các file hỗ trợ
Trong các ví dụ ở các chương trước, chúng ta đã tạo ra các `inventory` file để chứa thông tin của các remote host muốn kết nối đến. Khi chạy câu lệnh `ansible-play`, chúng ta cần xác định đường dẫn đến `inventory` file này thông qua tùy chọn `-i`. Tuy nhiện, việc này sẽ không cần thực hiện khi chúng ta tạo ra một file là `ansible.cfg` để nói cho ansible biết ví trị của `inventory` file. Dưới đây là nội dung của một file `ansible.cfg`:
```
[default]
hostfiles = inventory
host_key_checking = False
roles_path= roles
```
Những tham số và thứ tự độ ưu tiên của các file cấu hình của ansible đã được nói đến ở trong chương đầu tiên. `hostfiles` là đường dẫn đến `inventory` file. `host_key_checking` là xác định xem có cần xác minh SSH key của remote host không. `roles_path` được xác định đường dẫn đến các role cho các playbook.

Tiếp theo, chúng ta cần có một file `master.yml` để sắp xếp các playbook. Sau đó, chỉ cần chạy môt file `master.yml` này, các playbook được include sẽ được thực thi lần lượt theo thứ tự từ trên xuống dưới. Nội dung của `master.yml` như sau:
```
- include: playbooks/groups/database.yml
- include: playbooks/groups/webserver.yml
```
Tại thời điểm này, chúng ta đã có thể thực thi được với câu lệnh sau:
```
$ ansible-playbook master.yml
```
