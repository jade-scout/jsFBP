"""Supporting functions for the main program."""

error_msg = {
             1: "Configuration file not found",
             2: "Source directory missing or invalid",
             3: "Destination directory missing or invalid",
             4: "Action command missing",
             5: "Action command invalid",
             6: "Invalid file or subdirectory entry. All entries must begin"
             " with \'  - \'",
             7: "Failed to access source directory. Please make sure that this"
             " directory exists and is accessbile",
             8: "Failed to access destination directory. Please make sure that"
             " this directory exists and is accessible"
             }

CONFIG_FILE_NOT_FOUND = 1
SRC_DIR_MISSING = 2
DEST_DIR_MISSING = 3
ACTION_CMD_MISSING = 4
ACTION_CMD_INVALID = 5
FILE_ENTRY_INVALID = 6
SRC_DIR_ACCESS_FAIL = 7
DEST_DIR_ACCESS_FAIL = 8

ERRORS_FOUND = 0


def print_error(message):
    """Print an error message to the console."""
    print("[Error] {}".format(message))
    return


def handle_error(code, print_e, line):
    """
    Retrieve the correct error message and save the error code to a list.

    print_e is a boolean; True when the message is to be printed to the
    console; False, otherwise.

    Returns the current number of errors found.
    """
    if print_e:
        if line == -1:
            print_error(error_msg[code])
        elif line >= 0:
            print_error("[Line {}] {}".format(line, error_msg[code]))
    global ERRORS_FOUND
    ERRORS_FOUND += 1
    return ERRORS_FOUND


def print_info(message):
    """Print a status message about the program."""
    print("[Info] {}".format(message))
    return
