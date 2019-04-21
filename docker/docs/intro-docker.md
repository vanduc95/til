# Ảo hóa truyền thống? (Hypervisor based Virtualization)
Với công nghệ ảo hóa này, ta có thể chạy nhiều hệ điều hành cùng lúc trên một máy. Toàn bộ hệ thống từ phần cứng (RAM,CPU,HDD..) cho đến hệ điều hành đều được "ảo hóa".
<img src="http://i.imgur.com/wFhghgv.png"/>
Tuy nhiên việc ảo hóa nảy sinh các vấn đề sau:
 - Tốn tài nguyên: khi chạy 1 máy ảo, nó sẽ luôn chiếm 1 phần tài nguyên cố định. Vd:máy chủ bạn có 512GB SSD, 16GB RAM. Bạn tạo ra 4 máy ảo Linux, mỗi máy bạn cấp 64GB SSD và 2GB RAM. Như vậy, bạn sẽ mất 256 GB SSD để chứa 4 máy ảo, và khi chạy cùng 4 máy ảo lên cùng lúc, chúng sẽ chiếm 8GB RAM. Mặc dù chỉ chạy lên để không đó thôi, chưa dùng gì cả nhưng nó vẫn chiếm từng đó. 
 - Tốn thời gian thực thi: thời gian khởi động, shutdown của các máy ảo sẽ lâu, thường là hàng phút.
 - Cồng kềnh: việc phải ảo hóa nhiều OS làm server không thể chạy hết hiệu suất.
 
Từ những yếu điểm trên mà công nghệ Operating System/Container Virtualization ra đời.

# Ảo hóa Container (Operating System/Container Virtualization)
Ảo hoá Container còn được gọi là "ảo hoá hệ điều hành" (operating system virtualization). Ở đây, chúng ta không ảo hoá cả phần cứng , hệ điều hành nữa mà chỉ ảo hoá môi trường. Các service trong Container vẫn chạy chung hệ điều hành chủ ở phía dưới, chung Kernel nhưng môi trường chạy của các service thì luôn được đảm bảo hoàn toàn độc lập với nhau.
<img src="http://i.imgur.com/2YM0QP8.png"/>
Thuật ngữ **Container** ở đây được hiểu là khái niệm đóng gói. Một Container chứa đầy đủ application và tất các các thành phần phụ thuộc như: các file Bins, các thư viện kèm theo để đảm bảo các ứng dụng có thể chạy độc lập trong container đó.
Container có những ưu điểm sau:
 - Hiệu năng cao: Hệ điều hành chủ quản lý các Container bằng Systemd hoặc Upstart. Do vậy, các Container ở đây như là môt process của hệ thống. Chỉ mất vài giây để start, stop hay restart một Container, và khi các container ở trạng thái chò chúng gần như không tiêu tốn tài nguyên CPU. Với một máy tính cấu hình thông thường, nếu chạy máy ảo truyền thống chúng ta chỉ chạy được khoảng vài cái. Tuy nhiên nếu chạy bằng Container chúng ta có thể chạy lên đến vài trăm cái. 
 - Tính di động và tính mở: chúng ta có thể tạo một container từ các image có sẵn, thiết lập các thay đổi trên đó và lưu lại trạng thái mới như một image khác và triển khai image này đến bất kì chỗ nào ta mong muốn.
 
# Docker là gì?
Docker là một open platform để xây dựng, vận chuyển và chạy các ứng dụng. Docker cung cấp cho các lập trình viên, các nhóm phát triển và các kỹ sư những công cụ và service đã được đóng gói (còn gọi là Container) và chạy chương trình của mình một cách độc lập, không tác động đến môi trường hiện tại của máy. Bằng phương thức đóng gói ứng dụng thành các Containers, Docker đem đến sự linh hoạt và thống nhất trong môi trường phát triển, kiểm thử, và vận hành.

## Docker – Build, Ship, and Run Any App Anywhere
Build : Docker cho phép tạo một môi trường linh động và nhất quán cho môi trường phát triển và môi trường vận hành ứng dụng.

Ship : Docker cho phép thiết kế toàn bộ chu kỳ phát triển ứng dụng, thử nghiệm và phân phối, và quản lý nó với một giao diện người dùng phù hợp.

Run : Docker cung cấp khả năng triển khai mở rộng các dịch vụ an toàn và đáng tin cậy trên nhiều nền tảng …

# Docker Engine?
Docker Engine là một ứng dụng client-server với các thành phần chính sau đây:
 - Server hay còn được gọi là Docker daemon- xử lí yêu cầu của users
 - Command line interface (CLI) client.
 - REST API - giao thức để kết nối CLI với service
<img src="http://i.imgur.com/AQn3ZzW.png?2"/>

CLI sử dụng Docker REST API để điều khiển hoặc tương tác với Docker daemon thông qua script hoặc CLI commands.

Docker daemon tạo và quản lí các đối tượng Docker. Đối tượng Docker ở đây bao gồm images, containers, networks, data volumes,...

 
# Kiến trúc của Docker
<img src="http://i.imgur.com/uIjrljq.png?1"/>
## Docker daemon
Như hình trên, Docker daemon chạy trên một máy host. Các user không thể tương tác trực tiếp với deamon mà phải thông qua Docker client.
## Docker client
Docker client là giao diện sử dụng chính của Docker. Nó tiếp nhận các yêu cầu từ người dùng và truyền các yêu cầu đó cho Docker daemon xử lí
## Các thành phần chính của Docker
 - Docker images
 - Docker registries
 - Docker containers

