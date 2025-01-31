import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/sujeong/rokey2_D1_Driving1/src/install/driving1'
