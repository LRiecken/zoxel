from os.path import dirname
from os import listdir

path = dirname(__file__)
i = path.find(".zip")

if i == -1:  # OS X app or unpacked python files
    __all__ = [p[:-3] for p in listdir(path) if p.endswith(".py") and p != "__init__.py"]
    del p
else:  # Windows binary ziped .pyc files
    import zipfile
    __all__ = [f[8:-4] for f in zipfile.ZipFile(path[:i+4]).namelist() if f.find('plugins/') == 0 and
               f.endswith(".pyc") and not f.endswith("__init__.pyc")]
    del f
    del zipfile

del i
del path
del dirname
del listdir
