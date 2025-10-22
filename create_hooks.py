#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建PyInstaller hooks文件
在运行pyinstaller之前先运行此脚本
"""

import os
from pathlib import Path


def create_hooks():
    """创建所有需要的hook文件"""

    # 创建hooks目录
    hooks_dir = Path('hooks')
    hooks_dir.mkdir(exist_ok=True)

    # 1. 创建onnxruntime hook
    hook_onnxruntime = hooks_dir / 'hook-onnxruntime.py'
    with open(hook_onnxruntime, 'w', encoding='utf-8') as f:
        f.write("""# -*- coding: utf-8 -*-
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
""")
    print(f"✓ 创建了: {hook_onnxruntime}")

    # 2. 创建osam hook
    hook_osam = hooks_dir / 'hook-osam.py'
    with open(hook_osam, 'w', encoding='utf-8') as f:
        f.write("""# -*- coding: utf-8 -*-
# hook-osam.py
from PyInstaller.utils.hooks import collect_all

try:
    datas, binaries, hiddenimports = collect_all('osam')
except Exception:
    datas = []
    binaries = []
    hiddenimports = []
""")
    print(f"✓ 创建了: {hook_osam}")

    # 3. 创建numpy hook补充（如果需要）
    hook_numpy = hooks_dir / 'hook-numpy.py'
    with open(hook_numpy, 'w', encoding='utf-8') as f:
        f.write("""# -*- coding: utf-8 -*-
# hook-numpy.py
from PyInstaller.utils.hooks import collect_submodules

# 确保收集所有numpy子模块
hiddenimports = collect_submodules('numpy')
""")
    print(f"✓ 创建了: {hook_numpy}")

    print("\n✓ 所有hook文件创建完成!")
    print("现在可以运行: pyinstaller --clean labelme_with_hooks.spec")


if __name__ == '__main__':
    create_hooks()