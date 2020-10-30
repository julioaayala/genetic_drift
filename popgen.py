'''
Functions for simulations of different population genetics models.
Author: Julio Ayala
Date: 2020-10-29

'''
import numpy as np

# np.random.seed(1810)

def genetic_drift(n = 1000, freq = 0.5, g = 1000):
    '''
    Function to simulate genetic drift
    Arguments:
        n = population size
        g = generations
        freq = initial frequency of allele
    Returns: List of frequencies, and the fixation generation
    '''
    data = [[],[]]
    p_A = freq
    fixation_gen = 0
    for i in range(g): # Simulate for the maximum number of generations
        fixation_gen = i
        data[0].append(i)
        data[1].append(p_A)
        p_A = np.random.binomial(n, p_A)/n # The new allele fequency will be selected using a binomial distribution
        if (p_A==0 or p_A==1):
            break # Finishes when the allele fixates
    return data, fixation_gen

def genetic_drift_with_selection(n = 100000, freq = 0.5, h = 0.25, s = 0.2, g = 100):
    '''Function to simulate genetic drift with selection
    Arguments:
        n = population size
        freq = initial frequency of allele
        s = selection coefficient
        h = dominance coefficient
        g = generations
    Returns: List of frequencies, array of genotypes, and the fixation generation
    '''
    data = []
    genotype_data = []
    #Initial frequencies
    p_A = freq
    p_a = 1 - freq
    # Calculating the frequencies after selection
    w_AA = 1
    w_Aa = 1 - (h * s)
    w_aa = 1 - s
    # In g = 0, they follow the Hardy Weinberg equilibrium
    p_AA = p_A * p_A
    p_Aa = 2 * p_A * p_a
    p_aa = p_a * p_a
    fixation_gen = 0
    for i in range(g): # Repeat for all generations
        # Mean fitness (Constant of proportionality)
        wbar =  (p_AA * w_AA) + (p_Aa * w_Aa) + (p_aa * w_aa)
        # New frequencies after selection
        p_AA_wAA = p_AA * w_AA / wbar
        p_Aa_wAa = p_Aa * w_Aa / wbar
        p_aa_waa = p_aa * w_aa / wbar # Eq. to  1 - p_AA_wAA - p_Aa_wAa
        # Draw one sample of the population following a multinomial distribution
        new_population = np.random.multinomial(n, [p_AA_wAA, p_Aa_wAa, p_aa_waa], size = 1)
        genotype_data.append(new_population[0]/n)
        p_AA = new_population[0][0]/n
        p_Aa = new_population[0][1]/n
        p_aa = new_population[0][2]/n
        p_A = p_AA + 0.5 * p_Aa # Calculate the new allele frequencies
        p_a = p_aa + 0.5 * p_Aa
        data.append([p_A])
        fixation_gen = i
        if p_A == 0 or p_A ==1: # Finish when the allele reaches fixation
            break
    return data, genotype_data, fixation_gen
