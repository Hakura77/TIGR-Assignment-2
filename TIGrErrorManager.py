"""

Created by Thomas Baines
"""
import sys


class TIGrErrorManager:

    def __init__(self):
        self.exit_message = "TIGr encountered an error and had to exit"

    def log_error_and_exit(self, error_to_log):
        """Program standard behaviour for """
        print(self.exit_message, file=sys.stderr)
        print(error_to_log, file=sys.stderr)
        exit(1)

    def mutate_other_exceptions(self, e, line_number):
        """Intercepts errors that are thrown and not explicitly handled - indicating their
        line_number providence """
        args = e.args
        if args:
            arg0 = args[0]
        else:
            arg0 = str
        arg0 += f' at source line {line_number}'
        e.args = (arg0, *args[1:])
        return e

    def unable_to_open_input_error(self, error):
        """This error is thrown when the program is unable to open the provided source file"""
        return FileNotFoundError(f"Error loading source code from file {error}")

    def unable_to_load_language_error(self, error):
        return FileNotFoundError(f"Error loading commands from file: {error}")

    def drawer_language_missmatch_error(self, command_text):
        """This error is thrown when the language database contains a command not supported by drawer"""
        return SyntaxError(
            f'Command {command_text} Not recognized by drawer - Command reference mismatch detected')

    def unrecognized_command_error(self, command_string, line_number):
        """This error is thrown when the command passed in does not exist within the language database"""
        return SyntaxError(f"Command {command_string} on line {line_number} not recognized")

    def invalid_line_syntax_error(self, line_number, line_value):
        return SyntaxError(f"Command {line_value} on line {line_number} not recognized")


    def invalid_direction_error(self, direction):
        return ValueError(f"Direction given was {direction}, must be between 0 - 360")