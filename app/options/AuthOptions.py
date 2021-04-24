class AuthOptions:
  def __init__(self, 
    jwt_secret,
    api_user
  ):
    self.jwt_secret = jwt_secret
    self.api_user = api_user
