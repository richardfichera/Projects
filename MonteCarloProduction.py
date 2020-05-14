#!/usr/bin/env python3.8
#
# Monte Carlo model for investments - Models account depletion under a set
# of assumptions for initial balance. inflation, return and withdrawal rates
#
# Define RMD_calc function - takes RMD schedules and assets, returns RMD
#
import random
from tkinter import *
import openpyxl
import matplotlib.pyplot as plt


def RMD_calc(year, t_NQ_Assets):
    # schedule of RMD for RF, JR, starting at 72, using 2019 tables
    # divides Q assets by RMF factor, 1000000 is used for years that have no RMD
    rmf_RMD_sched = [1000000, 100000, 27.4, 26.5, 25.6, 24.7, 23.8, 22.9, 22, 21.2, 20.3, 19.5,
                     18.7, 17.9, 17.1, 16.3, 15.5, 14.8, 14.1, 13.4, 12.7, 12, 11.4, 10.8, 10.2, 9.6]
    jr_RMD_sched = [1000000, 100000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 27.4
                    , 26.5, 25.6, 24.7, 23.8, 22.9, 22, 21.2, 20.3, 19.5,
                    18.7, 17.9, 17.1, 16.3, 15.5, 14.8, 14.1]
    rmf_RMD = t_NQ_Assets * (1 / rmf_RMD_sched[year - 1]) * .75  # adjust for RF assets ~ 75% of total
    jr_RMD = t_NQ_Assets * (1 / jr_RMD_sched[year - 1]) * .25  # adjust for JR assets ~ 25% of total
    # print(rmf_RMD, jr_RMD)
    RMD = jr_RMD + rmf_RMD
    return RMD  # end of RMD_calc

def xls_get_input():
    # workbook object is created from file "montecarloparams.xlsx"
    wb_obj = openpyxl.load_workbook("C:/Users/richa/Downloads/montecarloparams.xlsx")
    # Get workbook active sheet object, default is first sheet
    sheet_obj = wb_obj.active
    # Cell objects also have row, column, attributes. Note: The first row or
    # column integer is 1, not 0. Cell object is created by using
    # sheet object's cell obj and sheet_obj methods.
    cell_obj = sheet_obj.cell(row=1, column=1)
    # Print title in cell A1 to verify
    print("Sheet title: ", cell_obj.value)
    #
    # Input for Monte Carlo investment model - models account depletion under a set
    # of assumptions.Get input variables from spreadsheet
    #
    NQ_Assets = sheet_obj.cell(row=7, column=2).value
    print("NQ assets (1000): ", NQ_Assets)
    #
    NQ_Return = sheet_obj.cell(row=3, column=2).value  # 40 year avg for bonds is .058
    print("NQ return (%): ", NQ_Return)
    #
    NQ_Return_Sigma = sheet_obj.cell(row=4, column=2).value
    print("NQ std dev (%): ", NQ_Return_Sigma)
    #
    Q_Assets = sheet_obj.cell(row=8, column=2).value
    print("Q assets: ", Q_Assets)
    #
    Q_Return = sheet_obj.cell(row=5, column=2).value  # 40 year avg for stocks is 7%
    print("Q return (%): ", Q_Return)
    #
    Q_Return_Sigma = sheet_obj.cell(row=6, column=2).value  # 40 year avg for stocks is 12%
    print("Q std dev (%): ", Q_Return_Sigma)
    #
    years = sheet_obj.cell(row=15, column=2).value  # How many years
    print("Years: ", years)
    #
    cycles = sheet_obj.cell(row=16, column=2).value  # how many model iterations
    print("Monte Carlo iterations: ", cycles)
    #
    Net_SS = sheet_obj.cell(row=11, column=2).value
    print("Net Social Security: ", Net_SS)
    #
    Net_Annuities = sheet_obj.cell(row=17, column=2).value  # NQ annuities
    print("Net NQ Annuities: ", Net_Annuities)
    #
    #RMD = sheet_obj.cell(row=12, column=2).value  # Qual annuity plus additional $43K
    #print("RMD: ", RMD) # Not passing RMD as parameter, fix spreadsheet later
    #
    Annual_Required = sheet_obj.cell(row=9, column=2).value
    print("Annual budget: ", Annual_Required)
    #
    SS_Cola = sheet_obj.cell(row=14, column=2).value
    print("Soc Sec COLA: ", SS_Cola)
    #
    Inflation = sheet_obj.cell(row=10, column=2).value
    print("Annual inflation: ", Inflation)
    #
    RMD_Tax_Rate = sheet_obj.cell(row=18, column=2).value
    print("RMD Tax Rate: ", RMD_Tax_Rate)
    return (Annual_Required, NQ_Assets, NQ_Return, NQ_Return_Sigma, Q_Assets,
            Q_Return, Q_Return_Sigma, years, cycles, Net_SS, Net_Annuities, SS_Cola, Inflation,
            RMD_Tax_Rate) # end of spreadsheet input

