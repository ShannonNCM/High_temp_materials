import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import fsolve
from openpyxl import load_workbook
#functions used to perform calculations




#################################################################################333
# PROBLEM SET 4
#################################################################################333

#problem 4 functions
#dictionary to rename the columns so that it is easier to use
names = {
    'Mole percent of Ni in FCC_A1': 'Ni_gamma',
    'Mole percent of Al in FCC_A1': 'Al_gamma',
    'Mole percent of Ta in FCC_A1': 'Ta_gamma',
    'Mole percent of Cr in FCC_A1': 'Cr_gamma',
    'Mole percent of Co in FCC_A1': 'Co_gamma',
    'Mole percent of Mo in FCC_A1': 'Mo_gamma',
    'Mole percent of Re in FCC_A1': 'Re_gamma',
    'Mole percent of W in FCC_A1': 'W_gamma',
    'Mole percent of Ni in GAMMA_PRIME': 'Ni_gammaprime',
    'Mole percent of Al in GAMMA_PRIME': 'Al_gammaprime',
    'Mole percent of Ta in GAMMA_PRIME': 'Ta_gammaprime',
    'Mole percent of Cr in GAMMA_PRIME': 'Cr_gammaprime',
    'Mole percent of Co in GAMMA_PRIME': 'Co_gammaprime',
    'Mole percent of Mo in GAMMA_PRIME': 'Mo_gammaprime',
    'Mole percent of Re in GAMMA_PRIME': 'Re_gammaprime',
    'Mole percent of W in GAMMA_PRIME': 'W_gammaprime'
}

#function to change the names of the columns to work with
def rename_alloy_columns(df, rename_map):
    return df.rename(columns=rename_map)

#funciones para calcular a_gamma y a_gammaprime
def a_gamma(row):
    return (3.523 + 0.179*row.get('Al_gamma',0) + 0.700*row.get('Ta_gamma',0) + 0.110*row.get('Cr_gamma',0) + 0.444*row.get('W_gamma',0) + 0.441*row.get('Re_gamma',0) + 0.478*row.get('Mo_gamma',0) + 0.096*row.get('Co_gamma',0))

def a_gamma_prime(row):
    return (3.558 + 0.500*row.get('Ta_gammaprime',0) - 0.004*row.get('Cr_gammaprime',0) + 0.194*row.get('W_gammaprime',0) + 0.262*row.get('Re_gammaprime',0) + 0.208*row.get('row.Mo_gammaprime',0))

#funcion para calcular lattice misfit
def delta(row):
    return(np.abs(2*((row.a_gammaprime-row.a_gamma)/(row.a_gammaprime+row.a_gamma))))

#function to perform all calculations
def calculations(dataframe):
    dataframe['a_gamma'] = dataframe.apply(a_gamma, axis=1)
    dataframe['a_gammaprime'] = dataframe.apply(a_gamma_prime, axis=1)
    dataframe['delta'] = dataframe.apply(delta, axis=1)
    return dataframe

#this is to save the result in latex format so that I can use it in my report
def save_latex(df):
    df = df.round(4).to_latex(index=False, float_format="%.4f")
    return df


#functions for problem 5

#dictionary with the fraction names
frac_names = {
    'Mole percent Ni':'x_Ni',
    'Mole percent Al':'x_Al',
    'Mole percent Ta':'x_Ta',
    'Mole percent Cr':'x_Cr',
    'Mole percent W':'x_W',
    'Mole percent Re':'x_Re',
    'Mole percent Co':'x_Co',
    'Mole fraction of FCC_A1':'x_gamma',
    'Mole fraction of GAMMA_PRIME':'x_gammaprime',
}

#dictionary with the mass of the elements in the alloys
molar_masses = {
    "Ni": 58.693,
    "Al": 26.982,
    "Ta": 180.947,
    "Cr": 51.996,
    "Co": 58.933,
    "Mo": 95.95,
    "W": 183.84,
    "Re": 186.21
}

#function to calculate the density
def density(row, mol_mass):
    molar_mass_sum = sum(row.get(f'x_{el}',0)*M
               for el, M in mol_mass.items())
    
    N_A = 6.022e23
    phase_fractions = (row.get('x_gamma',0)*((row.get('a_gamma',0))**3))+(row.get('x_gammaprime',0)*((row.get('a_gammaprime',0))**3))
    mass_unit_cell = (molar_mass_sum/N_A)*4
    volumen_cell = phase_fractions * 1e-24

    dens = mass_unit_cell/volumen_cell
    return dens