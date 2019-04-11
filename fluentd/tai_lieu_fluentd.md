# Logging với Fluentd verison v1.x

## 1. Fluentd là gì?
Fluentd là một open-source và free cho phép thu thập và xử lý dữ log hiệu quả.

Fluentd được viết bằng Ruby và C nên sử dụng ít tài nguyên, khả năng scale tốt.

![](./images/fluentd-overview.png)

## 2. Kiến trúc tổng quan của Fluentd

Fluentd sẽ định dạng dữ liệu về dạng JSON, điều này cho phép fluentd có thể thống nhất tất cả các thao tác trong việc xử lý dữ liệu log: collecting (thu thập), lọc (filtering), ghi vào bộ nhớ đệm (buffering) và xuất dữ liệu (outputting) ra nhiều destination khác nhau.

Dưới đây là quá trình mà một event log được xử lý bởi fluentd.

![](./images/architecture.png)

Hình trên mô tả quá trình mà một event sẽ được xử lý.
- **Input** thu thập các event log từ các resource như `file`, `http`...Các event log này sau khi đi qua input plugin có định dạng Json gồm 3 phần: `time`, `tag` và `record`. Đây là một ví dụ về event log:

```
2019-04-04 10:01:15 +0000 example.tag: {"action":"login","user":42} 
```
- **Engine (filter)** xử lí event log từ input gửi đến. Đó là một chuỗi các rule filter được áp dụng tới mỗi event log.
- Cuối cùng event log có thể đưọc lưu trữ trong buffer (file hoặc memory) và gửi đến các **Output** dựa vào `tag`. 

## 3. Cài đặt Fluentd với Docker
Mục này sẽ hướng dẫn cài đặt Fluentd bằng Docker để tiếp nhận các record từ http, sau đó output tới stdout.

- Tạo file `/tmp/fluent.conf`
```
$ vi /tmp/fluent.conf
<source>
  @type http
  port 9880
  bind 0.0.0.0
</source>
<match **>
  @type stdout
</match>
```
- Cài Fluentd với câu lệnh `docker run`. 
```
$ docker run -p 9880:9880 -v /tmp:/fluentd/etc fluent/fluentd:v1.3-debian
2019-04-03 15:49:29 +0000 [info]: parsing config file is succeeded path="/fluentd/etc/fluent.conf"
2019-04-03 15:49:29 +0000 [info]: using configuration file: <ROOT>
  <source>
    @type http
    port 9880
    bind "0.0.0.0"
  </source>
  <match **>
    @type stdout
  </match>
</ROOT>

```
- Đẩy một sample log thông qua HTTP để verify
```
$ curl -X POST -d 'json={"json":"message"}' http://localhost:9880/sample.test
```
- Kết quả trong docker log
```
2019-04-03 15:49:54.361742463 +0000 sample.test: {"json":"message"}
```

## 4. Cấu hình của Fluentd

### Cấu trúc thư mục cấu hình cơ bản
Tất cả quá trình xử lý này đều có thể được định nghĩa trong các file cấu hình. Đối với trường hợp fluentd phức tạp (nhiều source, filter và destination), một best practice có thể được áp dụng như sau:

```
├── conf
│   ├── filter
│   │   ├── 00-rewrite-syslog.conf
│   │   ├── 01-record-transformer-syslog.conf
│   │   ├── 02-parser-syslog.conf
│   │   └── 03-record-transformer.conf
│   ├── input
│   │   ├── 00-access.conf
│   │   ├── 01-tomcat.conf
│   │   └── 02-syslog.conf
│   ├── output
│   │   └── 00-es.conf
│   └── fluent.conf
└── docker-compose.yml
```
Theo cấu trúc này, project sẽ được tổ chức như sau:
- `docker-compose.yml` là script để chạy fluentd theo docker.
- Thư mục conf chứa các file cấu hình cho project.
  - td-agent.conf là file cấu hình chính của fluentd. File này sẽ sử dụng @include để import tất cả các file cấu hình khác từ các folder con là filter/input/output
  - Thông tin các đối tượng input, filter, output sẽ được định nghĩa trong các folder tương ứng.

Ví dụ về file td-agent.conf:

```
# cat conf/td-agent.conf 
@include input/*.conf
@include filter/*.conf
@include output/*.conf
```

Như vậy, khi chạy, fluentd sẽ đọc cấu hình từ file td-agent.conf theo thứ tự từ trên xuống inpute --> filter --> output. Đầu tiên sẽ đọc cấu hình từ folder input, để xác định các resource cần tổng hợp log. Sau đó là folder filter cho việc xử lý log, nơi chứa các rule filter, rule parser. Và cuối cùng, folder output là các destination cần gửi output log sau khi được xử lý.

Xem chi tiết trong folder `lab`

### Routing event


### Config: Các tham số thông dụng

### Config: Parse Section

### Config: Buffer Section

### Config: Format Section



## 5. Tìm hiểu về Input Plugins cơ bản.

### Tổng quan
Input plugin chịu trách nhiệm retrieve và pull event logs từ các source. Một input plugin thông thường tạo một thread socket và một listen socket. Ngoài các input plugin có sẵn, ta cũng có thể tự viết một plugin để pull data từ source mà mình định nghĩa. 

Fluentd hỗ trợ một số input plugin sau:
- in_tail
- in_forward
- in_udp
- in_tcp
- in_http
- in_syslog
- in_exec
- in_dummy
- in_windows_eventlog

### in_tail

`in_tail` plugin cho phép Fluentd đọc các event log từ `tail of text file`, tương tự như sử dụng command `tail -F`. 

Khi Fluentd được cấu hình `in_tail`, nó sẽ bắt đầu đọc từ vị trí cuối cùng trong file log. Trong trường hợp Fluentd restart, nó sẽ tiếp tục đọc vị trí cuối cùng trước khi bị restart, vị trí này được lưu trong tham số `pos_file`.

Dưới đây là ví dụ sử dụng `in_tail` plugin:
```
<source>
  @type tail
  format none
  path /fluentd/log/tail.log
  pos_file /fluentd/log/tail.out.pos
  tag tets_tail
</source>

<match test_tail>
  @type stdout
</match>
```

Tham khảo thêm cấu hình trong `00-tail.conf`

### in_syslog

```
<source>
  @type syslog
  port 5140
  bind 0.0.0.0
  tag syslog
</source>
```

Ví dụ trên Fluentd tạo một socket lắng nghe trên port 5140. Để syslog daemon gửi message tới socket này, thêm cấu hình sau tới file `/etc/rsyslog.conf`

```
# Send log messages to Fluentd
*.* @127.0.0.1:5140
``` 

Tham khảo thêm cấu hình trong `01-syslog.conf`


## 6. Tìm hiểu về Output Plugins cơ bản.

### Tổng quan

### out_file

### out_elasticsearch

### out_copy


## 7. Tìm hiểu về Filter Plugins cơ bản.


### Tổng quan

### filter_record_transformer

### filter_grep

### filter_parser


## 8. Tìm hiểu về Parser Plugins cơ bản


### Tổng quan

### parser_regexp

### parser_syslog



## 9. Tìm hiểu về Buffer Plugins


### Tổng quan (Phần này quan trọng vì cần để tuning performace sau này)

### buf_memory

### buf_file



## 10. Trouble Shooting

### Tối ưu hóa hiệu năng