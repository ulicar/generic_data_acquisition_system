import sys
import requests

from util.input.argument_parser import argument_parser
from util.communication import publisher
from config import Configuration

class DataRequester(object):
  def __init__(self, cfg):
    self.app_id = cfg.app_id
    self.mq_url = cfg.mq_url
    self.input = cfg.input
    self.output = cfg.output
    self.loq = cfg.log_file
    self.routing_key = cfg.routing_key
    self.publisher = None
    self.communication_token = cfg.token
    self.core_url = cfg.core_url
    self.data_scheme = cfg.data_scheme
    
  def validate_data(user_data, config):
    scheme = config['DATA_SCHEME']
    for data in user_data:
        if not validictory.validate(data, scheme):
            return False

    return True
    
  def publish_to_mq(messages):
    assert isinstance(messages, list), "messages must be a list"

    routing_key = get_message_type(messages[0], config)
   
    self.publisher(messages)  
    
  def run():
    try:
      while True:
        headers = {'token' : self.communication_token} 
        data = requests.get(url, headers=headers, verify=False).json()
        
        if self.validate_data(data, self.data_scheme):
          self.publish_to_mq(list(data))
          continue
          
        raise Exception('Message not valid.')
    except Exception as e:
      raise Exception(str(e))
      
        
  def main():
    publisher_settings = publisher.Settings(
      self.app_id,
      self.mq_url,
      self.output,
      self.routing_key
    )
    self.publisher = publisher.Publisher(publisher_settings)
    
    self.run()

if __name__ == '__main__':
  try:
    args = argument_parser('Data requester argument parser')
    cfg = Configuration().load_from_file(args.ini)
  
    data_requester = DataRequester(cfg)
    DataRequester.main()
  except Exception, e:
        print >>sys.stderr, str(e)
        sys.exit(-1)
  
  sys.exit(0)
