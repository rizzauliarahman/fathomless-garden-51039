import logging

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

import mainTrain as mt
import warnings


warnings.filterwarnings("ignore")
mt.convert_upload()
