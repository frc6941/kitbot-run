# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/Users/geyize/Desktop/kitbot_run/py/game.py'],
    pathex=[],
    binaries=[],
    datas=[('../Toby Fox - Dogsong.mp3', '.'), ('../collide.mp3', '.'), ('../Toby Fox - Song That Might Play When You Fight Sans.mp3', '.'), ('../Toby Fox - sans_cbr.mp3', '.'), ('../du.mp3', '.'), ('../car.png', '.'), ('../obstacle.png', '.'), ('../fail.png', '.'), ('../swerve.png', '.'), ('../kraken.png', '.'), ('../xiaomai.png', '.'), ('../car_def.png', '.'), ('../double.png', '.'), ('../blind.png', '.')],
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
    name='game',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
