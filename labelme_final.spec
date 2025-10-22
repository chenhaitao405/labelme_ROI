# labelme_final.spec
# -*- mode: python -*-
# 最终版本：修复中文显示和隐藏控制台

import sys
import os
from pathlib import Path

block_cipher = None

# 获取labelme包的路径
import labelme
labelme_dir = Path(labelme.__file__).parent

# 收集labelme的所有数据文件（包括翻译文件）
labelme_datas = []

# 1. 配置文件
config_dir = labelme_dir / 'config'
if config_dir.exists():
    labelme_datas.append((str(config_dir), 'labelme/config'))

# 2. 图标文件
icons_dir = labelme_dir / 'icons'
if icons_dir.exists():
    labelme_datas.append((str(icons_dir), 'labelme/icons'))

# 3. 翻译文件（关键！解决中文问题）
translate_dir = labelme_dir / 'translate'
if translate_dir.exists():
    labelme_datas.append((str(translate_dir), 'labelme/translate'))
    print(f"Found translate directory: {translate_dir}")
    # 列出所有翻译文件
    for locale_file in translate_dir.glob('**/*'):
        if locale_file.is_file():
            print(f"  - {locale_file.name}")

# 处理onnxruntime
binaries_list = []
datas_list = []
hiddenimports_list = []

try:
    import onnxruntime
    onnxruntime_dir = Path(onnxruntime.__file__).parent
    
    print(f"Found onnxruntime at: {onnxruntime_dir}")
    
    # 复制整个onnxruntime目录
    datas_list.append((str(onnxruntime_dir), 'onnxruntime'))
    
    # 处理capi目录
    capi_dir = onnxruntime_dir / 'capi'
    if capi_dir.exists():
        for file_path in capi_dir.glob('*'):
            if file_path.is_file():
                if file_path.suffix in ['.dll', '.pyd', '.so', '.dylib']:
                    binaries_list.append((str(file_path), 'onnxruntime/capi'))
    
    # 检查主目录的DLL文件
    for dll_file in onnxruntime_dir.glob('*.dll'):
        binaries_list.append((str(dll_file), 'onnxruntime'))
    
    hiddenimports_list.extend([
        'onnxruntime',
        'onnxruntime.capi',
        'onnxruntime.capi._pybind_state',
        'onnxruntime.capi.onnxruntime_pybind11_state',
    ])
    
except ImportError:
    print("WARNING: onnxruntime not found")

# 处理osam包（如果存在）
try:
    import osam
    osam_dir = Path(osam.__file__).parent
    datas_list.append((str(osam_dir), 'osam'))
    hiddenimports_list.extend(['osam', 'osam.apis'])
except ImportError:
    print("osam not found (optional)")

# 处理PyQt5的翻译文件（Qt的中文支持）
try:
    import PyQt5
    pyqt5_dir = Path(PyQt5.__file__).parent
    
    # Qt的翻译文件
    translations_dir = pyqt5_dir / 'Qt5' / 'translations'
    if translations_dir.exists():
        # 只复制中文相关的翻译文件
        for qm_file in translations_dir.glob('qt*zh*.qm'):
            datas_list.append((str(qm_file), 'PyQt5/Qt5/translations'))
        for qm_file in translations_dir.glob('qtbase*.qm'):
            datas_list.append((str(qm_file), 'PyQt5/Qt5/translations'))
except ImportError:
    print("PyQt5 translations not found")

a = Analysis(
    ['labelme/__main__.py'],
    pathex=['.'],
    binaries=binaries_list,
    datas=labelme_datas + datas_list,  # 合并所有数据文件
    hiddenimports=[
        'PIL._tkinter',
        'PIL._imagingtk',
        'skimage.filters.rank.core_cy_3d',
        'scipy._lib.messagestream',
        'pkg_resources.py2_warn',
        # 添加locale相关的模块（处理语言）
        'locale',
        'gettext',
    ] + hiddenimports_list,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tensorboard', 'tensorflow', 'torch'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='labelme',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # 关闭UPX压缩
    console=True,  # ✅ 关闭控制台窗口！
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='labelme/icons/icon.ico' if sys.platform == 'win32' else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='labelme',
)
