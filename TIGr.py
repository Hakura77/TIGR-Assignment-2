from abc import ABC, abstractmethod

from TIGrErrorManager import TIGrErrorManager

""" Tiny Interpreted GRaphic = TIGR
Keep the interfaces defined below in your work.
 """


class AbstractDrawer(ABC):
    """ Responsible for defining an interface for drawing """

    def execute_command(self, command_name, args):
        """Wrapper method to allow dynamic selection of command methods from a provided string
        added to reduce inappropriate intamacy between drawers and parsers."""
        command = self.__getattribute__(command_name)
        command(*args)

    @abstractmethod
    def select_pen(self, pen_num):
        pass

    @abstractmethod
    def pen_down(self):
        pass

    @abstractmethod
    def pen_up(self):
        pass

    @abstractmethod
    def go_along(self, along):
        pass

    @abstractmethod
    def go_down(self, down):
        pass

    @abstractmethod
    def draw_line(self, direction, distance):
        pass


class AbstractParser(ABC):
    def __init__(self, drawer):
        self.drawer = drawer
        self.error_manager = TIGrErrorManager()
        self.source = []
        self.command = ''
        self.data = 0

    @abstractmethod
    def parse(self, raw_source):
        pass


class AbstractSourceReader(ABC):
    """ responsible for providing source text for parsing and drawing
        Initiates the Draw use-case.
        Links to a parser and passes the source text onwards
    """

    def __init__(self, parser, optional_file_name=None):
        self.parser = parser
        self.file_name = optional_file_name
        self.source = []
        self.error_handler = TIGrErrorManager()

    @abstractmethod
    def go(self):
        pass
