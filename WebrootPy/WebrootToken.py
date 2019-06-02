import base64
import datetime
import pickle
import requests


class WebRootToken:
    WR_TOKEN_URL = "https://unityapi.webrootcloudav.com/auth/token"
    RAW_TOKEN = None
    SCOPE = None
    PRE_EXPIRE = 30  # pre-expire the token to start retrieving a new token.
    TOKEN_CACHE = None

    def __init__(self, credentials, scope="*", raw_token=None, token_cache=None):
        self.WR_CREDENTIALS = credentials
        self.RAW_TOKEN = raw_token
        self.SCOPE = scope
        self.TOKEN_CACHE = token_cache

        if token_cache and not raw_token:
            self.read_cache()
        elif token_cache and raw_token:
            self.write_cache()

    @staticmethod
    def base64encode(string):
        b64 = base64.b64encode(string.encode())
        return str(b64.decode('utf-8'))

    def get_new_token(self):
        header = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + self.base64encode(self.WR_CREDENTIALS["api"]["id"] + ":" +
                                                          self.WR_CREDENTIALS["api"]["secret"])
        }
        data = {
            'username': self.WR_CREDENTIALS["credential"]["user"],
            'password': self.WR_CREDENTIALS["credential"]["password"],
            'grant_type': 'password',
            'scope': self.SCOPE
        }
        token = requests.post(self.WR_TOKEN_URL, headers=header, data=data).json()
        token['time'] = datetime.datetime.now()
        self.RAW_TOKEN = token

        if self.TOKEN_CACHE:
            self.write_cache()

        return token

    def expired(self, pre_expire=True):
        try:
            if pre_expire:
                exp = self.RAW_TOKEN['time'] + datetime.timedelta(
                    seconds=self.RAW_TOKEN['expires_in'] - self.PRE_EXPIRE)
            else:
                exp = self.RAW_TOKEN['time'] + datetime.timedelta(seconds=self.RAW_TOKEN['expires_in'])

            if exp < datetime.datetime.now():
                return True
            else:
                return False
        except TypeError:
            return True

    def get_token(self):
        if self.expired():
            self.get_new_token()
        return self.RAW_TOKEN

    def read_cache(self):
        try:
            self.RAW_TOKEN = pickle.load(open(self.TOKEN_CACHE, 'rb'))
        except FileNotFoundError:
            self.get_token()

    def write_cache(self):
        pickle.dump(self.RAW_TOKEN, open(self.TOKEN_CACHE, 'wb'))
