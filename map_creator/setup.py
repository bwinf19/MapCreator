from cx_Freeze import setup, Executable

build_exe_options = {'include_files': ['sp.png'],
                     "excludes": ["tkinter", "PyQt4.QtSql", "sqlite3",
                                  "scipy", "numpy", "email",
                                  "PyQt4.QtNetwork",
                                  "PyQt4.QtScript",
                                  "PyQt5"]}

setup(name="map_creator",
      version="0.1",
      description="",
      options={"build_exe": build_exe_options},
      executables=[Executable("__main__.py", targetName="map_creator.exe")])
