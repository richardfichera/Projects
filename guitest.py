'''
Input using PySimpleGUI.
'''

import PySimpleGUI as sg

def gui_dual_screen():
    
    layout = [
    [sg.Text('Monte Carlo Portfolio Model', size=(
           30, 1), justification='center', font=("Helvetica", 18), relief=sg.RELIEF_RIDGE)],
    [sg.Text('Annual income required?')],
    [sg.Slider(range=(100, 250), tooltip='How much money will you need each year?', key='Annual_Required', orientation='h', size=(16, 10), default_value=168)],
    [sg.Text('How many years?')],
    [sg.Slider(range=(1, 25), tooltip='How many years for this scenario?', key='years', orientation='h', size=(16, 10), default_value=25)],
    [sg.Text('How many cycles?')],
    [sg.Slider(range=(1, 10000), tooltip='How many iterations of the model?', key='cycles', orientation='h', size=(16, 10), default_value=10000)],
    [sg.Text('NQ Assets')],
    [sg.Slider(range=(1, 2000), tooltip='Initial NQ assets?', key='NQ_Assets', orientation='h', size=(16, 10), default_value=1500)],
    [sg.Text('Q Assets')],
    [sg.Slider(range=(1, 2000), tooltip='Initial Q assets?', key='Q_Assets', orientation='h', size=(16, 10), default_value=1500)],
    [sg.Text('Non-Qualified Investment Return Basis Points')],
    [sg.Slider(range=(100, 1000), tooltip='NQ return?', key='NQ_Return', orientation='h', size=(16, 10), default_value=580)],
    [sg.Text('Qualified Investment Return Basis Points')],
    [sg.Slider(range=(100, 1000), tooltip='Q Return?', key='Q_Return', orientation='h', size=(16, 10), default_value=700)],
    [sg.Text('Non-Qualified Return Std Deviation Basis Points')],
    [sg.Slider(range=(100, 1000), tooltip='NQ Sigma', key='NQ_Return_Sigma', orientation='h', size=(16, 10), default_value=600)],
    [sg.Text('Qualified Return Std Deviation Basis Points')],
    [sg.Slider(range=(100, 1500), tooltip='NQ Sigma', key='Q_Return_Sigma', orientation='h', size=(16, 10), default_value=1200)],
    [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()],
    ]
    
    window = sg.Window('MonteCarlo GUI', layout, no_titlebar=False,
        default_element_size=(100, 2), grab_anywhere=False)
    
    event, values_1 = window.read()
    # print (event)
    # print (values_1)
    window.close(); del window
    
    Annual_Required = values_1['Annual_Required']
    #print('Annual_Required: ', Annual_Required)
    years = values_1['years']
    #print('years: ', years)
    cycles = values_1['cycles']
    #print('cycles: ', cycles)
    NQ_Assets = values_1['NQ_Assets']
    #print('NQ_Assets: ',NQ_Assets)
    Q_Assets = values_1['Q_Assets']
    #print('Q_Assets: ', Q_Assets)
    NQ_Return = values_1['NQ_Return']
    #print('NQ_Return: ', NQ_Return)
    Q_Return = values_1['Q_Return']
    #print('Q_Return: ',Q_Return)
    NQ_Return_Sigma = values_1['NQ_Return_Sigma']
    #print('NQ_Return_Sigma: ', NQ_Return_Sigma)
    Q_Return_Sigma = values_1['Q_Return_Sigma']
    #print("Q_Return_Sigma: ", Q_Return_Sigma)
    
    layout = [
    [sg.Text('Net NQ Annuities')],
    [sg.Slider(range=(6, 12), tooltip='Net NQ Annuities', key='Net_Annuities', orientation='h', size=(16, 10), default_value=10)],
    [sg.Text('Net Social Security')],
    [sg.Slider(range=(20, 50), tooltip='Net Social Security', key='Net_SS', orientation='h', size=(16, 10), default_value=39)],
    [sg.Text('Social Security COLA (%)')],
    [sg.Slider(range=(0, 3), tooltip='Soc Sec COLA', key='SS_Cola',orientation='h', size=(16, 10), default_value=39)],
    [sg.Text('Inflation (%)')],
    [sg.Slider(range=(1, 4), tooltip='Inflation?', key='Inflation', orientation='h', size=(16, 10), default_value=2.5)],
    [sg.Text('RMD Tax Rate)')],
    [sg.Slider(range=(0, 60), tooltip='RMD Tax Rate', key='RMD_Tax_Rate', orientation='h', size=(16, 10), default_value=15)],
    
    [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()],
    ]
    
    window = sg.Window('MonteCarlo GUI_2', layout, no_titlebar=False,
        default_element_size=(100, 2), grab_anywhere=False)
    
    event, values_2 = window.read()
    # print (event)
    # print (values_2)
    
    Net_Annuities = values_2['Net_Annuities']
    Net_SS = values_2['Net_SS']
    SS_Cola = values_2['SS_Cola']
    Inflation = values_2['Inflation']
    RMD_Tax_Rate = values_2['RMD_Tax_Rate']
    
    return (Annual_Required, NQ_Assets, NQ_Return, NQ_Return_Sigma, Q_Assets,
                Q_Return, Q_Return_Sigma, years, cycles, Net_SS, Net_Annuities, SS_Cola, Inflation,
                RMD_Tax_Rate) # end of spreadsheet input

def main():
    (Annual_Required, NQ_Assets, NQ_Return, NQ_Return_Sigma, Q_Assets,
     Q_Return, Q_Return_Sigma, years, cycles, Net_SS, Net_Annuities, SS_Cola, Inflation,
     RMD_Tax_Rate) = gui_dual_screen()

    print('*** validate inputs ***')
    print('Annual_Required: ', Annual_Required)
    print('years: ', years)
    print('cycles: ', cycles)
    print('Q_Assets: ', Q_Assets)
    print('NQ_Return: ', NQ_Return)
    print('Q_Return: ', Q_Return)
    print('NQ_Return_Sigma: ', NQ_Return_Sigma)
    print("Q_Return_Sigma: ", Q_Return_Sigma)
    print('Net_Annuities: ', Net_Annuities)
    print('Net_SS: ', Net_SS)
    print('SS_Cola: ', SS_Cola)
    print('Inflation: ', Inflation)
    print('RMD_Tax_Rate: ', RMD_Tax_Rate)


if __name__ == '__main__':
    main()
