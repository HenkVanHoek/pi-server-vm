# web-app.spec
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None
a = Analysis(
    ['webapp/app.py'],
    binaries=collect_dynamic_libs('python'),
    datas=[('webapp/templates', 'templates'), ('webapp/static', 'static')],
    hiddenimports=['waitress'],
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    name='pi-selfhosting-web',
    console=True,
    upx=True,
    # Point directly to the version info file.
    version='file_version_info.txt'
)
