# necessary to import other modules
import sys
sys.path.append('../')

from functions.machine_learning_model import *
from config.model_info import *

import json
import pickle
import wx

with open('config/input_possible_choices.json') as f:
  input_possible_choices = json.load(f)

class PredictWinnerInterface(wx.Frame):

    """
    Interface Settings
    """
    
    def __init__(self, *args, **kwargs):
        super(PredictWinnerInterface, self).__init__(*args, **kwargs) 

        self.custom_size_mandatory = (200, 20)
        self.custom_size_not_mandatory = (300, 20)

        self.InitUI()


    def InitUI(self):

        self.InitMainPanel()

        self.SetSize((510, 470))
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
        update_button = wx.Button(panel, label='Get Prediction', size=(100, 40))
        button_box.Add(update_button, flag=wx.RIGHT)
        update_button.Bind(wx.EVT_BUTTON, self.on_press)
        vbox.Add(button_box, flag=wx.ALIGN_CENTER|wx.BOTTOM, border=20)


    def loadWidgets(self, panel):

        widgets = []

        text_control_label_total_value = wx.StaticText(panel, label='Total Tender Value [€]')
        self.textControl_total_value = wx.TextCtrl(panel, size=self.custom_size_mandatory)
        widgets.append(text_control_label_total_value)
        widgets.append(self.textControl_total_value)

        text_control_label_lot = wx.StaticText(panel, label='Number of Lots in Tender')
        self.textControl_lot = wx.TextCtrl(panel, size=self.custom_size_mandatory)
        widgets.append(text_control_label_lot)
        widgets.append(self.textControl_lot)

        text_control_label_lot_value = wx.StaticText(panel, label='Lot Value')
        self.textControl_lot_value = wx.TextCtrl(panel, size=self.custom_size_mandatory)
        widgets.append(text_control_label_lot_value)
        widgets.append(self.textControl_lot_value)

        # create one empty row
        text_control_pad_1 = wx.StaticText(panel, label='')
        widgets.append(text_control_pad_1)
        text_control_pad_2 = wx.StaticText(panel, label='')
        widgets.append(text_control_pad_2)

        combobox_label_reg_branch = wx.StaticText(panel, label='Regional Branch')
        choices = input_possible_choices["sezione_regionale"]
        self.combobox_reg_branch = wx.ComboBox(panel, choices=choices, size=self.custom_size_not_mandatory)
        widgets.append(combobox_label_reg_branch)
        widgets.append(self.combobox_reg_branch)

        combobox_label_field = wx.StaticText(panel, label='Field')
        choices = input_possible_choices["settore"]
        self.combobox_field = wx.ComboBox(panel, choices=choices, size=self.custom_size_not_mandatory)
        widgets.append(combobox_label_field)
        widgets.append(self.combobox_field)

        combobox_label_partner_choice_crit = wx.StaticText(panel, label='Partner Choice Criterion')
        choices = input_possible_choices["tipo_scelta_contraente"]
        self.combobox_partner_choice_crit = wx.ComboBox(panel, choices=choices, size=self.custom_size_not_mandatory)
        widgets.append(combobox_label_partner_choice_crit)
        widgets.append(self.combobox_partner_choice_crit)

        combobox_label_tender_modality = wx.StaticText(panel, label='Tender Modality')
        choices = input_possible_choices["modalita_realizzazione"]
        self.combobox_tender_modality = wx.ComboBox(panel, choices=choices, size=self.custom_size_not_mandatory)
        widgets.append(combobox_label_tender_modality)
        widgets.append(self.combobox_tender_modality)

        combobox_label_contracting_auth = wx.StaticText(panel, label='Contracting Authority')
        choices = input_possible_choices["denominazione_amministrazione_appaltante"]
        self.combobox_contracting_auth = wx.ComboBox(panel, choices=choices, size=self.custom_size_not_mandatory)
        widgets.append(combobox_label_contracting_auth)
        widgets.append(self.combobox_contracting_auth)

        combobox_label_cpv = wx.StaticText(panel, label='CPV')
        choices = input_possible_choices["descrizione_cpv"]
        self.combobox_cpv = wx.ComboBox(panel, choices=choices, size=self.custom_size_not_mandatory)
        widgets.append(combobox_label_cpv)
        widgets.append(self.combobox_cpv)

        combobox_label_tend_denom = wx.StaticText(panel, label='Tenderer Denomination')
        choices = input_possible_choices["tipo_aggiudicatario"]
        self.combobox_tend_denom = wx.ComboBox(panel, choices=choices, size=self.custom_size_not_mandatory)
        widgets.append(combobox_label_tend_denom)
        widgets.append(self.combobox_tend_denom)

        return widgets


    """
    Logic
    """

    """
    Main function to compute the prediction
    """
    def getPrediction(self):
        
        # ottenere tutti i valori passati dall'utente
        # ammessi valori in bianco (ma non nei primi 3!)

        importo_complessivo_gara = self.textControl_total_value.GetValue()
        n_lotti_componenti = self.textControl_lot.GetValue()
        importo_lotto = self.textControl_lot_value.GetValue()

        sezione_regionale = self.combobox_reg_branch.GetStringSelection()
        settore = self.combobox_field.GetStringSelection()
        tipo_scelta_contraente = self.combobox_partner_choice_crit.GetStringSelection()
        modalita_realizzazione = self.combobox_tender_modality.GetStringSelection()
        denominazione_amministrazione_appaltante = self.combobox_contracting_auth.GetStringSelection()
        descrizione_cpv = self.combobox_cpv.GetStringSelection()
        tipo_aggiudicatario = self.combobox_tend_denom.GetStringSelection()

        # Check that all data is provided
        all_data = True

        for elem in [importo_complessivo_gara, n_lotti_componenti, importo_lotto]:
            if not elem:
                print("Error: you must provide all the information")
                dial = wx.MessageDialog(None, "Total Tender Value, Number of Lots in Tender and Lot Value are mandatory fields.\nPlease provide some values.", "Error", wx.ICON_EXCLAMATION)
                dial.ShowModal()
                all_data = False
                break

        if all_data:
            # Load model and encoder
            KNeighborsClassifier_model = pickle.load(open(model_info["model_path"], 'rb'))
            KNeighborsClassifier_encoder = pickle.load(open(model_info["encod_path"], 'rb'))
            
            # Prepare list with input data
            input_data = [importo_complessivo_gara, n_lotti_componenti, importo_lotto, settore, tipo_scelta_contraente, modalita_realizzazione, denominazione_amministrazione_appaltante, sezione_regionale, descrizione_cpv, tipo_aggiudicatario]

            # Return prediction
            pred = get_pred(KNeighborsClassifier_model, KNeighborsClassifier_encoder, input_data)
            
            dial = wx.MessageDialog(None, "Predicted Winner: " + pred, "Results", wx.ICON_INFORMATION)
            dial.ShowModal()


    # on button press
    def on_press(self, event):
        self.getPrediction()


def main():
    ex = wx.App()
    PredictWinnerInterface(None)
    ex.MainLoop()    

if __name__ == '__main__':
    main()