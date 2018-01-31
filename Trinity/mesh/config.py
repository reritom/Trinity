'''
  This class contains configuration settings for the mesh network.
'''

class Config():
  def __init__(self):
    
    # Relay configurations
    relay = dict()
    relay['process_time'] = 10 # Time to process, in microseconds
    relay['process_variance'] = 0.05 # value between 0-1 representing how much the process time can vary
    
    # Cortex configurations
    cortex = dict()
    
    pass
