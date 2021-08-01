from typing import Any

def isfloat(value:Any):
  '''Check if an input can be converted to a float.'''
  try:
    float(value)
    return True
  except ValueError:
    return False