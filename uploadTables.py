#import libraries
import requests
import pandas
from pandas.io import gbq
import time
import numpy
import base64
import datetime
from urllib.parse import urlencode

# Developer keys
client_id = 'xxx'
secret_id = 'xxx

#Base API class
class TwitchAPI(object):
  access_token = None
  access_token_expires = datetime.datetime.now()
  access_token_did_expire = True
  client_id = None
  client_secret = None
  game_id = None
  idiom = None
  token_url = 'https://id.twitch.tv/oauth2/token'
  stream_url = 'https://api.twitch.tv/helix/streams'
  follow_url = 'https://api.twitch.tv/helix/users/follows'

  def __init__(self, client_id, client_secret, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.client_id = client_id
    self.client_secret = client_secret

  def get_client_credentials(self):
    #Return a base64 encoded string
    client_id = self.client_id
    client_secret = self.client_secret
    if client_secret == None or client_id == None:
      raise Exception('client_id and client_secret not set')
    client_creds = f"{client_id}:{secret_id}"
    client_creds_b64 = base64.b64encode(client_creds.encode())
    return client_creds_b64.decode()

  def get_token_headers(self):
    client_creds_b64 = self.get_client_credentials()
    return {
        "Client-ID": client_id,
        "Authorization": f"Bearer {client_creds_b64}",
      }
  
  def get_token_data(self):
    return{
        "grant_type": "client_credentials"
    }

  def get_auth_body(self):
    client_id = self.client_id
    secret_id = self.client_secret
    return  {
        "client_id": client_id,
        "client_secret": secret_id,
        "grant_type": "client_credentials"
        }
    
  def perform_auth(self):
    token_url = self.token_url
    auth_body = self.get_auth_body()
    #token_data = self.get_token_data()
    #token_headers = self.get_token_headers()
    r = requests.post(token_url, auth_body)
    if r.status_code not in range(200, 299):
      return False
    data = r.json()
    now = datetime.datetime.now()
    access_token = data['access_token']
    expires_in = data['expires_in']
    expires = now + datetime.timedelta(seconds=expires_in)
    self.access_token = access_token
    self.access_token_expires = expires
    self.access_token_did_expire = expires < now
    return True
  
  def get_headers(self):
    client_id = self.client_id
    access_token = self.access_token
    return {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}"
        }
  
  # top 20 by default
  def top_streams(self):
    stream_url = self.stream_url
    headers = self.get_headers()
    #Maximum number of objects to return.
    dict_param = {'first': 50}

    if self.game_id is not None:
      dict_param['game_id'] = self.game_id
    if self.idiom is not None:
      dict_param['language'] = self.idiom

    data = urlencode(dict_param)
    lookup_url = f"{stream_url}?{data}"
    return requests.get(lookup_url, headers = headers).json()

  def get_df(self, game_id=None, idiom=None):
    self.game_id = game_id
    self.idiom = idiom
    df = pandas.DataFrame(columns=['game_id', 'game_name','id','is_mature','language',
                                  'started_at', 'tag_ids','thumbnail_url', 'title',
                                  'user_id', 'user_name', 'viewer_count'])

    streams = self.top_streams()
    time.sleep(1)

    for field in streams['data']:
      game_id = field['game_id']
      game_name = field['game_name']
      id = field['id']
      is_mature = field['is_mature']
      language = field['language']
      started_at = field['started_at']
      tag_ids = field['tag_ids']
      thumbnail_url = field['thumbnail_url']
      title = field['title']
      user_id = field['user_id']
      user_name = field['user_name']
      viewer_count = field['viewer_count']

      df =df.append({'game_id':game_id, 'game_name':game_name,'id': id,'is_mature': is_mature,
                    'language':language, 'started_at': started_at, 'tag_ids': tag_ids,
                    'thumbnail_url':thumbnail_url, 'title': title, 'user_id': user_id, 'user_name':user_name, 'viewer_count':viewer_count}, ignore_index=True)
    return df

  def get_follows(self, user_id):
    follow_url = self.follow_url
    headers = self.get_headers()

    dict_param = {"to_id": user_id}
    data = urlencode(dict_param)
    lookup_url = f"{follow_url}?{data}&first=1"
    data = requests.get(lookup_url, headers = headers).json()
    return data['total']
