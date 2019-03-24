import sys
sys.path.append("..")
from http_client import  HttpClient

Hc = HttpClient()
print(hc.get_headers())
hc.set_headers("name","zhang")
r = Hc.get("http://www.baidu.com")
print(hc.get_headers())

