#!/bin/sh

access_key_id=xxxxxxxxxxx
access_key_secret=xxxxxxxxxxxxxxxxxxx
#aliddns_record_id=xxxxxxxxxxx     
aliddns_name1=xxxxxxxxxxx
aliddns_domain=xxxxxxxx.com
aliddns_ttl=600

timestamp=`date -u "+%Y-%m-%dT%H%%3A%M%%3A%SZ"`
ip=`$aliddns_curl 2>&1` || die "$ip"

urlencode() {
    # urlencode <string>
    out=""
    while read -n1 c
    do
        case $c in
            [a-zA-Z0-9._-]) out="$out$c" ;;
            *) out="$out`printf '%%%02X' "'$c"`" ;;
        esac
    done
    echo -n $out
}

enc() {
    echo -n "$1" | urlencode
}

send_request() {
    local args="AccessKeyId=$access_key_id&Action=$1&Format=json&$2&Version=2015-01-09"
    local hash=$(echo -n "GET&%2F&$(enc "$args")" | openssl dgst -sha1 -hmac "$access_key_secret&" -binary | openssl base64)
    curl -v "http://alidns.aliyuncs.com/?$args&Signature=$(enc "$hash")"
}

get_recordid() {
    grep -Eo '"RecordId":"[0-9]+"' | cut -d':' -f2 | tr -d '"'
}

query_recordid() {
    send_request "DescribeSubDomainRecords" "SignatureMethod=HMAC-SHA1&SignatureNonce=$timestamp&SignatureVersion=1.0&SubDomain=$aliddns_name1.$aliddns_domain&Timestamp=$timestamp"
}

update_record() {
    send_request "UpdateDomainRecord" "RR=$aliddns_name1&RecordId=$1&SignatureMethod=HMAC-SHA1&SignatureNonce=$timestamp&SignatureVersion=1.0&TTL=$aliddns_ttl&Timestamp=$timestamp&Type=A&Value=$ip"
}

aliddns_record_id=`query_recordid | get_recordid`
echo $aliddns_record_id
update_record $aliddns_record_id