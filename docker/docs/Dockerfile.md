# Dockerfile
Dockerfile là một kịch bản, bao gồm các câu lệnh liên tiếp nhau được thực hiện tự động trên một image gốc để tạo ra một image mới. Dockerfile giúp đơn giản hóa tiến trình từ lúc bắt đầu đến khi kết thúc.

Dockerfile bắt đầu quy trình với việc xác định một image gốc với câu lệnh **FROM**. Tiếp theo đó là các câu lệnh và tham số khác để cung cấp cho user một image mới được sử dụng cho việc tạo container.

# Dockerfile Systax
Trước khi chúng ta bắt đầu với Dockerfile, ta hãy nói qua về cú pháp trong Dockerfile và điều này thực sự có nghĩa :)

Dockerfile sử dụng cú pháp đơn giản, rõ ràng và dễ sử dụng. Ta có thể comment lên mã nguồn khiến nó dễ hiểu hơn rất nhiều.
## Dockerfile Syntax Example
Cú pháp của Dockerfile bao gồm 2 phần chính: ```comments``` và ```commands + arguments```
```sh
# Line blocks used for commenting
command argument argument ..
```
Ví dụ:
```sh
# Print "Hello docker!"
RUN echo "Hello docker!"
```

# Dockerfile Commands
Chúng ta sẽ tìm hiểu qua về các command cơ bản trước khi làm một ví dụ về Dockerfile
### FROM
**FROM** xác định image cơ bản được sử dụng trong quá trình build. Nó có thể là bất kì image nào, bao gồm cả những image bạn tạo ra trước đó. Nếu image không được tìm thấy trên host, Docker sẽ cố gắng pull image đó về từ Docker Hub.

**FROM** bắt buộc phải là câu lệnh khai báo đầu tiên trong Dockerfile.
```sh
# Usage: FROM <image_name>
   or    FROM <image_name>:<tag>
FROM ubuntu:14.04
```
Khi không có tag thì mặc định nó nhận là "lastest"

### MAINTAINER
Câu lệnh này có thể đặt ở bất cứ đâu trong Dockerfile, nhưng sẽ tốt hơn nếu ta đặt nó sau **FROM**. Câu lệnh không-được-thực-thi này có tác dụng khai báo tác giả của image.
```sh
# Usage: MAINTAINER [name]
MAINTAINER vanduc.bk
```

### ADD & COPY
Lệnh **ADD** và **COPY** gồm 2 tham số: 1 nguồn và 1 đích đến. Về cơ bản nó sao chép các tập tin, thư mục từ ```[src]``` và thêm chúng vào file hệ thống của container tại đường dẫn ```[dest]```
```sh
# Usage: ADD [src] [dest] & COPY [src] [dest]
ADD http://github.com/user/file/ /my_app_folder
COPY hom* /mydir/        # adds all files starting with "hom"
```
KHUYẾN KHÍCH SỬ DỤNG COPY

ADD là 1 phần của Docker ngay từ thời bắt đầu. và hỗ trợ 1 vài chức năng khá thú vị:
 - ADD có thể copy file từ URL : ADD http://foo.com/bar.go /tmp/main.go
 - ADD tự động giải nén với những file : (tar, gzip, bzip2, etc) nhưng với source là local.
 - ADD nếu source là URL và là định dạng nén, ADD chỉ down và đẩy vào, không giải nén

COPY mang đúng nghĩa COPY, file như thế nào copy đúng như thế, và không hỗ trợ URL
Tại sao lại khuyến khích dùng COPY,hạn chế dùng ADD ? Bởi vì khi sử dụng COPY nghĩa của nó mang đúng nghĩa tường minh. ADD quá phức tạp dễ gây nhầm lẫn trong sử dụng. Do đó KHUYẾN KHÍCH SỬ DỤNG COPY.

### RUN
Là câu lệnh chính trên Dockerfile, dùng để chạy các câu lệnh trên image
```sh
# Usage: RUN [command] or RUN [“executable”, “param1”, “param2”] 
RUN [“/bin/bash”, “-c”, “echo hello”]
```
### CMD
Tương tự như RUN, nó cũng chạy các câu lệnh trên image. Tuy nhiên mục đích chính của CMD là cung cấp chạy mặc định cho image, thông thường là các service: apache2, perl, python, php,... Nếu có nhiều câu lệnh CMD thì chỉ có câu lệnh CMD cuối cùng mới được thực thi.
```sh
# Usage: CMD application "argument", "argument", ..
CMD "echo" "Hello docker!"
```
### LABEL
LABEL dùng để gắn metadata vào image. Metadata hay còn gọi là siêu dữ liệu , là tập hợp các phần tử để mô tả nguồn thông tin của images
VD : 1 cuốn sách thì metadata ở đây là tên tác giả, nhan đề, năm xuất bản, …
Với image có thể là Vendor, label-with-value, version, depcription, …
```sh
# Usage: LABEL <key>=<value> <key>=<value> <key>=<value> ...
LABEL "com.example.vendor"="ACME Incorporated"
LABEL com.example.label-with-value="foo"
LABEL version="1.0"
```
### EXPOSE 
EXPOSE dùng để thông báo cho Docker rằng cái container sẽ lắng nghe ở cổng nào (port). Thay vì trong câu lệnh docker sử dụng cờ -p:
```docker run -d -p 80:5000 training/webapp python app.py```
thì sử dụng EXPOSE
```sh
# Usage: EXPOSE [port]
EXPOSE 80
```
### USER
User để thiết lập username hoặc UID để chạy image và cho các câu lệnh RUN, CMD và ENTRYPOINT ở trong dockfile
```sh
# Usage: USER [UID]
USER 751
```
### VOLUME
????
```sh
# Usage: VOLUME ["/dir_1", "/dir_2" ..]
VOLUME ["/my_files"]
```