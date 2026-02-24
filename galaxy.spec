# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

# Collect all source files
src_game_files = [
    ('src/game_files/audio.py', 'src/game_files'),
    ('src/game_files/controls.py', 'src/game_files'),
    ('src/game_files/game_manager.py', 'src/game_files'),
    ('src/game_files/land_tiles.py', 'src/game_files'),
    ('src/game_files/lines_gen.py', 'src/game_files'),
    ('src/game_files/ship.py', 'src/game_files'),
    ('src/game_files/transform.py', 'src/game_files'),
    ('src/game_files/__init__.py', 'src/game_files'),
]

src_screens = [
    ('src/screens/menu.py', 'src/screens'),
    ('src/screens/pause.py', 'src/screens'),
    ('src/screens/restart.py', 'src/screens'),
    ('src/screens/settings.py', 'src/screens'),
    ('src/screens/__init__.py', 'src/screens'),
]

# Data files: .kv files, assets, json config
datas = [
    ('galaxy.kv', '.'),
    ('src/screens/menu.kv', 'src/screens'),
    ('src/screens/restart.kv', 'src/screens'),
    ('src/screens/pause.kv', 'src/screens'),
    ('src/screens/settings.kv', 'src/screens'),
    ('assets/audio', 'assets/audio'),
    ('assets/fonts', 'assets/fonts'),
    ('assets/images', 'assets/images'),
    ('color.json', '.'),
    ('high_score.json', '.'),
    ('src/__init__.py', 'src'),
]

datas += src_game_files + src_screens

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'kivy',
        'kivy.core.window',
        'kivy.core.audio',
        'kivy.core.text',
        'kivy.core.image',
        'kivy.graphics',
        'src.game_files.transform',
        'src.game_files.audio',
        'src.game_files.controls',
        'src.game_files.land_tiles',
        'src.game_files.lines_gen',
        'src.game_files.game_manager',
        'src.game_files.ship',
        'src.screens.menu',
        'src.screens.pause',
        'src.screens.restart',
        'src.screens.settings',
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
    [],
    exclude_binaries=True,
    name='GalaxyGame',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GalaxyGame',
)
