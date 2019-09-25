from TIGr import AbstractSourceReader
from TurtleDrawer import TurtleDrawer
from TigrParser import TigrParser
import sys
from TigrExcptionHandler import ExceptionHandler


class TigrReader(AbstractSourceReader):

    def __init__(self, parser, exception_handler, optional_file_name=None, optional_source=None):
        super().__init__(parser, optional_file_name)
        if optional_source:
            self.source = optional_source
        self.exception_handler = exception_handler

    def go(self):
        try:
            if not self.source:
                if not self.file_name:
                    self.file_name = input("Please enter a file name: ")
                try:
                    self.source = open(self.file_name).readlines()
                except (IOError, FileNotFoundError) as e:
                    self.exception_handler.display_and_exit(e)
            self.parser.parse(self.source)
        except Exception as e:  # nice error display to user
            self.exception_handler.display_and_exit(e)


if __name__ == "__main__":

    # check for file name arguments
    import argparse
    import time

    '''
    example usage within a terminal:
    > python TigrReader.py -f commands.txt
    
    > type commands.txt | python TigrReader.py
    
    > python TigrReader.py
    > Enter your commands. Ctrl + Z to exit
    > If no commands are entered, you will be prompted for a file name.
    
    '''
    arg_parser = argparse.ArgumentParser(description="Extract filename if present")
    arg_parser.add_argument("-f", "--file", help="Name of the file", default=None)
    args = arg_parser.parse_args()
    exception_handling = ExceptionHandler("TIGr went wrong and stopped")
    if args.file:
        # file name provided - read input from file
        TigrReader(TigrParser(TurtleDrawer(), exception_handling),
                   exception_handling, optional_file_name=args.file).go()
    else:
        # read from stdin
        # TODO examine if this section of the code can be incorporated within the class structure
        source = None
        if sys.stdin.isatty():
            # read from input at prompt
            print("Enter your commands. Ctrl + Z to exit or finish.")
            # only on windows, if this was portable we should add the linux interrupt command x3
            print("If no commands are entered, you will be prompted for a file name.")
            source = sys.stdin.readlines()
        else:
            # read from piped input
            source = sys.stdin.readlines()

        TigrReader(TigrParser(TurtleDrawer(), exception_handling), exception_handling, optional_source=source).go()

    time.sleep(10)
