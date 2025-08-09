# -*- mode: python ; coding: utf-8 -*-

# This block defines the version information for the executable
block_cipher = None
version_info = {
    'vers': '1.4.0.0',
    'CompanyName': 'PiSelfhosting',
    'ProductName': 'PiSelfhosting',
    'InternalName': 'clone-vm',
    'OriginalFilename': 'clone-vm.exe',
    'FileDescription': 'Clones a VirtualBox master template for automated testing.',
    'LegalCopyright': '© 2025 Henk van Hoek. All rights reserved.'
}

a = Analysis(
    ['run_clone.py'],
    pathex=[],
    binaries=[],
    datas=[],
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
    name='clone-vm',
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
    # Add the version information to the EXE
    version=version_info['vers'],
    version_string=version_info
)
