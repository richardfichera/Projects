# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script
"""

# import numpy as np
import random
# import openpyxl
import matplotlib.pyplot as plt
#
# Monte Carlo model for investments - Models account depletion under a set
# of assumptions for initial balance. inflation, return and withdrawal rates
#
# Get input variables
#
NQ_Assets = float(input("NQ investment assets (1000s):"))
NQ_Return = .045 # 40 year avg for bonds is .058
NQ_Return_Sigma = .03 # 40 year avg for bonds
Q_Assets = float(input("Q investment assets (1000s):"))
Q_Return = .07 # 40 year avg for stocks
Q_Return_Sigma = .12 # 40 year avg for stocks
years = int(input("How many years:")) # How many years per cycle
cycles = int(input("How many Monte Carlo iterations?:")) # how many model samples
Net_SS = 39.6
Net_Annuities = 10  # NQ annuities
RMD = 43 # Qual annuity plus additional $23K
Net_RMD = 36 # conservative st - 15% avg tax rate
Annual_Required = 144
# Annual changes - 1% SS COLA, 2.5% inflation
#
SS_Cola = .01
Inflation = .025
#
# Main logic loop - cycles is number of times to run N-year simulation,
# accumulating a new final asset value at the end of each cycle
#
Results = [] # empty list to hold results of each cycle for later
for cycle in range (1, cycles+1):
    # setup/restore initial conditions for next Monte Carlo iteration
    t_NQ_Assets = NQ_Assets
    t_Net_SS = Net_SS
    t_Q_Assets = Q_Assets
    t_Annual_Required = Annual_Required
    for year in range (1, years+1):
        #
        # Non qual assets
        #
        if (t_NQ_Assets > 0): # check to see if there aare any NQ assets left
            t_NQ_return = random.gauss(mu = NQ_Return, sigma = NQ_Return_Sigma) 
            NQ_Earnings = t_NQ_Assets * t_NQ_return *.95 #assumes  NQ$ are F tax free
            Total_Income = NQ_Earnings + t_Net_SS + Net_Annuities + Net_RMD
            Shortfall = t_Annual_Required - Total_Income
            t_NQ_Assets = t_NQ_Assets - Shortfall
        else:
            # NQ assets have run out, set to 0 to use as test later, error should be minor
            t_NQ_Assets = 0
        #
        # now qual assets - when NQ assets are depleted, required income is
        # taken from Q assets
        #
        t_Q_Return = random.gauss(mu = Q_Return, sigma = Q_Return_Sigma)       
        t_Q_Earnings = (t_Q_Assets * t_Q_Return)
        # now see if we are taaking required income out of Qual funds
        if (t_NQ_Assets == 0): # take additional Q expenses to compensate for zero NQ assets
            Total_Income = t_Q_Earnings + t_Net_SS + Net_Annuities + Net_RMD
            Shortfall = t_Annual_Required - Total_Income
            t_Q_Assets = t_Q_Assets - Shortfall - RMD
        else:  # still have NQ assets, Qual assets continue to accumulate ex RMD 
            t_Q_Assets = t_Q_Assets + t_Q_Earnings - RMD
        #
        # print ("Yr:%2d R:%5.3f NQ:%5.2f TI: %5.2f TNQ: %6.1f TQ: %6.1f" % (year, t_NQ_return, NQ_Earnings, Total_Income, t_NQ_Assets, t_Q_Assets))
        # increment annual requirements, COLA adjustments, etc
        #
        t_Annual_Required = t_Annual_Required * (1 + Inflation)
        t_Net_SS = t_Net_SS * (1 + SS_Cola)
  # grab total assets at end of each cycle and accumulate                
    Tot_Assets = t_Q_Assets + t_NQ_Assets #tot = Q + NQ
    Results.append(Tot_Assets)
#   if cycle % 100 == 0: # show completion of every 100 steps
#        print ("end cycle:", cycle)
print ("Completed ", cycles, "Monte Carlo Simulations")
#
# plot results
#        
num_bins = 100
n, bins, patches = plt.hist(Results, num_bins, facecolor='blue', alpha=0.5, label= "Frequency")
plt.grid(True)
plt.legend(loc='best')
plt.xlabel("Assets At End Of Simulation (1000s)")
plt.show()