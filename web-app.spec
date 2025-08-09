# -*- mode: python ; coding: utf-8 -*-

# Paths are now relative to the project root where webapp/ is located.

block_cipher = None
version_info = {
    'vers': '1.4.0.0',
    'CompanyName': 'PiSelfhosting',
    'ProductName': 'PiSelfhosting',
    'InternalName': 'pi-selfhosting-web',
    'OriginalFilename': 'pi-selfhosting-web.exe',
    'FileDescription': 'Web interface for PiSelfhosting services.',
    'LegalCopyright': '© 2025 Henk van Hoek. All rights reserved.'
}

a = Analysis(
    ['webapp/app.py'],
    pathex=[],
    binaries=[],
       datas=[
        ('webapp/templates', 'templates'),
        ('webapp/static', 'static')
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
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=version_info['vers'],
    version_string=version_info
)
