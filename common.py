# -*- coding: utf-8 -*-
# =============================================================================
#          Desc: 
#        Author: chemf
#         Email: eoyohe@gmail.com
#      HomePage: eoyohe.cn
#       Version: 0.0.1
#    LastChange: 2020/3/2 4:40 PM
#       History: 
# =============================================================================
from dataclasses import dataclass

import yaml
import logging
import coloredlogs


@dataclass
class JobItem:
    title: str
    wage: str
    company: str
    url: str


with open('config.yaml') as f:
    config = yaml.load(f, yaml.FullLoader)

logger = logging.getLogger()
coloredlogs.install('INFO', logger=logger)
