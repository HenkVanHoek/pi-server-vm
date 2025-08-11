# web-app.spec
# -*- mode: python ; coding: utf-8 -*-
import os

# PyInstaller provides the 'SPECPATH' variable in the execution context of the spec file.
# This is the reliable way to get the directory of the .spec file itself.
HERE = os.path.dirname(SPECPATH)

# Construct the full, absolute paths to the source directories.
WEBAPP_DIR = os.path.join(HERE, 'webapp')
TEMPLATE_DIR = os.path.join(WEBAPP_DIR, 'templates')
STATIC_DIR = os.path.join(WEBAPP_DIR, 'static')


block_cipher = None
version_info = {
    'vers': '1.4.2.0', # This will be updated by bump-my-version
    'CompanyName': 'PiSelfhosting',
    'ProductName': 'PiSelfhosting',
    'InternalName': 'pi-selfhosting-web',
    'OriginalFilename': 'pi-selfhosting-web.exe',
    'FileDescription': 'Web interface for PiSelfhosting services.',
    'LegalCopyright': '© 2025 Henk van Hoek. All rights reserved.'
}

a = Analysis(
    [os.path.join(WEBAPP_DIR, 'app.py')], # Use absolute path to the script
    pathex=[],
    binaries=[],
    datas=[
        (TEMPLATE_DIR, 'templates'), # Use absolute path to the data
        (STATIC_DIR, 'static')     # Use absolute path to the data
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
