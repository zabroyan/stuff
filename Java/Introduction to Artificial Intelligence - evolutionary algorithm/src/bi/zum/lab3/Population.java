package bi.zum.lab3;

import cz.cvut.fit.zum.api.ga.AbstractEvolution;
import cz.cvut.fit.zum.api.ga.AbstractIndividual;
import cz.cvut.fit.zum.api.ga.AbstractPopulation;
import cz.cvut.fit.zum.data.StateSpace;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * @author My name
 */
public class Population extends AbstractPopulation {

    private Random random;
    public Population(AbstractEvolution evolution, int size) {
        individuals = new Individual[size];
        for (int i = 0; i < individuals.length; i++) {
            individuals[i] = new Individual(evolution, true);
            individuals[i].computeFitness();
        }
        this.random = new Random();
    }

    /**
     * Method to select individuals from population
     *
     * @param count The number of individuals to be selected
     * @return List of selected individuals
     */
    public List<AbstractIndividual> selectIndividuals(int count) {
        ArrayList<AbstractIndividual> selected = new ArrayList<AbstractIndividual>();
        
        for(int i = 0; i<count; i++) {
            
            double bestFitness = Double.NEGATIVE_INFINITY;
            AbstractIndividual theBest = null;
            
            for(int j = 0; j < 15; j++) {
                
                AbstractIndividual candidate = this.individuals[random.nextInt(this.individuals.length)];
                if(candidate.getFitness() > bestFitness) {
                    theBest = candidate;
                    bestFitness = candidate.getFitness();
                }
            }
            
            selected.add(theBest);
        }

        
        return selected;
    }
    
    //SELECT ELITE
    public List<AbstractIndividual> selectElite(int cnt, int fitness, int size) {
        ArrayList<AbstractIndividual> selected = new ArrayList<AbstractIndividual>();
        for(int i = 0; i < size; i++) {
                AbstractIndividual candidate = this.individuals[random.nextInt(this.individuals.length)];
                if(candidate.getFitness() == fitness) {
                    selected.add(candidate);
                    cnt--;
                }  
                if ( cnt == 0 ) 
                    break;
        }
        return selected;
    }
}