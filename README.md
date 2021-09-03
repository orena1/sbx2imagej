# sbx2imagej: load sbx files directly to imagej/fiji

sbx2imagej, is a wrapper between [sbxreader](https://github.com/jcouto/sbxreader) and [pyimagej](https://github.com/imagej/pyimagej), sbxreader takes care of loading sbx files and pyimagej takes care of showing them in imagej.

## Usage

open console and write:

`sbx2imagej`

![](sbx2imagej_example.gif)


## Installation
sbx2imagej depends on pyimagej, and installing pyimagej is a bit hard as it require non-Python dependencies OpenJDK and Maven.
The easiest method it to install pyimagej with conda and then installing sbx2image with pip:
```
conda install -c conda-forge pyimagej openjdk=8
pip install sbx2imagej
```

[read more](https://github.com/imagej/pyimagej/blob/master/doc/Install.md) about pyimagej installation

---
Note! First time loading an sbx file to imagej will take a couple of minutes to set up pyimagej enviorment.







