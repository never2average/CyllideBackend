import requests
msg91_authkey = "298553AuLXaKEOL5da1d7d7"
phone_num = 9773065092
message = "chamar saale somil"
req = requests.get(
    "http://api.msg91.com/api/sendhttp.php?country=91" +
    "&sender=CYLLID" + "&route=4" + "&mobiles=" + str(phone_num) +
    "&authkey=" + msg91_authkey + "&message=" + message
)
print(req.status_code)
