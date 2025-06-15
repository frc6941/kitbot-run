# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['py\\game.py'],
    pathex=[],
    binaries=[],
    datas=[('mp3\\collide.mp3', 'mp3'), ('mp3\\Toby Fox - Dogsong.mp3', 'mp3'), ('mp3\\Toby Fox - Song That Might Play When You Fight Sans.mp3', 'mp3'), ('mp3\\Toby Fox - sans_cbr.mp3', 'mp3'), ('mp3\\du.mp3', 'mp3'), ('png\\car.png', 'png'), ('png\\obstacle.png', 'png'), ('png\\fail.png', 'png'), ('png\\swerve.png', 'png'), ('png\\kraken.png', 'png'), ('png\\xiaomai.png', 'png'), ('png\\car_def.png', 'png'), ('png\\double.png', 'png'), ('png\\blind.png', 'png')],
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
    name='KitbotRun',
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
)
