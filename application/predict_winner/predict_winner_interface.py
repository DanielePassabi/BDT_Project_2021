# necessary to import other modules
import sys
sys.path.append('../')

from functions.machine_learning_model import *
from config import *

import pickle
import wx

class PredictWinnerInterface(wx.Frame):

    """
    Interface Settings
    """
    
    def __init__(self, *args, **kwargs):
        super(PredictWinnerInterface, self).__init__(*args, **kwargs) 
            
        # Initialize variables (and placeholders)
        self.combobox_data_type = None
        self.csv_picker = None
        self.textControl_host = None
        self.textControl_port = None
        self.textControl_database = None
        self.textControl_user = None

        self.textControl_password = None
        self.log = None

        self.percent = None

        self.InitUI()


    def InitUI(self):

        self.InitMainPanel()

        self.SetSize((370, 715))
        self.SetTitle('Predict Winner of Future Tender')
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
        update_button = wx.Button(panel, label='Update DB', size=(100, 40))
        button_box.Add(update_button, flag=wx.RIGHT)
        update_button.Bind(wx.EVT_BUTTON, self.on_press)
        vbox.Add(button_box, flag=wx.ALIGN_CENTER|wx.BOTTOM, border=20)

        self.log = wx.TextCtrl(panel, -1, size=(300, 300), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        vbox.Add(self.log, 0, wx.ALL | wx.EXPAND, 5)
        redir = RedirectText(self.log)
        sys.stdout = redir


    def loadWidgets(self, panel):

        widgets = []

        combobox_label_data_type = wx.StaticText(panel, label='Select data to update')
        choices = ['CIG', 'AGGIUDICATARI']
        self.combobox_data_type = wx.ComboBox(panel, choices=choices)
        widgets.append(combobox_label_data_type)
        widgets.append(self.combobox_data_type)

        csv_picker_text = wx.StaticText(panel, label='Select .csv')
        self.csv_picker = wx.FilePickerCtrl(panel)

        widgets.append(csv_picker_text)
        widgets.append(self.csv_picker)


        text_control_mysql = wx.StaticText(panel, label='\nMySQL credentials')
        text_control_mysql_padding = wx.StaticText(panel, label='')
        widgets.append(text_control_mysql)
        widgets.append(text_control_mysql_padding)

        text_control_label_host = wx.StaticText(panel, label='Host')
        self.textControl_host = wx.TextCtrl(panel)
        widgets.append(text_control_label_host)
        widgets.append(self.textControl_host)

        text_control_label_port = wx.StaticText(panel, label='Port')
        self.textControl_port = wx.TextCtrl(panel)
        widgets.append(text_control_label_port)
        widgets.append(self.textControl_port)

        text_control_label_database = wx.StaticText(panel, label='Database')
        self.textControl_database = wx.TextCtrl(panel)
        widgets.append(text_control_label_database)
        widgets.append(self.textControl_database)

        text_control_label_user = wx.StaticText(panel, label='User')
        self.textControl_user = wx.TextCtrl(panel)
        widgets.append(text_control_label_user)
        widgets.append(self.textControl_user)

        text_control_label_password = wx.StaticText(panel, label='Password')
        self.textControl_password = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        widgets.append(text_control_label_password)
        widgets.append(self.textControl_password)

        return widgets


    """
    Logic
    """

    """
    Main function to update the Database
     1. obtains the path of the csv to add to the db
     2. obtains the credentials for MySQL DB (uses placeholders if not provided)
     3. checks that all the data was provided by the user
     4. updates the db with the provided data 
    """
    def updateDB(self):
        data_to_update = self.combobox_data_type.GetStringSelection()

        csv_path = self.csv_picker.GetPath()

        if self.textControl_host.GetValue():
            host = self.textControl_host.GetValue()

        if self.textControl_port.GetValue():
            port = self.textControl_port.GetValue()

        if self.textControl_database.GetValue():
            database = self.textControl_database.GetValue()

        if self.textControl_user.GetValue():
            user = self.textControl_user.GetValue()

        password = self.textControl_password.GetValue()

        # Check that all data is provided
        all_data = True

        for elem in [data_to_update, csv_path, host, port, database, user, password]:
            if not elem:
                print("Error: you must provide all the information")
                dial = wx.MessageDialog(None, "You must provide all the information", "Error", wx.ICON_EXCLAMATION)
                dial.ShowModal()
                all_data = False
                break
            
        if all_data:
            print("\n========================================\n")
            # Show provided data
            print("INFORMATION PROVIDED")
            print("\n > Data to update:", data_to_update)
            print("\n > Path of chosen .csv:", csv_path)
            print("\n > MySQL Credentials:")
            print("   - host:", host)
            print("   - port:", port)
            print("   - database:", database)
            print("   - user:", user)

            print("\nStarting the update")

            try:
                if data_to_update == "CIG":
                    updateCIGTable(host, port, database, user, password, csv_path, interface=True)

                elif data_to_update == "AGGIUDICATARI":
                    updateAggiudicatariTable(host, port, database, user, password, csv_path, interface=True)

                dial = wx.MessageDialog(None, "Database correctly updated", "Information", wx.ICON_INFORMATION)
                dial.ShowModal()

                    
            except Exception as e:
                print("Error: Update Failed. Error details below.\n" + str(e))
                dial = wx.MessageDialog(None, "Update Failed. Error details below.\n" + str(e), "Error", wx.ICON_ERROR)
                dial.ShowModal()

    # on button press
    def on_press(self, event):
        self.updateDB()



class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)


def main():
    ex = wx.App()
    PredictWinnerInterface(None)
    ex.MainLoop()    

if __name__ == '__main__':
    main()




