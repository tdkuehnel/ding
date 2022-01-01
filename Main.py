import sys, os, time, traceback
import wx.lib.agw.aui as aui
import wx
import images

from wx.adv import SplashScreen as SplashScreen
from six.moves import cPickle

import wx.lib.mixins.inspection

from knoten.models import Knoten


# We won't import the images module yet, but we'll assign it to this
# global when we do.
images = None

_platformNames = ["wxMSW", "wxGTK", "wxMac"]
DEFAULT_PERSPECTIVE = "Default Perspective"

def GetDataDir():
    """
    Return the standard location on this platform for application data
    """
    sp = wx.StandardPaths.Get()
    return sp.GetUserDataDir()

def GetConfig():
    if not os.path.exists(GetDataDir()):
        os.makedirs(GetDataDir())

    config = wx.FileConfig(
        localFilename=os.path.join(GetDataDir(), "options"))
    return config


def MakeDocDirs():

    docDir = os.path.join(GetDataDir(), "docs")
    if not os.path.exists(docDir):
        os.makedirs(docDir)

    for plat in _platformNames:
        imageDir = os.path.join(docDir, "images", plat)
        if not os.path.exists(imageDir):
            os.makedirs(imageDir)

def GetDocFile():

    docFile = os.path.join(GetDataDir(), "docs", "TrunkDocs.pkl")

    return docFile


def GetDocImagesDir():

    MakeDocDirs()
    return os.path.join(GetDataDir(), "docs", "images")



def opj(path):
    """Convert paths to the platform-specific separator"""
    st = os.path.join(*tuple(path.split('/')))
    # HACK: on Linux, a leading / gets lost...
    if path.startswith('/'):
        st = '/' + st
    return st


class ListCtrl(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1,
                             style = wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES | wx.LC_SINGLE_SEL,)
        #self.InsertColumn(0, 'ID')
        #self.InsertColumn(1, 'Hash')

        info = wx.ListItem()
        info.Mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        info.Image = -1
        info.Align = 0
        info.Text = "ID"
        self.InsertColumn(0, info)
        
        #info.Align = wx.LIST_FORMAT_RIGHT
        #info.Text = "Hash"
        #self.InsertColumn(1, info)
        
        self.SetColumnWidth(0, 120)
        #self.SetColumnWidth(1, 120)

        self.il = wx.ImageList(16, 16)
        self.idx1 = self.il.Add(images.aquaflagged.GetBitmap())
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        for knoten in Knoten.objects.all():
            index = self.InsertItem(self.GetItemCount(), knoten.id.hex[:5] + '...', self.idx1)
            #self.SetItem(index, 1, '4534543r3') 
        
