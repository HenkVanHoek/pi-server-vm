# web-app.spec (Directory Build Test)
# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_dynamic_libs

block_cipher = None

a = Analysis(
    ['webapp/app.py'],
    binaries=collect_dynamic_libs('python'),
    # This ensures your web templates and static files are included.
    # Please verify these paths match your project structure.
    datas=[('webapp/templates', 'templates'), ('webapp/static', 'static')],
    hiddenimports=['waitress']
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    # This is a best practice for directory builds to avoid duplicating DLLs.
    exclude_binaries=True,
    name='pi-selfhosting-web',
    console=False,
    upx=True,
    version='file_version_info.txt'
)

# The COLLECT object is what tells PyInstaller to create a final output directory
# instead of a single file.
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='pi-selfhosting-web'
)
