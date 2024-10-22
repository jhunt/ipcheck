import os
from sqlalchemy import text, create_engine
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

eng = create_engine("duckdb:///:memory:")

@app.route('/check')
def check_ip():
  ipv4 = request.remote_addr.split('.')
  #ipv4 = '66.78.209.135'.split('.')
  with eng.connect() as c:
    r = c.execute(text(f'''
    select country
      from read_csv('ipv4.csv')
     where {ipv4[0]} between start_octet_1 and end_octet_1
       and {ipv4[1]} between start_octet_2 and end_octet_2
       and {ipv4[2]} between start_octet_3 and end_octet_3
       and {ipv4[3]} between start_octet_4 and end_octet_4
    ''')).fetchone()
    c = None
    if r is not None:
      (c,) = r
    return {'a': request.remote_addr, 'l': c}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
  return {'e':'nope'}

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
