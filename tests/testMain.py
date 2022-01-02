import unittest
import wx

from Main import MyApp

class WindowTest(unittest.TestCase):
    def __init__(self, arg):
        # superclass setup
        super(WindowTest,self).__init__(arg)
        # WindowTest setup
        # make derived classes less annoying
        self.children = []
        self.children_ids = []
        self.children_names = []

    def setUp(self):
        self.app = MyApp()

    def tearDown(self):
        self.app.Destroy()

    def testApp(self):
        pass

