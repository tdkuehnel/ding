import wx
from math import sin, cos, pi

class NodePanel(wx.Panel):
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

    def __init__(self, parent):
        super(NodePanel, self).__init__(parent)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def on_size(self, event):
        event.Skip()
        self.Refresh()

    def draw_node(self, x, y, dc, style=0):

        # Create a memory DC
        temp_dc = wx.MemoryDC()        
        temp_dc.SelectObject(wx.Bitmap(64, 64, depth=wx.BITMAP_SCREEN_DEPTH))
        temp_dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        temp_dc.Clear()
        temp_dc.SetPen(wx.Pen(wx.BLACK, 5))
        #dc.FloodFill(w / 2, h / 2, wx.RED, style=wx.FLOOD_BORDER)
        temp_dc.DrawCircle(32, 32, 28)
        brush = wx.Brush(wx.Colour(128,128,16))
        temp_dc.SetBrush(brush)
        temp_dc.FloodFill(32,32, wx.BLACK, style=wx.FLOOD_BORDER)

        dc.Blit(x - 32, y - 32, 64, 64, temp_dc, 0, 0)
        
    def on_paint(self, event):
        w, h = self.GetClientSize()
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 5))
        #dc.DrawLine(0, 0, w, h)

        self.draw_node(w/2, h/2, dc)

        centerx = w/2
        centery = h/2

        dc.DrawLine(centerx, centery + 32, centerx, centery + 32 + 32)
        
        posxstart = centerx + 32 * cos(pi/6)
        posystart = centery - 32 * sin(pi/6)

        posxend   = centerx + (32 + 36) * cos(pi/6)
        posyend   = centery - (32 + 36) * sin(pi/6)

        dc.DrawLine(posxstart, posystart, posxend, posyend)
        
        posxstart = centerx + 32 * cos(5*pi/6)
        posystart = centery - 32 * sin(5*pi/6)

        posxend   = centerx + (32 + 36) * cos(5*pi/6)
        posyend   = centery - (32 + 36) * sin(5*pi/6)

        dc.DrawLine(posxstart, posystart, posxend, posyend)
        
