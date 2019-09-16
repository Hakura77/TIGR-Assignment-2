import unittest
from TurtleDrawer import TurtleDrawer
from TigrParser import TigrParser
from TigrReader import TigrReader

"""Written by Thomas Baines and Sean Ryan 22/08/2019"""


class DrawerTestCase(unittest.TestCase):

    def setUp(self):
        self.drawer = TurtleDrawer()

    def test_select_pen_exists(self):
        """Test to confirm that the drawer has a method called select_pen"""
        self.assertTrue("select_pen" in dir(TurtleDrawer))

    def test_pen_down_exists(self):
        """Test to confirm that the drawer has a method called pen_down"""
        self.assertTrue("pen_down" in dir(TurtleDrawer))

    def test_pen_up_exists(self):
        """Test to confirm that the drawer has a method called pen_up"""
        self.assertTrue("pen_up" in dir(TurtleDrawer))

    def test_go_along_exists(self):
        """Test to confirm that the drawer has a method called go_along"""
        self.assertTrue("go_along" in dir(TurtleDrawer))

    def test_go_down_exists(self):
        """Test to confirm that the drawer has a method called go_down"""
        self.assertTrue("go_down" in dir(TurtleDrawer))

    def test_draw_line_exists(self):
        """Test to confirm that the drawer has a method called draw_line"""
        self.assertTrue("draw_line" in dir(TurtleDrawer))

    def test_select_pen_executes(self):
        """Test to confirm that the drawer's method select_pen runs without error"""
        raised = False
        try:
            self.drawer.select_pen(1)
        except:
            raised = True
        self.assertFalse(raised, "Error Raised")

    def test_pen_down_executes(self):
        """Test to confirm that the drawer's method pen_down runs without error"""
        raised = False
        try:
            self.drawer.pen_down()
        except:
            raised = True
        self.assertFalse(raised, "Error Raised")

    def test_pen_up_executes(self):
        """Test to confirm that the drawer's method pen_up runs without error"""
        raised = False
        try:
            self.drawer.pen_up()
        except:
            raised = True
        self.assertFalse(raised, "Error Raised")

    def test_go_along_executes(self):
        """Test to confirm that the drawer's method go_along runs without error"""
        raised = False
        try:
            self.drawer.go_along(20)
        except:
            raised = True
        self.assertFalse(raised, "Error Raised")

    def test_go_down_executes(self):
        """Test to confirm that the drawer's method go_down runs without error"""
        raised = False
        try:
            self.drawer.go_down(20)
        except:
            raised = True
        self.assertFalse(raised, "Error Raised")

    def test_draw_line_executes(self):
        """Test to confirm that the drawer's method draw_line runs without error"""
        raised = False
        try:
            self.drawer.draw_line(20, 20)
        except:
            raised = True
        self.assertFalse(raised, "Error Raised")


class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = TigrParser(TurtleDrawer())
        self.source = ["p 3"]

    def test_parse_exists(self):
        """Test to confirm that the parser has a method called parse"""
        self.assertTrue("parse" in dir(TigrParser))

    def test_parse_executes(self):
        """Test to confirm that the parser's method parse runs without error"""
        raised = False
        try:
            self.parser.parse(self.source)
        except:
            raised = True
        self.assertFalse(raised, "Error Raised")

    def test_source_valid(self):
        """Test to confirm source stored in parser is valid"""
        self.parser.parse(self.source)
        self.assertEqual(self.parser.source, self.source)


class SourceReaderTestCase(unittest.TestCase):

    def setUp(self):
        self.source_reader = TigrReader(TigrParser(TurtleDrawer()))

    def test_go_exists(self):
        """Test to confirm that the Source Reader has a method called go"""
        self.assertTrue("go" in dir(TigrReader))

    def test_go_executes(self):
        """Test to confirm that the source reader's method go runs without error"""
        raised = False
        self.source_reader.source = ["p 3"]
        try:
            self.source_reader.go()
        except:
            raised = True
        self.assertFalse(raised, "Error Raised")


def drawer_suite():
    suite = unittest.TestSuite()
    """Following code is "Clever" as it automatically identifies all tests that conform
    to the correct naming scheme within the test case and adds them to the suite"""
    test_names = [i for i in dir(DrawerTestCase) if i.startswith("test_")]
    for test_name in test_names:
        suite.addTest(DrawerTestCase(test_name))
    return suite


def parser_suite():
    suite = unittest.TestSuite()
    test_names = [i for i in dir(ParserTestCase) if i.startswith("test_")]

    for test_name in test_names:
        suite.addTest(ParserTestCase(test_name))
    return suite


def source_reader_suite():
    suite = unittest.TestSuite()
    test_names = [i for i in dir(SourceReaderTestCase) if i.startswith("test_")]

    for test_name in test_names:
        suite.addTest(SourceReaderTestCase(test_name))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(drawer_suite())
    runner.run(parser_suite())
    runner.run(source_reader_suite())
