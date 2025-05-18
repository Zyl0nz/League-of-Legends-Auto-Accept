# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['lol.py'],
    pathex=[],
    binaries=[],
    datas=[('zzz_sleep.gif', '.'), ('accept_en.png', '.'), ('accept_kr.png', '.'), ('app_icon.ico', '.'), ('BeaufortforLOL-Heavy.ttf', '.'), ('BeaufortforLOL-Medium.ttf', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='lol',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app_icon.ico'],
)