### Docker images
Là một "read-only template". Ví dụ, một image chứa hệ điều hành Ubuntu đã cài đặt sẵn Apache và ứng dụng web. Các images được sử dụng để tạo Docker containers. Docker cung cấp cách đơn giản để build một image mới hoặc bạn có thể download Docker image đã được tạo sẵn trên Docker Hub.
<img src="http://i.imgur.com/joNLpZZ.png"/>
Trên đây là cấu trúc của một image:
 - Mỗi một image gồm một list các **image-layer** cái mà đại diện cho các file của hệ thống. Các layer được xếp chồng lên nhau tạo thành một hệ thống tập tin cơ sở cho một container. Mỗi layer chỉ có thể **read-only** và đều có ID riêng đã được băm mã hóa.
 - Khi tạo một container mới, trong mỗi container sẽ tạo thêm một lớp có-thể-ghi được gọi là **container-layer**. Các thay đổi trên container như thêm, sửa, xóa file... sẽ được ghi trên lớp này. Do vậy, từ một image ban đầu, ta có thể tạo ra nhiều máy con mà chỉ tốn rất ít dung lượng ổ đĩa. ID của các **container-layer** được tạo bằng **Random UUID**
 - Khi một container bị xóa, lớp **container-layer** cũng được xóa theo. Các lớp **image-layer** vẫn được giữ nguyên và không bị thay đổi. Bởi vì mỗi container có lớp **container-layer** của riêng nó, tất cả các thay đổi sẽ được lưu trên đây, điều đó có nghĩa là các container có thể chia sẻ quyền truy cập đến cùng image gốc. 
 <img src="http://i.imgur.com/102XMmL.png"/>
 
### Docker registries
Là kho chứa images. Registries có thể ở dạng public hoặc private tương ứng với việc có thể download image hay không. Docker Hub là một trong những Registries cho phép người dùng có thể upload image và download image về với 2 câu lệnh docker push và docker pull.
### Docker containers
Hoạt động giống như một thư mục (directory), chứa tất cả những thứ cần thiết để một ứng dụng có thể chạy được. Mỗi một docker container được tạo ra từ một docker image. Các thao tác với một container : chạy, bật, dừng, di chuyển, và xóa. Mỗi container là một ứng dụng riêng biệt và được bảo mật.

# Ưu điểm của Docker
 - Triển khai ứng dụng nhanh chóng : container bao gồm các yêu cầu tối thiểu để chạy ứng dụng. Các container này đều dùng chung phần nhân của máy mẹ (host OS) và chia sẻ với nhau tài nguyên của máy mẹ (bộ nhớ RAM, CPU...). Vì vậy việc tận dụng tài nguyên sẽ được tối ưu hơn, hiệu năng sẽ nhanh hơn so với máy ảo
 - Khả năng di chuyển linh động : một ứng dụng và tất cả các phụ thuộc của nó có thể được gói vào một container duy nhất , độc lập với các phiên bản máy chủ của Linux kernel , phân phối nền tảng , hoặc mô hình triển khai.Container này có thể được chuyển sang một máy chạy Docker, và được thực hiện mà không hề có vấn đề tương thích hay không.
 - Kiểm soát phiên bản và tái sử dụng
 - Dễ dàng chia sẻ : với Docker Hub hoặc 1 public Registry việc chia sẻ container rất dễ dàng thực hiện và thân thiện với mọi người kể cả developer, tester, admin system.
 - Nhẹ và chi phí tối thiểu : Docker image thường rất nhỏ , tạo điều kiện cho việc kiểm thử và giao hàng nhanh chóng và giảm thời gian để triển khai các ứng dụng mới container.
 - Bảo trì đơn giản : Docker giảm sự phụ thuộc và nguy hiểm đến từ các ứng dụng phụ thuộc.

# Nhược điểm của Docker
 - Do các Container sử dụng chung kernel với hệ điều hành chủ nên chúng ta chỉ có thể "ảo hoá" được các hệ điều hành mà hệ điều hành chủ hỗ trợ. Ví dụ: Nếu hệ điều hành chủ là nhân Linux thì chúng ta chỉ có thể ảo hoá được các hệ điều hành nhân Linux như Lubuntu, OpenSuse, LinuxMint ... chứ không thể tạo được một container Window được.
 - Việc dùng chung kernel làm docker ít tách biệt hơn so với VM, một lỗi nhỏ trong kernel cũng có thể ảnh hưởng đến tất cả các container.

# Các lệnh cơ bản với Docker
### Pull một image từ Docker Hub
```docker pull {image_name}```
### Tạo một container từ image có sẵn
```docker run {image_name} ```
### Liệt kê các images hiện có
```docker images```
### Xóa một image
```docker rmi {image_id/name}```

Để remove 1 image, hãy đảm bảo rằng không có container nào đang chạy được lấy từ image đó.
### Liệt kê các container đang chạy
```docker ps #Chỉ liệt kê các container đang chạy```

```docker ps -a #Liệt kê tất cả các container, kể cả các container đã tắt```
### Xóa một container
```docker rm {container_id/name}```

Lệnh trên chỉ thực hiện được khi container đó đã stop.

Nếu container đang chạy, bạn cũng có thể xoá nhưng phải thêm tham số -f vào sau rm để remove:

```docker rm -f {container_id/name}```

### Đổi tên một container
```docker rename {old_container_name} {new_container_name}```
### Dừng/Khởi động một container 
```sh
docker stop/start {new_container_name}
docker exec -it {new_container_name} /bin/bash
```
### Build một image từ container
```docker build -t {container_name} .```

Dấu . ở đây ám chỉ Dockerfile đang nằm trong thư mục hiện tại.

### Xem log của container đang chạy
```docker logs -f {image_name}```



