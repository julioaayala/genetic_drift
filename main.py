#!/usr/bin/python3
'''
Main
Author: Julio Ayala
'''
from genetic_drift import *
import argparse
p = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)

p.add_argument('-m', '--method',
    dest = 'method',
    choices = ['genetic_drift', 'wright_fisher'],
    default = 'genetic_drift')

p.add_argument('-n',
    dest = 'population_size',
    help = 'Population size',
    type = int,
    default = 100)

p.add_argument('-f',
    dest = 'freq',
    help = 'Frequency of allele',
    type = float,
    default = 0.5)

p.add_argument('-g',
    dest = 'generations',
    help = 'Maximum number of generations to simulate',
    type = int,
    default = 1000)

p.add_argument('-s',
    dest = 'selection_coef',
    help = 'Selection coefficient (When method is Wright Fisher)',
    type = float,
    default = 0.2)

p.add_argument('-d',
    dest = 'dominance_coef',
    help = 'Dominance coefficient (h) (When method is Wright Fisher)',
    type = float,
    default = 0.25)

p.add_argument('-r',
    dest = 'repetitions',
    help = 'Number of simulations',
    type = int,
    default = 3)

p.add_argument('-v', '--verbose', action="store_true", help = 'Print statistics')


args = p.parse_args()

if args.method == 'genetic_drift':
    ax1 = plt.subplot(2,1,1)
    avgs = [[],[]]
    cmap = plt.get_cmap('viridis')
    max_gen = 10000
    min_pop = 10
    max_pop = 1000000
    increment = 10
    trials = 2

    i = min_pop
    while i <= max_pop:
        print(i)
        pop_freq = []
        sim = genetic_drift(n=i, freq=0.5, g=max_gen, trials=trials)

        for trial in sim:
            for j in trial[1]:
                pop_freq.append(j)
            pop_freq += [trial[1][-1]] * (max_gen - len(trial[1]))
        avgs[0].append(i)
        avgs[1].append(sum(pop_freq)/len(pop_freq))
        pop_freq = []
        for j in range(len(sim)):
            x=0
            # ax1.plot(sim[j][0], sim[j][1], c=cmap(float(i)/max_pop))
            ax1.plot(sim[j][0], sim[j][1], label = i)
        i = i*increment

    ax1.legend(loc='lower right', title = 'Population size', frameon=False, ncol = 3)
    ax1.set_title('Freq of allele for different population sizes')
    ax1.set_ylabel('Freq of allele')
    ax1.set_xlabel('Generation')
    ax1.set_xlim(0, max_gen)
    ax1.set_ylim([0, 1])


    ax2 = plt.subplot(2,1,2)
    ax2.plot(avgs[0], avgs[1])
    ax2.set_xlim(min(avgs[0]), max(avgs[0]))
    ax2.set_ylim([0, 1])
    ax2.set_title('Average frequency over {} generations for different population sizes'.format(max_gen))
    ax2.set_ylabel('Avg Freq')
    ax2.set_xlabel('Population size')
    plt.show()


if args.method == 'wright_fisher':
    fig = plt.figure()
    ax1 = plt.subplot(1,1,1)
    ax1.set_title('Freq of allele following a Wright Fisher genetic drift model')
    ax1.set_ylabel('Freq of allele')
    ax1.set_xlabel('Generation')
    cmap = plt.get_cmap('viridis')
    rep = args.repetitions
    n = args.population_size
    freq = args.freq
    h = args.dominance_coef
    s = args.selection_coef
    g = args.generations
    for i in range(rep):
        data, genotype_data = wright_fisher(n = n, freq = freq, h = h, s = s, g = g)
        data = np.array(data)
        ax1.plot(data, c=cmap(float(i)/rep))

    if args.verbose:
        print('Stats')
    plt.show()
