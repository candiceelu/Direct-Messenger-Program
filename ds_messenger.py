from ds_protocol4 import direct_message, extract_json_dm, gen_token
import socket

PORT = 3021

class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None


class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.dsuserver = dsuserver
    self.username = username
    self.password = password
    self.token = None
    self.sock = None
		
  def send(self, message:str, recipient:str) -> bool:
    # must return true if message successfully sent, false if send failed.
    try:
      if self.token is None:
        self.token, self.sock = gen_token(self.username, self.password, self.dsuserver)
      dm = direct_message(token=self.token, entry=message, recipient=recipient)
      send = self.sock.makefile('w')
      recv = self.sock.makefile('r')
      send.write(dm + '\r\n')
      send.flush()
      srv_msg = recv.readline()[:-1]
      resp = extract_json_dm(srv_msg)
      if resp.type == 'error':
        print(f'ERROR: {resp.message}')
        return False
      elif resp.type == 'ok':
        return True
    except:
      return False
		
  def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new messages
    try:
      if self.token is None:
        self.token, self.sock = gen_token(self.username, self.password, self.dsuserver)
      dm = direct_message(token=self.token, dm='new')
      send = self.sock.makefile('w')
      recv = self.sock.makefile('r')
      send.write(dm + '\r\n')
      send.flush()
      srv_msg = recv.readline()[:-1]
      resp = extract_json_dm(srv_msg)
      if resp.type == 'error':
        print(f'ERROR: {resp.message}')
        return False
      elif resp.type == 'ok':
        return resp.message
    except:
      return False
 
  def retrieve_all(self) -> list:
    # must return a list of DirectMessage objects containing all messages
    try:
      if self.token is None:
        self.token, self.sock = gen_token(self.username, self.password, self.dsuserver)
      dm = direct_message(token=self.token, dm='all')
      send = self.sock.makefile('w')
      recv = self.sock.makefile('r')
      send.write(dm + '\r\n')
      send.flush()
      srv_msg = recv.readline()[:-1]
      resp = extract_json_dm(srv_msg)
      if resp.type == 'error':
        print(f'ERROR: {resp.message}')
        return False
      elif resp.type == 'ok':
        return resp.message
    except:
      return False
