#!/usr/bin/env python3

"""create_pyside6_app.py

A proof-of-concept script to create a minimal pyside6 .app bundle using nuitka.

"""


import argparse
import os
import shutil
import sysconfig





def vcmds(shellcmds, *args, **kwds):
    shellcmd = " && ".join(shellcmds)
    os.system(shellcmd)


class NuitkaPySideAppBuilder:
    def __init__(self, app: str, venv: str = 'buildenv', cleanup: bool = False, **options):
        self.app = app
        self.venv = venv
        self.cleanup = cleanup
        self.packages = options.get('packages')       # --include-package=PACKAGE
        self.modules = options.get('modules',)        # --include-module=MODULE
        self.plugindir = options.get('plugindir')     # --include-plugin-directory
        self.pluginfiles = options.get('pluginfiles') # --include-plugin-files
        self.packagedata = options.get('packagedata') # --include-package-data
        self.datafiles = options.get('datafiles')     # --include-data-files
        self.datadir = options.get('datadir')         # --include-data-dir
        self.exclude_datafile_pattern = options.get('exclude_datafile_pattern')
        self.py_ver = sysconfig.get_config_var("py_version_short")

    def cmd(self, shellcmd, *args, **kwds):
        os.system(shellcmd.format(*args, **kwds))

    def vcmds(self, shellcmds, *args, **kwds):
        shellcmd = " && ".join(shellcmds)
        os.system(shellcmd)

    def remove_tests(self, testdir):
        shutil.rmtree(testdir)
        print('removed testdir:', testdir)

    def build(self):
        self.vcmds(
            [
                f"virtualenv {self.venv}",
                f"source {self.venv}/bin/activate",
                "pip install PySide6 nuitka ordered-set zstandard",
                f"nuitka3 --standalone  --onefile "
                    "--enable-plugin=pyside6 "
                    f"--macos-create-app-bundle {self.app} "
                    f"--output-dir={self.venv}",
            ]
        )

    @classmethod
    def commandline(cls):
        """command line api
        """

        parser = argparse.ArgumentParser(
            prog = 'nuitka-pyside6-builder',
            usage='%(prog)s [options] <name>',
            description = 'Use nuitka to compile a python program with pyside6 into a macOS .app',
            epilog = 'Text at the bottom of help')

        arg = opt = parser.add_argument

        arg("name", help="Python file or module to compile")

        opt("-v", "--venv", help="Name of virtualenv", default='buildenv')

        opt("-c", "--cleanup", help="Cleanup after compilation", action="store_true")

        args = parser.parse_args()

        builder = cls(args.name, venv=args.venv, cleanup=args.cleanup)
        builder.build()



if __name__ == "__main__":
    NuitkaPySideAppBuilder.commandline()
