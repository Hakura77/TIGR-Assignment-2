from TIGr import AbstractParser
import re
import json

"""
Uses Regular Expressions in Parser, Parsed from Configurable Lookup Table
Written by Kelsey Vavasour and Thomas Baines
"""


class TigrParser(AbstractParser):
    def __init__(self, drawer):
        super().__init__(drawer)
        self.regex_pattern = r'(^[a-zA-Z]\b)\s+?(-?\b\d+\.?\d?\b)?\s*?([#|//].*)?$'
        try:
            with open("command_lookup.json", 'r') as json_file:
                # load configurable language reference from file
                self.language_commands = json.load(json_file)  # convert to dict
        except (IOError, FileNotFoundError) as e:  # This error is thrown to be caught further up the stack
            raise FileNotFoundError(f"Error loading commands from file: {e}")

    def _prepare_source(self, raw_source):
        """defensively handles edge case where a single command was passed as a string"""
        if type(raw_source) == str:
            raw_source = [raw_source]
        return raw_source

    def _trim_and_validate_line(self, line, line_number):
        """accepts a line of code and a line index. validates that the line matches the provided pattern
          returns the valid line. in the instance where the line is empty, None is returned instead"""
        trimmed_line = line.strip()
        if not trimmed_line:
            return None
        match = re.findall(self.regex_pattern, trimmed_line)
        if match:
            return match
        else:
            # Raises SyntaxError to indicate that the line line_number didn't match the required pattern
            raise SyntaxError(f"line number {line_number} contains invalid syntax: \n\t{trimmed_line}")

    def _build_command(self, command_groups, line_number):
        """Takes the return from the _trim_and_validate() method and builds the appropriate command string to execute"""
        command_string = command_groups[0].upper()
        command_info = self.language_commands.get(command_string)
        if command_info:
            if command_groups[1]:
                command_data = int(round(float(command_groups[1])))
            else:
                command_data = None

            args = []
            if len(command_info) > 1:
                args.append(*command_info[1])
            if command_data:
                args.append(command_data)
            return command_info[0], args
        else:
            raise SyntaxError(f"Command {command_string} on line {line_number} not recognized")





    def parse(self, raw_source):
        """Method to accept raw source code, parse to language commands, and then execute language commands"""
        source = self._prepare_source(raw_source)
        for line_number in range(0, len(source) - 1):
            match = self._trim_and_validate_line(source[line_number], line_number)
            if match:
                groups = match[0]
                command = groups[0].upper()
                if groups[1]:
                    command_data = int(round(float(groups[1])))
                    """ Parser accepts decimals but silently rounds them in the background - all numbers passed are
                    stored as integers"""
                else:
                    command_data = None

                command_info = self.language_commands.get(command)
                if command_info:
                    args = []
                    if len(command_info) > 1:
                        args.append(*command_info[1])
                    if command_data:
                        args.append(command_data)

                    # explodes the created args array into the function that is being called
                    # if there is nothing in the array, nothing will be passed! Nice and fancy.
                    try:
                        self.drawer.__getattribute__(command_info[0])(*args)
                    except AttributeError as e:
                        raise SyntaxError(
                            f'Command {command} Not recognized by drawer - Command reference mismatch detected')
                    except Exception as e:  # intercept error thrown that wasn't caught and appending the line number
                        # that caused it
                        args = e.args
                        if args:
                            arg0 = args[0]
                        else:
                            arg0 = str()
                        arg0 += f' at source line {line_number}'
                        e.args = (arg0, *args[1:])
                        raise
                else:
                    raise SyntaxError(f"Command {command} on line {line_number} not recognized")
