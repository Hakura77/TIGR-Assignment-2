from TIGr import AbstractParser
import re
import json

"""
Uses Regular Expressions in Parser, Parsed from Configurable Lookup Table
Written by Kelsey Vavasour and Thomas Baines
"""


def _handle_source(raw_source):
    if type(raw_source) == str:
        raw_source = [raw_source]
    return raw_source


class TigrParser(AbstractParser):
    def __init__(self, drawer, exception_handler):
        super().__init__(drawer)
        self.draw_methods = {
            'select_pen': self.drawer.select_pen,
            'pen_down': self.drawer.pen_down,
            'pen_up': self.drawer.pen_up,
            'go_along': self.drawer.go_along,
            'go_down': self.drawer.go_down,
            'draw_line': self.drawer.draw_line,
            }
        self.exception_handler = exception_handler
        self.regex_pattern = r'(^[a-zA-Z]\b)\s+?(-?\b\d+\.?\d?\b)?\s*?([#|//].*)?$'
        try:
            with open("command_lookup.json", 'r') as json_file:
                # load configurable language reference from file
                self.language_commands = json.load(json_file)  # convert to dict
        except (IOError, FileNotFoundError) as e:  # This error is thrown to be caught further up the stack
            self.exception_handler.display_and_exit(e)

    def _find_match(self, line_number):
        trimmed_line = self.source[line_number].strip()
        if not trimmed_line:
            return None
        match = re.findall(self.regex_pattern, trimmed_line)
        if match:
            return match
        else:
            # Raises SyntaxError to indicate that the line line_number didn't match the required pattern
            raise SyntaxError(f"line number {line_number} contains invalid syntax: \n\t{trimmed_line}")

    def _make_command(self, match_line, line_number):
        groups = match_line[0]
        command_groups = []
        self.command = groups[0].upper()
        if groups[1]:
            self.data = int(round(float(groups[1])))
        else:
            self.data = None
        command_info = self.language_commands.get(self.command)
        command_groups.append(command_info)
        if command_info:
            args = []
            if len(command_info) > 1:
                args.append(*command_info[1])
            if self.data:
                args.append(self.data)
            command_groups.append(args)
            return command_groups
        else:
            raise SyntaxError(f"Command {self.command} on line {line_number} not recognized")

    def _execute(self, command_group, line_number):
        try:
            self.draw_methods[command_group[0][0]](*command_group[1])
        except AttributeError:
            raise SyntaxError(
                f'Command {self.command} Not recognized by drawer - Command reference mismatch detected')
        except Exception as e:  # intercept error thrown that wasn't caught and appending the line number
            # that caused it
            args = e.args
            if args:
                arg0 = args[0]
            else:
                arg0 = str()
            arg0 += f' at source line {line_number}'
            e.args = (arg0, *args[1:])

    def parse(self, raw_source):
        self.source = _handle_source(raw_source)
        for line_number in range(0, len(self.source) - 1):
            match = self._find_match(line_number)
            if match:
                command_group = self._make_command(match, line_number)
                self._execute(command_group, line_number)
