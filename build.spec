# labelme.spec
# -*- mode: python -*-
import sys
from pathlib import Path

block_cipher = None

# 获取labelme包的路径
import labelme
labelme_dir = Path(labelme.__file__).parent

a = Analysis(
    ['labelme/__main__.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        (str(labelme_dir / 'config' / 'default_config.yaml'), 'labelme/config'),
        (str(labelme_dir / 'icons' / '*'), 'labelme/icons'),
        (str(labelme_dir / 'translate' / '*'), 'labelme/translate'),
    ],
    hiddenimports=[
        'PIL._tkinter',
        'PIL._imagingtk',
        'skimage.filters.rank.core_cy_3d',
        'scipy._lib.messagestream',
        'pkg_resources.py2_warn',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=['matplotlib', 'tensorboard', 'tensorflow', 'torch'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
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
    upx=True,
    console=False,  # False表示不显示控制台窗口
    icon='labelme/icons/icon.ico' if sys.platform == 'win32' else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='labelme',
)