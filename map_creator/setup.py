from cx_Freeze import setup, Executable

build_exe_options = {"excludes": ["tkinter", "PyQt4.QtSql", "sqlite3", 
                                  "scipy", "numpy",
                                  "PyQt4.QtNetwork",
                                  "PyQt4.QtScript",
                                  "PyQt5"]}

setup(name = "map_creator",
      version = "0.1",
      description = "",
      options = { "build_exe" : build_exe_options },
      executables = [Executable("__main__.py")])