class MainPanel(wx.Panel):
    """
    Just a simple derived panel where we override Freeze and Thaw to work
    around an issue on wxGTK.
    """
    def Freeze(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(MainPanel, self).Freeze()

    def Thaw(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(MainPanel, self).Thaw()

class wxDasDing(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size = (970, 720),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)

        self.SetMinSize((640,480))

        self.pnl = pnl = MainPanel(self)

        self.mgr = aui.AuiManager()
        self.mgr.SetManagedWindow(pnl)

        self.loaded = False
        self.cwd = os.getcwd()
        self.curOverview = ""
        self.demoPage = None
        self.codePage = None
        self.shell = None
        self.firstTime = True
        self.finddlg = None

        #icon = images.WXPdemo.GetIcon()
        #self.SetIcon(icon)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_ICONIZE, self.OnIconfiy)
        self.Bind(wx.EVT_MAXIMIZE, self.OnMaximize)
        #self.Bind(wx.EVT_TIMER, self.OnDownloadTimer, self.downloadTimer)

        self.Centre(wx.BOTH)

        self.statusBar = self.CreateStatusBar(2)#, wx.ST_SIZEGRIP
        self.statusBar.SetStatusWidths([-2, -1])

        statusText = "Welcome to wxPython %s" % wx.VERSION_STRING
        self.ReadConfigurationFile()

        self.downloadGauge = wx.Gauge(self.statusBar, wx.ID_ANY, 50)
        self.downloadGauge.SetToolTip("Downloading Docs...")
        self.downloadGauge.Hide()

        self.sizeChanged = False
        self.Reposition()

        self.statusBar.Bind(wx.EVT_SIZE, self.OnStatusBarSize)
        self.statusBar.Bind(wx.EVT_IDLE, self.OnStatusBarIdle)
        self.dying = False

        # Create a Notebook
        self.nb = wx.Notebook(pnl, -1, style=wx.CLIP_CHILDREN)
        self.BuildMenuBar()

        leftPanel = wx.Panel(pnl, style=wx.TAB_TRAVERSAL|wx.CLIP_CHILDREN)

        self.tree = ListCtrl(leftPanel)
        
        self.filter = wx.SearchCtrl(leftPanel, style=wx.TE_PROCESS_ENTER)
        self.filter.ShowCancelButton(True)
        self.filter.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)

        # Set up a log window
        self.log = wx.TextCtrl(pnl, -1,
                              style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        if wx.Platform == "__WXMAC__":
            self.log.MacCheckSpelling(False)

        # But instead of the above we want to show how to use our own wx.Log class
        wx.Log.SetActiveTarget(MyLog(self.log))
        self.Bind(wx.EVT_ACTIVATE, self.OnActivate)
        wx.GetApp().Bind(wx.EVT_ACTIVATE_APP, self.OnAppActivate)

        # add the windows to the splitter and split it.
        leftBox = wx.BoxSizer(wx.VERTICAL)
        leftBox.Add(self.tree, 1, wx.EXPAND)
        leftBox.Add(wx.StaticText(leftPanel, label = "Filter Nodes:"), 0, wx.TOP|wx.LEFT, 5)
        leftBox.Add(self.filter, 0, wx.EXPAND|wx.ALL, 5)
        if 'wxMac' in wx.PlatformInfo:
            leftBox.Add((5,5))  # Make sure there is room for the focus ring
        leftPanel.SetSizer(leftBox)

        # Use the aui manager to set up everything
        self.mgr.AddPane(self.nb, aui.AuiPaneInfo().CenterPane().Name("Notebook"))
        self.mgr.AddPane(leftPanel,
                         aui.AuiPaneInfo().
                         Left().Layer(2).BestSize((240, -1)).
                         MinSize((240, -1)).
                         Floatable(self.allowAuiFloating).FloatingSize((240, 700)).
                         Caption("NCoT Nodes").
                         CloseButton(False).
                         Name("NCoTList"))
        self.mgr.AddPane(self.log,
                         aui.AuiPaneInfo().
                         Bottom().BestSize((-1, 150)).
                         MinSize((-1, 140)).
                         Floatable(self.allowAuiFloating).FloatingSize((500, 160)).
                         Caption("NCoT Log Messages").
                         CloseButton(False).
                         Name("LogWindow"))

        self.auiConfigurations[DEFAULT_PERSPECTIVE] = self.mgr.SavePerspective()
        self.mgr.Update()

        self.mgr.SetAGWFlags(self.mgr.GetAGWFlags() ^ aui.AUI_MGR_TRANSPARENT_DRAG)

        

    def BuildMenuBar(self):

        # Make a File menu
        self.mainmenu = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, '&Redirect Output',
                           'Redirect print statements to a window',
                           wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnToggleRedirect, item)

        exitItem = wx.MenuItem(menu, wx.ID_EXIT, 'E&xit\tCtrl-Q', 'Get the heck outta here!')
        exitItem.SetBitmap(images.catalog['exit'].GetBitmap())
        menu.Append(exitItem)
        self.Bind(wx.EVT_MENU, self.OnFileExit, exitItem)
        self.mainmenu.Append(menu, '&File')

        # Make an Option menu
        menu = wx.Menu()
        item = wx.MenuItem(menu, -1, 'Allow floating panes', 'Allows the demo panes to be floated using wxAUI', wx.ITEM_CHECK)
        menu.Append(item)
        item.Check(self.allowAuiFloating)
        self.Bind(wx.EVT_MENU, self.OnAllowAuiFloating, item)
        self.mainmenu.Append(menu, '&Options')
        self.options_menu = menu

        
        self.SetMenuBar(self.mainmenu)

        self.EnableAUIMenu()

    def EnableAUIMenu(self):

        menuItems = self.options_menu.GetMenuItems()
        for indx in range(4, len(menuItems)-1):
            item = menuItems[indx]
            item.Enable(self.allowAuiFloating)


    # Menu methods
    def OnFileExit(self, *event):
        self.Close()

    def OnToggleRedirect(self, event):
        app = wx.GetApp()
        if event.IsChecked():
            app.RedirectStdio()
            print("Print statements and other standard output will now be directed to this window.")
        else:
            app.RestoreStdio()
            print("Print statements and other standard output will now be sent to the usual location.")


    def OnStatusBarIdle(self, evt):
        if self.sizeChanged:
            self.Reposition()


    def OnSearchMenu(self, event):

        # Catch the search type (name or content)
        searchMenu = self.filter.GetMenu().GetMenuItems()
        fullSearch = searchMenu[1].IsChecked()

        if fullSearch:
            self.OnSearch()

    def OnSearch(self, event=None):

        value = self.filter.GetValue()
        if not value:
            #self.RecreateTree()
            return

        wx.BeginBusyCursor()

        wx.EndBusyCursor()



    def Reposition(self):
        # rect = self.statusBar.GetFieldRect(1)
        # self.downloadGauge.SetPosition((rect.x+2, rect.y+2))
        # self.downloadGauge.SetSize((rect.width-4, rect.height-4))
        self.sizeChanged = False
    def OnStatusBarSize(self, evt):
        self.Reposition()  # for normal size events

        # Set a flag so the idle time handler will also do the repositioning.
        # It is done this way to get around a buglet where GetFieldRect is not
        # accurate during the EVT_SIZE resulting from a frame maximize.
        self.sizeChanged = True

    def OnCloseWindow(self, event):
        self.mainmenu = None

        #if self.tbicon is not None:
        #    self.tbicon.Destroy()

        config = GetConfig()
        #config.Write('ExpansionState', str(self.tree.GetExpansionState()))
        #config.Write('AUIPerspectives', str(self.auiConfigurations))
        #config.Write('AllowDownloads', str(self.allowDocs))
        #config.Write('AllowAUIFloating', str(self.allowAuiFloating))

        config.Flush()

        MakeDocDirs()
        pickledFile = GetDocFile()
        with open(pickledFile, "wb") as fid:
            cPickle.dump(self.pickledData, fid, cPickle.HIGHEST_PROTOCOL)

        self.Destroy()


    #---------------------------------------------
    def OnIdle(self, event):
        """ Brauchen wa noch nicht """
        pass
    
    def OnIconfiy(self, evt):
        wx.LogMessage("OnIconfiy: %s" % evt.IsIconized())
        evt.Skip()

    #---------------------------------------------
    def OnMaximize(self, evt):
        wx.LogMessage("OnMaximize")
        evt.Skip()

    #---------------------------------------------
    def OnActivate(self, evt):
        wx.LogMessage("OnActivate: %s" % evt.GetActive())
        evt.Skip()

    #---------------------------------------------
    def OnAppActivate(self, evt):
        wx.LogMessage("OnAppActivate: %s" % evt.GetActive())
        evt.Skip()


    def OnAllowAuiFloating(self, event):

        self.allowAuiFloating = event.IsChecked()
#        for pane in self.mgr.GetAllPanes():
#            if pane.name != "Notebook":
#                pane.Floatable(self.allowAuiFloating)

        self.EnableAUIMenu()
        #self.mgr.Update()

    def ReadConfigurationFile(self):

        self.auiConfigurations = {}
        self.expansionState = [0, 1]

        config = GetConfig()
        val = config.Read('ExpansionState')
        if val:
            self.expansionState = eval(val)

        val = config.Read('AllowAUIFloating')
        if val:
            self.allowAuiFloating = eval(val)

        MakeDocDirs()
        pickledFile = GetDocFile()

        if not os.path.isfile(pickledFile):
            self.pickledData = {}
            return

        with open(pickledFile, "rb") as fid:
            try:
                self.pickledData = cPickle.load(fid)
            except:
                self.pickledData = {}

        
class MyLog(wx.Log):
    def __init__(self, textCtrl, logTime=0):
        wx.Log.__init__(self)
        self.tc = textCtrl
        self.logTime = logTime

    def DoLogText(self, message):
        if self.tc:
            self.tc.AppendText(message + '\n')


class MySplashScreen(SplashScreen):
    def __init__(self):
        bmp = wx.Image(opj("bitmaps/splash.png")).ConvertToBitmap()
        SplashScreen.__init__(self, bmp,
                                 wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
                                 5000, None, -1)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.fc = wx.CallLater(1000, self.ShowMain)


    def OnClose(self, evt):
        # Make sure the default handler runs too so this window gets
        # destroyed
        evt.Skip()
        self.Hide()

        # if the timer is still running then go ahead and show the
        # main frame now
        if self.fc.IsRunning():
            self.fc.Stop()
            self.ShowMain()


    def ShowMain(self):
        frame = wxDasDing(None, "Das ist ja ein Ding!")
        frame.Show()
        if self.fc.IsRunning():
            self.Raise()
        #wx.CallAfter(frame.ShowTip)


class MyApp(wx.App):
    def OnInit(self):
        wx.SystemOptions.SetOption("mac.window-plain-transition", 1)
        self.SetAppName("wxPyDemo")
        #self.InitInspection()  # for the InspectionMixin base class
        
        import images as i
        global images
        images = i

        splash = MySplashScreen()
        splash.Show()

        return True

def main():
    try:
        demoPath = os.path.dirname(__file__)
        os.chdir(demoPath)
    except:
        pass
    app = MyApp(False)
    app.MainLoop()

