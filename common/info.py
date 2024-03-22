import os


self_id = 6874839911
creator = 5273618487
administrators = {345060487, creator}
version = '1.0.3.100'
username = 'hisrchbot'
self_name = 'Kuma History Search'

if os.name == 'nt':
    debug_mode = True
    channel = 'local'
else:
    debug_mode = False
    channel = 'cloud'
