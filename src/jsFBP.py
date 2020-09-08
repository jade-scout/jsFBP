#!/bin/python3
# -*- coding: utf-8 -*-


"""
jsFBP is a simple file backup program.

Name:     jsFBP (jade-scout File Backup Program)
Version:  1.0.0
Author:   jade-scout
"""

import argparse
import core
import os
import util


MAX_ITERATIONS = 64
HEADER_LENGTH = 3


def main():
    """Start program."""
    parser = argparse.ArgumentParser(description="jsFBP is a simple program"
                                     "for moving and copying files.")
    parser.add_argument("config_file", help="name of the configuration file")

    args = parser.parse_args()

    directories = core.DirectoryPaths(args.config_file)
    files = core.Files(args.config_file)
    path_line_num = 0

    i = 0
    syntax_check: bool = True

    # A fail-safe precaution. If the program somehow gets trapped in
    # potentially infinite loop, the i counter will force it to stop. This also
    # means you can only have 64 different file lists in the same configuration
    # file.

    util.print_info("Checking configuration file syntax...")

    while i < MAX_ITERATIONS:
        paths = directories.find(path_line_num)
        if paths == -1:
            if syntax_check is True:
                syntax_check = False
                if util.ERRORS_FOUND == 0:
                    i = 0
                    path_line_num = 0
                    files.last_file_line = 0
                    paths = directories.find(path_line_num)
                else:
                    break
            else:
                break
        file_list = files.file_list(path_line_num + HEADER_LENGTH,
                                    os.fsdecode(paths[0]))
        action = files.action(path_line_num + HEADER_LENGTH - 1)

        if not(syntax_check) and util.ERRORS_FOUND == 0:
            util.print_info("Processing file list #: {}".format(i + 1))
            core.backup_files(paths[0], paths[1], file_list, action)
        path_line_num = files.last_file_line + 1
        i += 1

    if util.ERRORS_FOUND == 0:
        util.print_info("Success!")
    else:
        util.print_info("{} Errors found. Program aborted".format(
            util.ERRORS_FOUND))


if __name__ == "__main__":
    main()
