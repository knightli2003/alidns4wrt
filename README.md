# alidns4wrt
##功能介绍
用于动态更新阿里云解析DNS, 只有一个py文件，不依赖于阿里的sdk, 适合在openwrt, Tomato, AdvancedTomato,merlin 等固件里运行

##使用方法
    #修改upddns.py中的以下3个参数
    access_key_id = "HPL9DJpRus8xMAL6"                       #阿里云的Access Key ID
    access_key_secret = "DLLhR72K7vHa9AHEk85EEAPhY9cjuS"     #阿里云的	Access Key Secret
    record_id = "82461988"                                   #域名的RecordId

##参考文档
阿里云dns-api文档

http://docs-aliyun.cn-hangzhou.oss.aliyun-inc.com/pdf/dns-api-reference-cn-zh-2016-06-01.pdf?spm=5176.doc29739.3.3.o4lMY8&file=dns-api-reference-cn-zh-2016-06-01.pdf
