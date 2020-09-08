"""Contains the core routines for jsFBP."""

import util
import os
import platform
import re
import shutil


# These are the values that the Action parameter can be in the configuration
# file
ACTION_CMDS = ["Move", "Copy"]


class DirectoryPaths:
    """Class for configuration file directory handling."""

    def __init__(self, config_file_name):
        self.config_file_name = config_file_name
        self.paths = list()
        self.path_line_num: int

    def path_line(self):
        """Return the line number of the current path pair."""
        return self.path_line_num

    def is_path(self, path):
        """
        Verify that path is a legal file system path.

        Returns None if the path is invalid.
        """
        if platform.system() == "Windows":
            result = re.findall("^[^\\//]+:+(\\\\{1,1}[^\\/*\"<>|:?]*)+\\\\*$",
                                path)
        else:
            result = re.findall("^(//{1,1}[^\\/*\"<>|:?]*)+//*$", path)

        # If the path is invalid, re.findall will return an empty list
        try:
            result[0]
        except IndexError:
            return False
        return True

    def find(self, line_num):
        """
        Retrieve the source and destination paths in the configuration file.

        Returns a list where the 0th element is the source directory and the
        1st element is the destination directory. line_num indicates from which
        line to start searching.

        The 0th element is "EOFError" if an EOFError occurred.
        """
        # Initialize self.paths as an empty list
        self.paths = list()
        try:
            config_file = open(self.config_file_name, 'r')

        except FileNotFoundError:
            util.handle_error(util.CONFIG_FILE_NOT_FOUND, True, -1)

        else:
            contents = config_file.readlines()
            config_file.close()

            # Skip over any empty lines until you find the first directory
            # pair or until an EOF is reached
            lines_skipped = 0
            while True:
                # If the last line of the file is reached, terminate the
                # program
                if line_num + lines_skipped >= len(contents):
                    return -1

                line = contents[line_num + lines_skipped]

                if line != os.linesep:
                    break

                lines_skipped += 1

            # Store the line number of the path pair
            self.path_line_num = line_num + lines_skipped

            source_dir: str = contents[self.path_line_num]
            dest_dir: str = contents[self.path_line_num + 1]

            # Strip the leading descriptors and any trailing characters from
            # the directory path
            i = source_dir.find(':', 0) + 1
            source_dir = source_dir[i:]
            source_dir = source_dir.strip(" \t\n")

            if self.is_path(source_dir) is False or os.path.exists(
                    source_dir) is False:
                util.handle_error(util.SRC_DIR_MISSING, True,
                                  self.path_line_num + 1)

            source_dir = os.fsencode(source_dir)

            i = dest_dir.find(':', 0) + 1
            dest_dir = dest_dir[i:]
            dest_dir = dest_dir.strip(" \t\n")

            if self.is_path(dest_dir) is False or os.path.exists(
                    dest_dir) is False:
                util.handle_error(util.DEST_DIR_MISSING, True,
                                  self.path_line_num + 2)

            dest_dir = os.fsencode(dest_dir)

            self.paths.insert(0, source_dir)
            self.paths.insert(1, dest_dir)

        return self.paths


class Files:
    """Retrieves the list of files for the current path pair."""

    def __init__(self, config_file_name):
        self.config_file_name = config_file_name
        self.last_file_line: int = 0
        self.files = list()

    def action(self, action_line_offset):
        """Get the action that will be applied to the file list."""
        try:
            config_file = open(self.config_file_name, 'r')

        except FileNotFoundError:
            util.handle_error(util.CONFIG_FILE_NOT_FOUND, True, -1)

        else:
            contents = config_file.readlines()
            config_file.close()
            action_line = contents[action_line_offset]

            i = action_line.find(':', 0) + 1

            # If the colon is not found, i == -1 + 1 == 0
            if i == 0:
                util.handle_error(util.ACTION_CMD_MISSING, True,
                                  action_line_offset + 1)

            action_line = action_line[i:]
            action = action_line.strip(" \t\n")

            if not(action in ACTION_CMDS):
                util.handle_error(util.ACTION_CMD_INVALID, True,
                                  action_line_offset + 1)

            return action

    def file_list(self, file_list_offset, src_dir):
        """
        Retrieve all of the files for a specific target/destination path pair.

        Stores all of the filenames in a list.
        """
        # Initialize self.files as an empty list
        self.files = list()
        try:
            config_file = open(self.config_file_name, 'r')

        except FileNotFoundError:
            util.handle_error(util.CONFIG_FILE_NOT_FOUND, True, -1)

        else:
            contents = config_file.readlines()
            config_file.close()

            # Strip the whitespace from the file names and store them to the
            # files list
            i = 0
            while i < len(contents) - file_list_offset:
                line = contents[file_list_offset + i]

                # Break if an empty line is encountered. This means that the
                # all of the files in the current list have been retrieved.
                if line == '\n':
                    break

                if line.startswith("  - ") is False:
                    util.handle_error(util.FILE_ENTRY_INVALID, True,
                                      file_list_offset + i + 1)
                    self.files.insert(i, "Invalid")
                else:
                    line = line.strip(" -\n")
                    if os.path.exists(src_dir + line) is False:
                        util.handle_error(util.FILE_ENTRY_INVALID, True,
                                          file_list_offset + i + 1)
                        self.files.insert(i, "Invalid")
                    else:
                        self.files.insert(i, line)
                i += 1

            self.last_file_line = file_list_offset + i

        return self.files


def backup_files(source_dir, dest_dir, file_list, action):
    """
    Backup the the files in file_list from source_dir to dest_dir.

    action determines if the files are moved or copied.
    """
    i = 0
    while i < len(file_list):

        if action == "Copy":
            if (platform.system() == "Windows" and file_list[i].endswith(
                    '\\')) or file_list[i].endswith('//'):
                shutil.copytree(os.fsdecode(source_dir) + file_list[i],
                                os.fsdecode(dest_dir) + file_list[i])
            else:
                shutil.copy(os.fsdecode(source_dir) + file_list[i],
                            os.fsdecode(dest_dir))

        if action == "Move":
            shutil.move(os.fsdecode(source_dir) + file_list[i],
                        os.fsdecode(dest_dir) + file_list[i])
        i += 1

    return
