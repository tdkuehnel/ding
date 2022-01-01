import unittest
import wx

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
        self.app = wx.App()
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY)
        self.testControl = wx.Window(parent=self.frame, id=wx.ID_ANY)
        self.children_ids = (42, 43, 44)
        self.children_names = ('Child One', 'Child Two', 'Child Three')
        self.children = ( wx.Frame(self.testControl, id=id, name=name)
                            for id, name in zip(self.children_ids, self.children_names) )

    def tearDown(self):
        self.frame.Destroy()
        self.app.Destroy()

    def testApp(self):
        pass

    def testApp2(self):
        pass
