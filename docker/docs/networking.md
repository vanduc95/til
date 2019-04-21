Tài liệu này cung cấp cái nhìn tổng quát về networking trong contrainer. Mô tả các network được tạo mặc định và làm thế nào để tự tạo một network (user-defined networks). Ngoài ra tài liệu còn hướng dẫn cách kết nối giữa Docker container và host, giữa các container với nhau.
# Basic Containner Networking
Network của docker được quản lí thông qua một virtual bridge gọi là ```docker0``` là một network độc lập, tách biệt với môi trường khác.

Khi chúng ta cài đặt Docker, những thiết lập sau sẽ được thực hiện:
 - Virtual bridge ```docker0``` sẽ được tạo ra
 - Docker tìm một subnet chưa được dùng trên host và gán một địa chỉ cho ```docker0```

Sau đó, khi chúng ta khởi động một container (với bridge network), một ```veth``` (Virtual Ethernet) sẽ được tạo ra nối 1 đầu với ```docker0``` và một đầu sẽ được nối với interface ```eth0``` trên container. 
<img src="http://i.imgur.com/aNSJ69y.png">

# Default Networks
Khi cài đặt Docker, nó sẽ tự động tạo ra 3 networks. Bạn có thể liệt kê ra các network này bằng cách sử dụng lệnh ```docker network ls```
```sh
$ docker network ls
NETWORK ID          NAME                DRIVER
7fca4eb8c647        bridge              bridge
9f904ee27bf5        none                null
cf03ee007fb4        host                host
```
Mặc định, khi tạo một container, Docker daemon kết nối chúng với network ```bridge```. Tuy nhiên ta có thể tự thiết lập network với câu lệnh ```docker run --net=<NETWORK>```.
## None Network
Các container thiết lập network này sẽ không được cấu hình mạng. Điều này có ích khi container đó không cần đến mạng hoặc nếu bạn muốn tự mình thiết lập mạng cho nó. 
## Host Network
Nếu dùng ```--net=host``` thì các container sẽ sử dụng mạng của máy chủ, điều này có thể sẽ gây nguy hiểm. Nó cho phép bạn có thể thay đổi ```host network``` ở trong container. Và khi bạn chạy ứng dụng với quyền root ở trong container, nó sẽ có nguy cơ điều khiển từ xa tới các máy chủ thông qua các container. 

Nói chung, ta không nên sử dụng cấu hình này vì lí do an ninh, nhưng nó có thể hữu ích khi ta cần hiệu suất mạng tốt nhất bởi vì nó là nhanh nhất.
## Bridge Network
Network ```bridge``` là default network trong Docker.

Chúng ta có thể xem thông tin chi tiết về network ```bridge``` bằng cách sử dụng câu lệnh:
```sh
$ docker network inspect bridge
```
Network ```bridge``` được đại diện bởi ```docker0``` trong cấu hình ```ifconfig```. Khi thêm một container, chúng sẽ có một địa chỉ IP có cùng dải mạng với ```docker0```
```sh
$ ifconfig

docker0   Link encap:Ethernet  HWaddr 02:42:47:bc:3a:eb  
          inet addr:172.17.0.1  Bcast:0.0.0.0  Mask:255.255.0.0
          inet6 addr: fe80::42:47ff:febc:3aeb/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:9001  Metric:1
          RX packets:17 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:1100 (1.1 KB)  TX bytes:648 (648.0 B)
```
Điều này cho phép các container có thể giao tiếp được với máy host cũng như giao tiếp được với các container khác trên cùng 1 host.

Để xem thông tin chi tiết về một network, ta dùng lệnh ```docker network inspect <name_network>```, nó sẽ trả về thông tin dưới dạng 1 file json.

Với các ```default network```, chúng ta chỉ có thể liệt kê và inspect mà không thể xóa chúng. Chúng là mặc định khi cài Docker. Tuy nhiên có thể tự tạo một ``` user-defined networks```, nó có thể remove khi bạn không cần đến nó nữa.
# User-defined networks
Ngoài sử dụng ```default network```, chúng ta có thể tự tạo cho mình một network riêng. Tính năng này cho phép các container độc lập tốt hơn. Ta có thể tạo ra bridge network hoặc overlay network. Trong bài viết này, mình chỉ trình bày cách tạo ra một bridge network.
Để tạo một bridge network, ta sử dụng câu lệnh ```docker network create <name_network>```
```sh
$ docker network create demo 
1196a4c5af43a21ae38ef34515b6af19236a3fc48122cf585e3f3054d509679b
```
Ở ví dụ trên, Docker tự tạo 1 subnet cho network mới này, chúng ta cũng có thể quy định subnet cho nó với option ```--subnet ```
```sh
$ docker network create --subnet 172.25.0.0/16 test 
06a62f1c73c4e3107c0f555b7a5f163309827bfbbf999840166065a8f35455a8
```
Sau khi tao xong network, bạn có thể chạy 1 container trên network mới tạo này bằng cách sử dung ```docker run --net=<NETWORK>``` option.
```sh
$ docker run --network=isolated_nw -itd --name=container3 busybox
8c1a0a5be480921d669a073393ade66a3fc49933f08bcc5515b37b8144f6d47c
```
# Kết nối container với host
Để kết nối từ network ở ngoài vào container thì chúng ta cần phải mapping port của máy host với port mà container expose mà thông qua docker0.

