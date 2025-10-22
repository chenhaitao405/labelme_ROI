# -*- coding: utf-8 -*-
# hook-numpy.py
from PyInstaller.utils.hooks import collect_submodules

# 确保收集所有numpy子模块
hiddenimports = collect_submodules('numpy')
