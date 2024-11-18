class UserNotFoundException(Exception):
  '''Raise when user not found in your database'''
  pass

class PasswordNotMatch(Exception):
  '''Raise when user's password is not match with the data which is in your databas'''
  pass