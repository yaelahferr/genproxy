#-*- coding: utf-8 -*-
import socket,re,requests

G = '\033[92m'
Y = '\033[93m'
R = '\033[91m'
B = '\033[94m'
W = '\033[0m'
_G = '\033[32m'


class library(object):


      def __init__(
          self,
          proxy,
          port,
          host,
          method,
          delay,
          country = None,
          level = None
          ):
          
          self.proxy = proxy
          self.port = port
          self.host = host
          self.method = method
          self.delay = delay
          self.country = country
          self.level = level
          
          
      def check(self):
          _s = socket.socket(
                  socket.AF_INET, socket.SOCK_STREAM
                  )
          _s.settimeout(int(self.delay))
          try:
              _s.connect((self.proxy,int(self.port)))
              data = f'{self.method.upper()} {self.host}  HTTP/1.0\r\nConnection: keep-alive\r\n\r\n'
              _s.send(bytes(data,encoding='utf-8'))
              resp = _s.recv(9000).split(b"\r\n")[0]
              x = resp.decode('utf-8')
              print(f'[Method]    :{G} {self.method}{W}')
              print(f'[Proxy]     :{B} {self.proxy}:{W}{self.port}')
              print(f'[Host]      :{_G} {self.host}{W}')
              print(f'[Anonymity] :{Y} {self.level}{W}')
              print(f'[Country]   :{R} {self.country}{W}')
              if x in ['HTTP/1.0 200 OK','HTTP/1.1 200 OK','unknown 200 OK','HTTP/1.1 200 Connection established', 'HTTP/1.0 200 Connection established']:
                 print(f'[status]    :{G} {x}{W}')
                 print(f'[saveTo]    : {self.host}_result.txt')
                 print('\n')
                 f = open(f'{self.host}_result.txt','a+')
                 f.write(f'{self.proxy}:{self.port}\n')
                 f.close()
              else:
                 print(f'[status]    :{Y} {x}{W}')
                 print('\n')
          except Exception as e:
              print(f'\n{R}[!]{W} {e}\n')


             
      @classmethod
      def _get_proxy(self):
          data = {}
          r = requests.get("https://free-proxy-list.net")
          data['proxy']   = re.findall(r"\d+\.\d+\.\d+\.\d+",r.text)
          data['port']    = re.findall(r"\**<td>\d+</td>",r.text)
          data['level']   = re.findall("class='hm'>\D+</td><td>(\D.+?)</td>",r.text)
          data['country'] = re.findall(r'td>(\w{2})</',r.text)
          return data
          

class host_search(object):

      data = []

      def __init__(self,domain):
          self.domain = domain
          self.site = 'https://dnsdumpster.com/'

     
      def request(self):
          get_token = requests.get(
                      f'{self.site}',
          ).text
          token = re.findall("value=\'(.*?)\'",get_token)[0]
          req = requests.post(
                f'{self.site}',
                cookies = {'csrftoken':token },
                data = {
                        'csrfmiddlewaretoken': token, 
                        'targetip': self.domain
                        },
                headers = {'Referer':self.site }
          )
          for host in re.findall('http://(.*?)"',str(req.text)):

              host_search.data.append(host)
          return host_search.data



