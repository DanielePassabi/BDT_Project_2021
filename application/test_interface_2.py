import wx

APP_EXIT = 1
FILE_SAVE = 2
FILE_OPEN = 3
SHOW_HELP = 4
SHOW_ABOUT = 5


class Example(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs) 
            
        self.InitUI()


    def InitUI(self):

        self.InitMenus()
        self.InitMainPanel()

        self.SetSize((1000, 500))
        self.SetTitle('WxPython Application Template')
        self.Center()
        self.Show(True)


    def InitMainPanel(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vbox)

        # add main widgets
        widgets = self.loadWidgets(panel)
        fgs = wx.FlexGridSizer(rows=len(widgets), cols=2, vgap=10, hgap=15)
        fgs.AddMany([(widget) for widget in widgets])
        vbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=20)

        # add button box
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(panel, label='OK', size=(70, 30))
        button_box.Add(ok_button, flag=wx.RIGHT)
        vbox.Add(button_box, flag=wx.ALIGN_CENTER|wx.BOTTOM, border=20)

        # flag=wx.EXPAND|wx.LEFT|wx.RIGHT



    def loadWidgets(self, panel):
        widgets = []

        checkbox_label = wx.StaticText(panel, label='Checkbox')
        checkbox = wx.CheckBox(panel)
        checkbox.SetValue(True)
        checkbox.Bind(wx.EVT_CHECKBOX, self.OnCheckboxChange)
        widgets.append(checkbox_label)
        widgets.append(checkbox)

        spinner_label = wx.StaticText(panel, label='Spinner')
        spinner = wx.SpinCtrl(panel, value='0')
        spinner.SetRange(-10, 10)
        widgets.append(spinner_label)
        widgets.append(spinner)

        text_control_label = wx.StaticText(panel, label='TextCtrl')
        textControl = wx.TextCtrl(panel)
        widgets.append(text_control_label)
        widgets.append(textControl)

        combobox_label = wx.StaticText(panel, label='Combobox')
        choices = ['one', 'two', 'three']
        combobox = wx.ComboBox(panel, choices=choices)
        combobox.SetValue(choices[0])
        widgets.append(combobox_label)
        widgets.append(combobox)

        slider_label = wx.StaticText(panel, label='Slider')
        slider = wx.Slider(panel, value=200, minValue=150, maxValue=500, size=(250, -1), style=wx.SL_HORIZONTAL)
        widgets.append(slider_label)
        widgets.append(slider)

        return widgets


    def OnCheckboxChange(self, event):
        sender = event.GetEventObject()
        isChecked = sender.GetValue()
        if isChecked:
            print('Checkbox selected')
        else:
            print('Checkbox unselected')


    def InitMenus(self):

        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        openMenuItem = wx.MenuItem(fileMenu, FILE_OPEN, '&Open\tCtrl+O')
        saveMenuItem = wx.MenuItem(fileMenu, FILE_SAVE, '&Save\tCtrl+S')
        quitMenuItem = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tCtrl+Q')
        fileMenu.AppendItem(openMenuItem)
        fileMenu.AppendItem(saveMenuItem)
        fileMenu.AppendItem(quitMenuItem)
        menubar.Append(fileMenu, '&File')
        self.Bind(wx.EVT_MENU, self.OnOpen, id=FILE_OPEN)
        self.Bind(wx.EVT_MENU, self.OnSave, id=FILE_SAVE)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=APP_EXIT)

        helpMenu = wx.Menu()
        helpMenuItem = wx.MenuItem(helpMenu, SHOW_HELP, '&Help\tCtrl+H')
        aboutMenuItem = wx.MenuItem(helpMenu, SHOW_ABOUT, '$About App\tCtrl+A')
        helpMenu.AppendItem(aboutMenuItem)
        helpMenu.AppendItem(helpMenuItem)
        menubar.Append(helpMenu, 'Help')
        self.Bind(wx.EVT_MENU, self.ShowHelp, id=SHOW_HELP)
        self.Bind(wx.EVT_MENU, self.ShowAbout, id=SHOW_ABOUT)

        self.SetMenuBar(menubar)


    def ShowHelp(self, e):
        print('Display help. Maybe open online help via a wx.html.HtmlWindow (or in a browser)')


    def ShowAbout(self, e):
        about_text = 'Put info about the application here, e.g., name, author(s), version, license, etc.'
        dlg = wx.MessageDialog(self, about_text, 'About App', wx.OK)  # wx.OK|wx.ICON_INFORMATION
        result = dlg.ShowModal()
        dlg.Destroy()


    def OnQuit(self, e):
        self.Close()


    def OnSave(self, e):
        saveFileDialog = wx.FileDialog(self, 'Save your file', '', '',
                                   'XYZ files (*.xyz)|*.xyz', wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return


    def OnOpen(self, e):
        openFileDialog = wx.FileDialog(self, 'Open a file', '', '',
                                       'XYZ files (*.xyz)|*.xyz', wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        print('Open file %s' % openFileDialog.GetPath())



def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()