# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    # 将 src/assets 目录下的文件打包到程序运行时的 assets 文件夹中
    datas=[('src/assets/style.qss', 'assets')],
    # 包含了所有使用到的第三方库，特别是那些可能无法被自动检测到的隐式导入
    hiddenimports=[
        'pypdf',
        'fitz',
        'pdf2docx',
        'pdfplumber',
        'pandas',
        'openpyxl',
        'pptx',
        'docx2pdf',
        'PIL',
        'comtypes',
        'comtypes.client'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PDF工具集',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    # 控制台窗口隐藏
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # 如果有图标，可以在这里指定 icon='src/assets/icon.ico'
)
