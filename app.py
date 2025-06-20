import os
import ipaddress
from sqlalchemy import text, create_engine
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

if os.getenv('BEHIND_PROXY', '') != '':
  from werkzeug.middleware.proxy_fix import ProxyFix
  n=int(os.getenv('BEHIND_PROXY'))
  app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=n, x_proto=n, x_host=n, x_prefix=n
  )

eng = create_engine("sqlite:///ip.db")

def pad(ip):
  return f'{int(ip):010}' if ip.version == 4 else f'{int(ip):038}'

def lookup_ip(addr):
  ip = ipaddress.ip_address(addr)
  with eng.connect() as c:
    r = c.execute(text(f'''
    select locale, country, continent, network
      from ip
     where '{pad(ip)}' between first_address and last_address
       and version = {ip.version}
    ''')).fetchone()
    l = None
    c = None
    if r is not None:
      (l,c,co,net) = r
      print(f'{addr} <{int(ip)}> is in {c}, on {co} via {net}')
    else:
      print(f'{addr} <{int(ip)}> NOT FOUND')
    return {'a': addr, 'l': l, 'c': c}

@app.route('/check')
def check_ip_implicit():
  return lookup_ip(request.remote_addr)

@app.route('/check/<addr>')
def check_ip_explicit(addr):
  return lookup_ip(addr)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
  return {'e':'nope'}

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
