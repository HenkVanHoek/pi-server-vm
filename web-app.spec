# web-app.spec (Simplified and final version)
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
version_info = {
    'vers': '1.4.3.0', # This will be updated by bump-my-version
    'CompanyName': 'PiSelfhosting',
    'ProductName': 'PiSelfhosting',
    'InternalName': 'pi-selfhosting-web',
    'OriginalFilename': 'pi-selfhosting-web.exe',
    'FileDescription': 'Web interface for PiSelfhosting services.',
    'LegalCopyright': '© 2025 Henk van Hoek. All rights reserved.'
}

a = Analysis(
    ['webapp/app.py'], # Simple relative path
    pathex=[],
    binaries=[],
    datas=[
        ('webapp/templates', 'templates'), # Simple relative path
        ('webapp/static', 'static')     # Simple relative path
    ],
    hiddenimports=['waitress'],
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
    [],
    a.binaries,
    a.datas,
    name='pi-selfhosting-web',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=True,
    version=version_info['vers'],
    version_string=version_info
)
