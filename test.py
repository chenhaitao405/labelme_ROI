#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查和修复labelme打包后语言显示问题
"""

import os
import sys
import locale
from pathlib import Path


def check_locale_files():
    """检查labelme的翻译文件"""

    print("=" * 60)
    print("检查Labelme语言文件")
    print("=" * 60)

    # 1. 检查系统语言设置
    print("\n1. 系统语言设置:")
    try:
        system_locale = locale.getdefaultlocale()
        print(f"   系统默认语言: {system_locale[0]}")
        print(f"   系统编码: {system_locale[1]}")
    except Exception as e:
        print(f"   无法获取系统语言: {e}")

    # 2. 检查labelme的翻译文件
    print("\n2. Labelme翻译文件:")
    try:
        import labelme
        labelme_dir = Path(labelme.__file__).parent
        translate_dir = labelme_dir / 'translate'

        if translate_dir.exists():
            print(f"   ✓ 翻译目录存在: {translate_dir}")

            # 列出所有语言文件
            locale_dirs = [d for d in translate_dir.iterdir() if d.is_dir()]
            print(f"   找到 {len(locale_dirs)} 个语言包:")

            for locale_dir in locale_dirs:
                # 检查.qm文件（编译后的翻译文件）
                qm_files = list(locale_dir.glob('*.qm'))
                # 检查.po文件（源翻译文件）
                po_files = list(locale_dir.glob('*.po'))

                print(f"     - {locale_dir.name}:")
                if qm_files:
                    for qm in qm_files:
                        print(f"       ✓ {qm.name} ({qm.stat().st_size} bytes)")
                if po_files:
                    for po in po_files:
                        print(f"       ✓ {po.name} ({po.stat().st_size} bytes)")

                # 特别检查中文
                if 'zh' in locale_dir.name.lower():
                    print(f"       ⭐ 中文语言包已找到!")
        else:
            print(f"   ✗ 翻译目录不存在: {translate_dir}")
            print("   这可能是语言问题的原因")

    except ImportError:
        print("   ✗ labelme未安装")
    except Exception as e:
        print(f"   ✗ 检查失败: {e}")

    # 3. 检查PyQt5的翻译文件
    print("\n3. PyQt5翻译文件:")
    try:
        import PyQt5
        pyqt5_dir = Path(PyQt5.__file__).parent
        qt_translations = pyqt5_dir / 'Qt5' / 'translations'

        if qt_translations.exists():
            zh_files = list(qt_translations.glob('*zh*.qm'))
            if zh_files:
                print(f"   ✓ 找到 {len(zh_files)} 个中文翻译文件")
                for f in zh_files[:5]:  # 只显示前5个
                    print(f"     - {f.name}")
            else:
                print("   ⚠ 未找到中文翻译文件")
        else:
            print("   ✗ Qt翻译目录不存在")
    except ImportError:
        print("   ✗ PyQt5未安装")
    except Exception as e:
        print(f"   ✗ 检查失败: {e}")

    # 4. 检查打包后的文件（如果存在）
    print("\n4. 检查打包后的文件:")
    dist_dir = Path('dist/labelme')
    if dist_dir.exists():
        # 检查labelme/translate
        dist_translate = dist_dir / 'labelme' / 'translate'
        if dist_translate.exists():
            print(f"   ✓ 打包后翻译目录存在: {dist_translate}")
            # 列出语言包
            for item in dist_translate.iterdir():
                if item.is_dir():
                    files = list(item.glob('*'))
                    print(f"     - {item.name}: {len(files)} 个文件")
        else:
            print(f"   ✗ 打包后翻译目录不存在!")
            print("     这是导致英文显示的主要原因")
    else:
        print("   尚未打包或打包目录不在当前位置")


def create_runtime_hook():
    """创建运行时hook来强制设置语言"""

    hook_content = '''# -*- coding: utf-8 -*-
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
'''

    # 创建runtime_hooks目录
    hooks_dir = Path('runtime_hooks')
    hooks_dir.mkdir(exist_ok=True)

    hook_file = hooks_dir / 'runtime_hook_locale.py'
    hook_file.write_text(hook_content, encoding='utf-8')

    print(f"\n✓ 创建了运行时语言hook: {hook_file}")
    print("  在spec文件中添加: runtime_hooks=['runtime_hooks/runtime_hook_locale.py']")

    return str(hook_file)


def main():
    """主函数"""

    # 检查语言文件
    check_locale_files()

    # 创建运行时hook
    create_runtime_hook()

    print("\n" + "=" * 60)
    print("解决方案:")
    print("=" * 60)
    print("""
1. 使用 labelme_final.spec 打包（已包含所有翻译文件）:
   pyinstaller --clean labelme_final.spec

2. 如果还是英文，可以：

   a) 设置系统环境变量:
      set LANG=zh_CN.UTF-8
      set LANGUAGE=zh_CN

   b) 在程序启动时强制设置语言:
      创建一个启动脚本 start_labelme.bat:
      @echo off
      set LANG=zh_CN.UTF-8
      set LANGUAGE=zh_CN
      labelme.exe

   c) 修改Windows系统区域设置:
      控制面板 → 区域 → 管理 → 更改系统区域设置 → 中文(简体，中国)

3. 确保控制台窗口已关闭:
   spec文件中 console=False （已设置）

4. 重新打包后测试:
   cd dist/labelme
   labelme.exe
""")


if __name__ == '__main__':
    main()