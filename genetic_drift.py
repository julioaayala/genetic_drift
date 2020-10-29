import numpy as np
import matplotlib.pyplot as plt

# np.random.seed(1810)

def genetic_drift(n = 1000, freq = 0.5, g = 1000, trials = 10):
    '''
    n = population size
    g = generations
    freq = initial frequency of allele

    '''
    all_data = []
    data = [[],[]]
    # freqs = []
    for trial in range(trials):
        p_A = freq
        for i in range(g):
            data[0].append(i)
            data[1].append(p_A)
            p_A = np.random.binomial(n, p_A)/n
            # freqs.append(p_A)
            if p_A==0 or p_A==1:
                break # Finishes when it finds the equlibrium point
        # freqs += [data[1][-1]] * (g - len(data[1]))
        all_data.append(data)
        data = [[],[]]
    # return all_data, sum(freqs)/len(freqs)
    return all_data

def wright_fisher(n = 100000, freq = 0.5, h = 0.25, s = 0.2, g = 100):
    '''
    n = population size
    freq = initial frequency of allele
    s = selection coefficient
    h = dominance coefficient
    g = generations
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

    # In g = 0, they follow a Hardy Weinberg equilibrium
    p_AA = p_A * p_A
    p_Aa = 2 * p_A * p_a
    p_aa = p_a * p_a

    for i in range(g): # Repeat for all generations
        # Mean fitness (Constant of proportionality)
        wbar =  (p_AA * w_AA) + (p_Aa * w_Aa) + (p_aa * w_aa)
        # New frequencies after selection
        p_AA_wAA = p_AA * w_AA / wbar
        p_Aa_wAa = p_Aa * w_Aa / wbar
        p_aa_waa = p_aa * w_aa / wbar # Eq. to  1 - p_AA_wAA - p_Aa_wAa
        new_population = np.random.multinomial(n, [p_AA_wAA, p_Aa_wAa, p_aa_waa], size = 1)
        genotype_data.append(new_population[0]/n)
        p_AA = new_population[0][0]/n
        p_Aa = new_population[0][1]/n
        p_aa = new_population[0][2]/n
        p_A = p_AA + 0.5 * p_Aa
        p_a = p_aa + 0.5 * p_Aa
        data.append([p_A])
        if p_A == 0 or p_A ==1:
            break
    return data, genotype_data
