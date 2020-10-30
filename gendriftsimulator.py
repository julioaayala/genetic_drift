#!/usr/bin/python3
'''
Program to simulate genetic drift and selection.
Author: Julio Ayala
'''
import argparse
import popgen as pg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__,
                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

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

    p.add_argument('-r',
        dest = 'repetitions',
        help = 'Number of simulations',
        type = int,
        default = 3)

    p.add_argument('--with_selection', action="store_true", help = 'Add selection to the model')
    p.add_argument('-s',
    dest = 'selection_coef',
    help = 'Selection coefficient (When the model applies selection)',
    type = float,
    default = 0.2)

    p.add_argument('-d',
    dest = 'dominance_coef',
    help = 'Dominance coefficient (h) (When the model applies selection)',
    type = float,
    default = 0.25)

    p.add_argument('--export', action="store_true", help = 'Export plot to file (PNG for regular drift, or GIF for selection simulation (Note: GIF files can get big with a high number of generations))')

    args = p.parse_args()

    if not args.with_selection: # Simulating genetic drift without selection
        # Get parameters
        rep = args.repetitions
        n = args.population_size
        freq = args.freq
        g = args.generations
        pop_freq = []
        fixation = []

        # Initialize plot
        plt.figure(figsize=(12, 10))
        ax1 = plt.subplot(1,1,1)
        cmap = plt.get_cmap('viridis')
        for i in range(rep): # Simulate for each repetition
            sim, fixation_gen = pg.genetic_drift(n = n, freq=0.5, g=g)
            pop_freq.append(sim[1][-1]) # Adds the last frequency and fixation generation to an array to show the average
            if fixation_gen != g - 1:
                fixation.append(fixation_gen)

            ax1.plot(sim[0], sim[1], c=cmap(float(i)/rep))
        #Setting labels and titles
        ax1.set_title('Genetic drift: Frequency of allele over up to {} generations\n (N={}, freq in gen 0={}, {} repetitions)'.format(g, n, freq, rep))
        ax1.set_ylabel('Frequency')
        ax1.set_xlabel('Generation')
        ax1.set_ylim([0, 1])
        f_text = 'Average frequency in last generation: {}'.format(round(sum(pop_freq)/len(pop_freq),3))
        g_text = 'Average # of gen to fixation: {}'.format(int(sum(fixation)/len(fixation)) if len(fixation) > 0 else 'None of the repetitions reached fixation')
        ax1.text(0.5,-0.1, f'{f_text}\n{g_text}', size=12, ha="center", transform=ax1.transAxes) #Adding the averages at the bottom
        if args.export:
            plt.savefig('{}.png'.format(datetime.now().strftime("%Y%m%d%H%M%S")))
        plt.show()


    if args.with_selection:
        rep = args.repetitions
        n = args.population_size
        freq = args.freq
        h = args.dominance_coef
        s = args.selection_coef
        g = args.generations
        pop_freq = []
        fixation = []

        fig = plt.figure(figsize=(12, 10))
        ax1 = plt.subplot(2,1,1)
        ax1.set_title('Freq of allele in a Wright-Fisher model with selection\n (N={}, h={}, s = {}, freq in gen 0={}, {} repetitions)'.format(n, h, s, freq, rep))
        ax1.set_ylabel('Frequency')
        ax1.set_xlabel('Generation')
        cmap = plt.get_cmap('viridis') # Apply the color palette
        for i in range(rep): #Simulate for each repetition
            data, genotype_data, fixation_gen = pg.genetic_drift_with_selection(n = n, freq = freq, h = h, s = s, g = g)
            pop_freq.append(data[-1][-1]) # Adds the last frequency and fixation generation to an array to show the average
            if fixation_gen != g - 1:
                fixation.append(fixation_gen)
            ax1.plot(data, c=cmap(float(i)/rep))


        ax2 = plt.subplot(2,1,2) # Create the subplot for the genotype frequency
        p1 = plt.bar([], [])
        rects = plt.bar(['AA', 'Aa', 'aa'], genotype_data[0], color=cmap(float(i)/rep))
        ax2.set_ylim(0, 1)
        ax2.set_title('Frequency of genotype')
        ax2.set_ylabel('Frequency')
        ax2.set_xlabel('Genotype')
        def animate(i): # Animate function, to update the bar plot
            for barchart, yi in zip(rects, genotype_data[i]):
                barchart.set_height(yi)
                ax2.set_title('Frequency of genotypes in generation {} (Last repetition)'.format(i))
            return rects

        f_text = 'Average frequency in last generation: {}'.format(round(sum(pop_freq)/len(pop_freq),3))
        g_text = 'Average # of gen to fixation: {}'.format(int(sum(fixation)/len(fixation)) if len(fixation) > 0 else 'None of the repetitions reached fixation')
        ax2.text(0.5,-0.23, f'{f_text}\n{g_text}', size=12, ha="center", transform=ax2.transAxes) #Adding the averages at the bottom
        anim = animation.FuncAnimation(fig, animate, frames=len(genotype_data), interval=100, repeat=False) #Animate without repetition
        if args.export:
            anim.save('{}.png'.format(datetime.now().strftime("%Y%m%d%H%M%S")), writer='pillow', fps=30) # To save the animation. TODO: Adjust fps to # of generations, as to not to increase file size too much
        plt.show()
