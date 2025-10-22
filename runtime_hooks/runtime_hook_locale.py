# -*- coding: utf-8 -*-
# runtime_hook_locale.py
# 运行时设置语言为中文

import os
import sys
import locale

# 强制设置语言环境为中文
os.environ['LANG'] = 'zh_CN.UTF-8'
os.environ['LC_ALL'] = 'zh_CN.UTF-8'
os.environ['LANGUAGE'] = 'zh_CN:zh'

# Windows特殊处理
if sys.platform == 'win32':
    try:
        # Windows使用不同的语言代码
        locale.setlocale(locale.LC_ALL, 'Chinese_China.936')
    except:
        try:
            locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
        except:
            pass

print(f"Language environment set to: {os.environ.get('LANG', 'not set')}")