def std_get_input():
    # Get inout variables, some hard-coded, some from console
    Annual_Required = float(input("Desired annual after-tax income:"))
    NQ_Assets = float(input("NQ investment assets (1000s):"))
    NQ_Return = .058  # 40 year avg for bonds is .058,use this for whole NQ portfolio for conservative bias
    NQ_Return_Sigma = .06  # 40 year avg for bonds is 3% , double for mixed portfolio
    Q_Assets = float(input("Q investment assets (1000s):"))
    Q_Return = .07  # 40 year avg for stocks is 7%
    Q_Return_Sigma = .12
    # 40 year avg for stocks is 12%
    years = int(input("How many years:"))  # How many years per cycle
    if years > 25:
        print('Maximum 25 years, setting to 25 years')
        years = 25
    cycles = int(input("How many Monte Carlo iterations?:"))  # how many model samples
    Net_SS = 39
    Net_Annuities = 9.8  # NQ annuities
    SS_Cola = .01
    Inflation = .025
    RMD_Tax_Rate = .15
    # Add all vars here...
    return (Annual_Required, NQ_Assets, NQ_Return, NQ_Return_Sigma, Q_Assets,
            Q_Return, Q_Return_Sigma, years, cycles, Net_SS, Net_Annuities, SS_Cola, Inflation,
            RMD_Tax_Rate) # end of console + hard-coded input
#
# Main logic loop - cycles is number of times to run N-year simulation,
# accumulating a new final asset value at the end of each cycle
#
def tkinter_window_test():
    root = Tk()
    root.lift()

    title = Label(root, text='Monte Carlo Simulation Data Entry', font=("Helvetica", 16), bg='#909', fg='white', height=3, padx=100, pady=10)
    title.grid(row=0, column=1)

    Annual_Req = Scale(activebackground='green', relief=GROOVE, length=200, from_=90, to=250, label='Annual Required', orient=HORIZONTAL, bg='#CCC')
    Annual_Req.set(168)
    Annual_Req.grid(row=1)

    NQ_Ass = Scale(root, activebackground='green', relief=GROOVE, length=200, from_=900, to=2000, label='NQ Assets', orient=HORIZONTAL, bg='#CCC')
    NQ_Ass.set(1500)
    NQ_Ass.grid(row=2, column=0)

    Q_Ass = Scale(root, activebackground='green', relief=GROOVE, length=200, from_=900, to=2000, label='Q Assets', orient=HORIZONTAL, bg='#CCC')
    Q_Ass.set(1500)
    Q_Ass.grid(row=3, column=0)

    yrs = Scale(root, activebackground='green', relief=GROOVE, length=200, from_=20, to=30, label='Years', orient=HORIZONTAL, bg='#CCC')
    yrs.set(25)
    yrs.grid(row=1, column=1)

    cyc = Scale(root, activebackground='green', relief=GROOVE, length=200, from_=1000, to=10000, label='Model cycles', orient=HORIZONTAL, bg='#CCC')
    cyc.set(1000)
    cyc.grid(row=1, column=2)

    NQ_Ret = Scale(root, activebackground='green', relief=GROOVE, length=200, from_=10, to=100, label='NQ Return (1/10s)', orient=HORIZONTAL, bg='#CCC')
    NQ_Ret.set(55)
    NQ_Ret.grid(row=2, column=1)

    NQ_Ret_Sig = Scale(root, activebackground='green', relief=GROOVE, length=200, from_=10, to=100, label='NQ Return Sigma (1/10s)', orient=HORIZONTAL, bg='#CCC')
    NQ_Ret_Sig.set(60)
    NQ_Ret_Sig.grid(row=2, column=2)

    Q_Ret = Scale(root, activebackground='green', relief=GROOVE, length=200, from_=10, to=100, label='Q Return (1/10s)', orient=HORIZONTAL, bg='#CCC')
    Q_Ret.set(67)
    Q_Ret.grid(row=3, column=1)

    Q_Ret_Sig = Scale(root, activebackground='green', relief=GROOVE, length=200, from_=90, to=200, label='Q Return Sigma (1/10s)', orient=HORIZONTAL, bg='#CCC')
    Q_Ret_Sig.set(120)
    Q_Ret_Sig.grid(row=3, column=2)

    N_SS = Scale(root, activebackground='green', relief=GROOVE, length=200, from_=30, to=40, label='Net Social Security (1000s)', orient=HORIZONTAL, bg='#CCC')
    N_SS.set(39)
    N_SS.grid(row=4)

    N_Annuit = Scale(root, activebackground='green', relief=GROOVE, length=200, from_=8, to=12, label='Net NQ Annuities (1000s)', orient=HORIZONTAL, bg='#CCC')
    N_Annuit.set(10)
    N_Annuit.grid(row=4, column=1)

    RMD_Tax = Scale(root, activebackground='green', relief=GROOVE, length=200, from_=10, to=20, label='RMD Tax Rate (%)', orient=HORIZONTAL, bg='#CCC')
    RMD_Tax.set(15)
    RMD_Tax.grid(row=4, column=2)

    Infl = Scale(root, activebackground='green', relief=GROOVE, length=200, from_=10, to=40, label='Inflation (1/10s)', orient=HORIZONTAL, bg='#CCC')
    Infl.set(20)
    Infl.grid(row=5,column=1)

    S_Cola = Scale(root, activebackground='green', relief=GROOVE, length=200, from_=5, to=15, label='SS COLA (1/10s)', orient=HORIZONTAL, bg='#CCC')
    S_Cola.set(10)
    S_Cola.grid(row=5, column=0)

    Button(root, text='Submit', command=root.quit, bg='#CCC', activebackground='green').grid(row=7, column=1)
    mainloop()

    SS_Cola = float(S_Cola.get())/1000.0
    print(SS_Cola)
    RMD_Tax_Rate = float(RMD_Tax.get())/100.0
    print(RMD_Tax_Rate)
    Annual_Required = float(Annual_Req.get())
    print(Annual_Required) #print statements here for debug
    NQ_Assets = float(NQ_Ass.get())
    print(NQ_Assets)
    NQ_Return = float(NQ_Ret.get())/1000.0
    print(NQ_Return)
    NQ_Return_Sigma = float(NQ_Ret_Sig.get())/1000.0
    print(NQ_Return_Sigma)
    Q_Assets = float(Q_Ass.get())
    print(Q_Assets)
    Q_Return = float(Q_Ret.get())/1000.0
    print(Q_Return)
    Q_Return_Sigma = float(Q_Ret_Sig.get())/1000.0
    print(Q_Return_Sigma)
    years = int(yrs.get())
    print(years)
    cycles = int(cyc.get())
    print(cycles)
    Net_SS = float(N_SS.get())
    Net_Annuities = float (N_Annuit.get())
    print(Net_Annuities)
    Inflation = float(Infl.get())/1000.0
    print(Inflation)

    return (Annual_Required, NQ_Assets, NQ_Return, NQ_Return_Sigma, Q_Assets,
    Q_Return, Q_Return_Sigma, years, cycles, Net_SS, Net_Annuities, SS_Cola, Inflation,
    RMD_Tax_Rate)


