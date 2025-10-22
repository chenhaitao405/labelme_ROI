# -*- coding: utf-8 -*-
# hook-osam.py
from PyInstaller.utils.hooks import collect_all

try:
    datas, binaries, hiddenimports = collect_all('osam')
except Exception:
    datas = []
    binaries = []
    hiddenimports = []
