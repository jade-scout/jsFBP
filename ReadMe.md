## jsFBP (jade-scout File Backup Program)

### About

jsFBP is a simple program that uses configuration files
to automate rote file backups. It copies or moves files
using the `shutil` module. It does not zip or otherwise
compress the target files.

### Program Syntax

`python jsFBP.py [-h] <config_file>`

### Configuration File Syntax

```
Source:      <Directory path that contains the following files>
Destination:  <Directory path into which to move/copy the files>
Action:       <Move/Copy>
  - file01.txt
  - \subfolder1\              <Copies or moves all files and directories in subfolder1>
  - \subfolder2\file02.ini
```

### Technical Information

Platforms (tested): Windows 10, Ubuntu 19.04

Python Version: 3.6, 3.7

### Change Log
v1.0.1 - Fix some path validation errors while running on Linux. If a directory to be
         copied is already in the destination directory, the one in the destination
         directory is deleted and replaced, instead of erroring. Add tolerance for
         missing or unecessary path delimiters.

v1.0.0 - First release
