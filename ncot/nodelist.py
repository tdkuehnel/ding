import wx

from knoten.models import Knoten
from ncot.ncotthread import NCoTThread
from Main import images

class NodeList(wx.ListCtrl):
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
            # self.SetItem(index, 1, '4534543r3')
            # Für jeden Knoten einen thread erzeugen.
            # Ob das hier die richtige Stelle dafür ist, wird sich noch zeigen.
            NCoTThread(knoten)
        