Ví dụ chúng ta muốn map port 8080 của máy host vào port 80 trên container, ta sử dụng apache2 để minh họa
```sh
$ docker run -it -p 8080:80 ubuntu:14.04
```
Ngoài ra có vài cách khác để bạn có thể cấu hình trên ```-p``` flag. Bởi theo mặc định, ```-p``` flag sẽ mapping port quy định đến tất cả interface trên máy host. Nhưng ta có thể quy định chỉ mapping đến interface mà ta muốn, ví dụ như ```localhost```
```sh
$ docker run -it -p 172.0.0.1:8080:80 --name apache ubuntu:14.04
```
hoặc 
```sh
$ docker run -it -p 172.0.0.1::80 ubuntu:14.04
```
để container tự động mapping đến một port bất kì trên host.

Sau đó attach tới container
```sh
$ docker attach apache
```
Cài apache2 và bắt đầu dịch vụ
```sh
$ apt-get update
$ apt-get install apache2
$ /etc/init.d/apache2 start
```
Deattach khỏi container sử dung ```CTRL P + CTRL Q```

Cuối cùng ta có thể kiểm tra bằng cách thử curl trên máy host
```sh
$ curl localhost:8080
```
Nếu kết quả trả về 1 file html apache thì bạn đã cấu hình thành công

# Kết nối các container trên cùng một host
Trên cùng một host, các container chỉ cần dùng bridge network để nói chuyện với nhau. Do các IP của container được cấp phát động nên việc sử dụng nó không được thuận lợi. Ta có thể dùng hostname để giải quyết vấn đề này, khi IP thay đổi cũng không làm mất các dịch vụ chạy trên các container khác nhau.

Trong bài viết này sẽ trình bày 2 phương thức để kết nối các container với nhau, đó là sử dụng default bridge network và sử dụng user-defined bridge network
### Trường hợp sử dụng default bridge network để kết nối các container
Trong default bridge network, chúng ta chỉ có thể ping tới 1 container khác cùng host thông qua địa chỉ IP mà không thể sử dụng hostname. Để giải quyết điều này, ta có giải pháp đó là dùng ```link```

Giả sử có mô hình web - db. Ở đây từ container web phải connect được đến db. Đặt tên cho từng container. Sau đó link theo tên, phải đảm bảo container được link phải tồn tại. Do đó phải run theo thư tứ db -> web.
```sh
docker run -itd --name=db -e MYSQL_ROOT_PASSWORD=pass mysql:latest
docker run -itd --name=web --link=redis --link=db nginx:latest
docker attach web
# ping db
PING db (172.17.0.2): 56 data bytes
64 bytes from 172.17.0.2: icmp_seq=0 ttl=64 time=0.126 ms
...
```
Lý do web container liên lạc được db qua name là nhờ docker engine đã tự set thông tin link vào /etc/hosts của web container:
```sh
# cat /etc/hosts
172.17.0.2  db 158aed2b8df9
```
Nhược điểm của phương pháp này là nó chỉ có một chiều, nghĩa là từ db bạn không thể ping được đến web. Vì vậy phải định nghĩa rõ chiều kết nối, phải đảm bảo start container theo đúng thứ tự.

## Trường hợp sử dụng user-defined bridge network để kết nối các container
Ngược lại với default bridge network, user-defined bridge network có thể ping bằng hostname mà không cần cấu hình gì.
```sh
docker network create my-net
docker network ls
NETWORK ID          NAME                DRIVER
716f591e185a        bridge              bridge              
4b0041303d6d        host                host                
7239bb9e0255        my-net              bridge              
016cf6ec1791        none                null

docker run -itd --name=web1 --net my-net nginx:latest
docker run -itd --name=db1 --net my-net -e MYSQL_ROOT_PASSWORD=pass mysql:latest

docker attach web1
# ping db1
PING db1 (172.18.0.4): 56 data bytes
64 bytes from 172.18.0.4: icmp_seq=0 ttl=64 time=0.161 ms
```
Ngoài ra nó còn có thể kết nối được 2 chiều, nghĩa là từ db1 bạn vẫn có thể ping đến web1

## Tài liệu tham khảo
https://docs.docker.com/engine/userguide/networking/work-with-networks/

https://docs.docker.com/engine/userguide/networking/default_network/dockerlinks/

http://www.linuxjournal.com/content/concerning-containers-connections-docker-networking?page=0,0

https://deis.com/blog/2016/connecting-docker-containers-1/

http://kipalog.com/posts/Co-ban-ve-docker-network