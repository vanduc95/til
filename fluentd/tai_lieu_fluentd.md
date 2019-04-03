# Logging với Fluentd

## 1. Fluentd là gì?
Fluentd là một open-source và free cho phép thu thập và xử lý dữ log hiệu quả.

Fluentd xử lí các log về định dạng JSON, cho phép Fluentd thống nhất các thao tác trong việc xử lí dữ liệu log: collecting (thu thập), lọc (filtering), ghi vào bộ nhớ đệm (buffering) và xuất dữ liệu (outputting) ra nhiều destination khác nhau.

Fluentd được viết bằng C và Ruby nên sử dụng ít tài nguyên, khả năng scale tốt.

![]](./images/fluentd-overview.png)

## 2. Kiến trúc tổng quan của Fluentd


## 3. Cài đặt Fluentd với Docker

## 4. Cấu hình của Fluentd

### Cấu trúc thư mục cấu hình cơ bản

### Routing event

### Config: Các tham số thông dụng

### Config: Parse Section

### Config: Buffer Section

### Config: Format Section



## 5. Tìm hiểu về Input Plugins cơ bản.


### Tổng quan

### in_tail

### in_syslog



## 6. Tìm hiểu về Output Plugins cơ bản.


### Tổng quan

### out_file

### out_copy

### out_elasticsearch



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