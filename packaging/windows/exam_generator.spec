# -*- mode: python ; coding: utf-8 -*-
import sys
import os
import glob
from PyInstaller.utils.hooks import get_module_file_attribute

# Location of source and script files
repo_dir = os.path.realpath('../..')
module_dir = os.path.join(repo_dir, 'src/exam_generator')

# Templates and settings of exam_generator needs to be shipped as well
data_files = [(filename, './templates') for filename in glob.glob(os.path.join(module_dir, 'templates', '*.tex'))]
data_files += [(os.path.join(repo_dir, 'settings'), './settings')]

# It's open source, so we do not need to encrypt the python code
block_cipher = None

# Catch really every package loaded by exam_generator
sys.setrecursionlimit(sys.getrecursionlimit() * 5)

# Analyze what needs to be packaged
a = Analysis([os.path.join(repo_dir, 'run_exam_generator.py')],
             pathex=[repo_dir, module_dir],
             binaries=[],
             datas=data_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

# Put everything together
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Specification for building the exe
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='exam_generator',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True)

# Collection of all information needed for building the exe
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='exam_generator')
