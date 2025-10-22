# -*- coding: utf-8 -*-
# hook-onnxruntime.py
# PyInstaller hook for onnxruntime

from PyInstaller.utils.hooks import collect_all, collect_dynamic_libs
import os
import sys
from pathlib import Path

# 收集所有onnxruntime相关文件
datas, binaries, hiddenimports = collect_all('onnxruntime')

# Windows平台特殊处理
if sys.platform == 'win32':
    try:
        import onnxruntime
        onnx_dir = Path(onnxruntime.__file__).parent

        # 处理capi目录（onnxruntime 1.23.1的关键）
        capi_dir = onnx_dir / 'capi'
        if capi_dir.exists():
            # 添加所有capi目录的文件
            for file in capi_dir.glob('*'):
                if file.is_file():
                    binaries.append((str(file), 'onnxruntime/capi'))

        # 添加主目录的DLL
        for dll_file in onnx_dir.glob('*.dll'):
            binaries.append((str(dll_file), 'onnxruntime'))

    except Exception as e:
        print(f"Warning in hook-onnxruntime: {e}")

# 添加必要的隐藏导入
hiddenimports += [
    'onnxruntime.capi',
    'onnxruntime.capi._pybind_state',
    'onnxruntime.capi.onnxruntime_pybind11_state',
]
