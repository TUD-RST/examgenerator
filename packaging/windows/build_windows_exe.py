# -*- coding: utf-8 -*-
"""
Builds a Windows executable of exam_generator using PyInstaller
"""
import os
import shutil
from PyInstaller.__main__ import run as pyinstaller_run

# Specifications for PyInstaller
spec_file = "exam_generator.spec"

# Directories where to build into
script_dir = os.getcwd()
build_dir = os.path.join(script_dir, "build")
temp_dir = os.path.join(script_dir, "temp")

# Build the command string
cmd = ["--clean", f"--distpath={build_dir}", f"--workpath={temp_dir}", spec_file]

# Clean-up environment
for dir in [build_dir, temp_dir]:
    if os.path.exists(dir):
        shutil.rmtree(dir, ignore_errors=True)

# Call pyinstaller
print(f"Executing pyinstaller {' '.join(cmd)}")
pyinstaller_run(cmd)

# Remove temp data
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir, ignore_errors=True)
