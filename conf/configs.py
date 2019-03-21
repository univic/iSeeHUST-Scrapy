# configs.py

# -*- coding: utf-8 -*-
# Author : univic
# CreateDate : 2017-06-20

from conf.config_default import CONFIGS as CFG
CONFIGS = CFG

try:
    from conf.config_override import CONFIGS as CFG
    CONFIGS.update(CFG)
except ImportError:
    pass