def main():
    Results = []  # empty list to hold results of each cycle for later
    ZeroYear = []  # empty list to collect years that NQ assets are exhausted
    Annual_Req_Adjust = [1.0, 1.0, 1.0, 1.0, 1.0, .95, .95, .95, .95, .95, .90, .90, .90, .90, .90,
                         .90, .90, .90, .90, .90, 1.0, 1.0, 1.0, 1.0,
                         1.0]  # adjust required spend for age, then for extra help
    Param_Source = input("Use GUI(G), XLS(X) or Console(C) for input:")
    if Param_Source == "X":
        (Annual_Required, NQ_Assets, NQ_Return, NQ_Return_Sigma, Q_Assets,
         Q_Return, Q_Return_Sigma, years, cycles, Net_SS, Net_Annuities, SS_Cola, Inflation,
         RMD_Tax_Rate) = xls_get_input()
    elif Param_Source == 'C':
        (Annual_Required, NQ_Assets, NQ_Return, NQ_Return_Sigma, Q_Assets,
         Q_Return, Q_Return_Sigma, years, cycles, Net_SS, Net_Annuities, SS_Cola, Inflation,
         RMD_Tax_Rate) = std_get_input()
    elif Param_Source == 'G':
         (Annual_Required, NQ_Assets, NQ_Return, NQ_Return_Sigma, Q_Assets,
         Q_Return, Q_Return_Sigma, years, cycles, Net_SS, Net_Annuities, SS_Cola, Inflation,
         RMD_Tax_Rate) = tkinter_window_test()
    else: # input error, default to console
        print('Input source error, defaulting to console input')
        (Annual_Required, NQ_Assets, NQ_Return, NQ_Return_Sigma, Q_Assets,
         Q_Return, Q_Return_Sigma, years, cycles, Net_SS, Net_Annuities, SS_Cola, Inflation,
         RMD_Tax_Rate) = std_get_input()
    for cycle in range(1, cycles):
        # setup/restore initial conditions for next Monte Carlo iteration
        t_NQ_Assets = NQ_Assets
        t_Net_SS = Net_SS
        t_Q_Assets = Q_Assets
        t_Annual_Required = Annual_Required
        zero_flag = False
        for year in range(1, years):
            #
            # Non qual assets
            #
            if (t_NQ_Assets > 0):  # check to see if there are any NQ assets left
                t_NQ_return = random.gauss(mu=NQ_Return, sigma=NQ_Return_Sigma)
                NQ_Earnings = t_NQ_Assets * t_NQ_return * .95  # assumes  NQ$ are F tax free
                RMD = RMD_calc(year, t_NQ_Assets)
                Net_RMD = RMD * (1 - RMD_Tax_Rate)  # adjust RMD for tax
                # print Net_RMD)
                Total_Income = NQ_Earnings + t_Net_SS + Net_Annuities + Net_RMD
                Shortfall = t_Annual_Required - Total_Income
                t_NQ_Assets = t_NQ_Assets - Shortfall
                NQ_Cache = t_NQ_Assets  # preserve this value so it can be used when NQ drops < 0
            else:
                # NQ assets have run out, need to correct for the fact that <0 is detected the
                # year after assets cross the zero line, so
                # must subtract last NQ assets from existing Q assets to get true value
                if (zero_flag == False):  # first time that NQ < 0
                    t_Q_assets = t_Q_Assets + NQ_Cache  # add last year (now a negative) to Qual assets
                    t_NQ_Assets = 0
                    ZeroYear.append(year - 1)
                    zero_flag = True  # set this flag so subsequent passes just go to ELSE
                else:
                    t_NQ_Assets = 0  # not the first time through, this assignment really does nothing
            #
            # now qual assets - when NQ assets are depleted, required income is
            # taken from Q assets
            #
            t_Q_Return = random.gauss(mu=Q_Return, sigma=Q_Return_Sigma)
            t_Q_Earnings = (t_Q_Assets * t_Q_Return)
            RMD = RMD_calc(year, t_Q_Assets)
            Net_RMD = RMD * (1 - RMD_Tax_Rate)  # adjust for tax
            # now see if we are taaking required income out of Qual funds
            if (t_NQ_Assets == 0):  # take additional Q expenses to compensate for zero NQ assets
                Total_Income = t_Q_Earnings + t_Net_SS + Net_Annuities + Net_RMD
                Shortfall = t_Annual_Required - Total_Income
                t_Q_Assets = t_Q_Assets - Shortfall - RMD
            else:  # still have NQ assets, Qual assets continue to accumulate ex RMD
                t_Q_Assets = t_Q_Assets + t_Q_Earnings - RMD
            #
            # print ("Yr:%2d R:%5.3f NQ:%5.2f TI: %5.2f TNQ: %6.1f TQ: %6.1f" % (year, t_NQ_return, NQ_Earnings, Total_Income, t_NQ_Assets, t_Q_Assets))
            # increment annual requirements, COLA adjustments, etc
            #
            t_Annual_Required = t_Annual_Required * (1 + Inflation) * Annual_Req_Adjust[year - 1]
            t_Net_SS = t_Net_SS * (1 + SS_Cola)
        # grab total assets at end of each cycle and accumulate
        Tot_Assets = t_Q_Assets + t_NQ_Assets  # tot = Q + NQ
        Results.append(Tot_Assets)
        #
    print("Completed ", cycle+1, "Monte Carlo Simulations")
    #
    # plot results
    # original, ugly but works
    #num_bins = 100
    #plt.grid(True)
    #n, bins, patches = plt.hist(Results, num_bins, facecolor='blue', alpha=0.5, label="Frequency")
    #plt.xlabel("Assets At End Of Simulation (1000s)")
    #plt.legend(loc='best')
    #plt.show()
    #n, bins, patches = plt.hist(ZeroYear, num_bins, facecolor='blue', alpha=0.5, label="Frequency")
    #plt.xlabel("Year NQ Assets Exhausted")
    #plt.grid(True)
    #plt.legend()
    #plt.show()
    #
    # mods
    #
    num_bins = 100
    #plt.grid(True)
    # create multiple plots via plt.subplots(rows,columns)
    fig, axes = plt.subplots(2)
    # one plot on each subplot
    axes[0].hist(Results, num_bins, facecolor='blue', alpha=0.5, label="Frequency")
    axes[1].hist(ZeroYear, num_bins, facecolor='blue', alpha=0.5, label="Frequency")
    axes[0].legend(['Final Value'])
    axes[1].legend(['Year NQ Assets Exhausted'])
    plt.show()

if __name__ == '__main__':
    main()
