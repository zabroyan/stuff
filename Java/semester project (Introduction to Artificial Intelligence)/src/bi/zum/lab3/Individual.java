package bi.zum.lab3;

import cz.cvut.fit.zum.api.ga.AbstractEvolution;
import cz.cvut.fit.zum.api.ga.AbstractIndividual;
import cz.cvut.fit.zum.data.Edge;
import cz.cvut.fit.zum.data.StateSpace;
import cz.cvut.fit.zum.util.Pair;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;
import java.util.List;


/**
 * @author My Name
 */
public class Individual extends AbstractIndividual {

    private double fitness = Double.NaN;
    private AbstractEvolution evolution;
    
    private Random random;
    boolean[] genome;    
    

    /**
     * Creates a new individual
     * 
     * @param evolution The evolution object
     * @param randomInit <code>true</code> if the individial should be
     * initialized randomly (we do wish to initialize if we copy the individual)
     */
    public Individual(AbstractEvolution evolution, boolean randomInit) {
        this.evolution = evolution;
        this.random = new Random();
        this.genome = new boolean[evolution.getNodesCount()];
        
        if(randomInit) {  //random genome
            for(int i = 0; i < evolution.getNodesCount(); i++) 
                this.genome[i] = random.nextBoolean();
            
            this.repair();
            this.hillClimbing();
        }
    }
    @Override
    public boolean isNodeSelected(int j) {
        
        return this.genome[j]; //1 or 0
    }
    /**
     * Evaluate the value of the fitness function for the individual. After
     * the fitness is computed, the <code>getFitness</code> may be called
     * repeatedly, saving computation time.
     */
    @Override
    public void computeFitness() {
        
        //double res = StateSpace.nodesCount();
        double res = 0;
        for(int i = 0; i < this.genome.length; i++) {
            if(!this.genome[i]) 
                res++;
        }

        this.fitness = res; 
    }
    /**
     * Only return the computed fitness value
     *
     * @return value of fitness fucntion
     */
    @Override
    public double getFitness() {
        return this.fitness;
    }
    /**
     * Does random changes in the individual's genotype, taking mutation
     * probability into account.
     * 
     * @param mutationRate Probability of a bit being inverted, i.e. a node
     * being added to/removed from the vertex cover.
     */
    @Override
    public void mutate(double mutationRate) {
        
        Random r = new Random();
        int rand = r.nextInt(genome.length);
         for(int i = 0; i < genome.length; i++) {
            if( rand < mutationRate ) {
                this.genome[i] = !this.genome[i];
            }
        }
        this.repair();
    }
    /**
     * Crosses the current individual over with other individual given as a
     * parameter, yielding a pair of offsprings.
     * 
     * @param other The other individual to be crossed over with
     * @return A couple of offspring individuals
     */
    
    // HILL CLIMBING
    // creates similar individuals with better fitness
    // is used in initialization and crossover 
    public void hillClimbing() {        
        int i = 0;                      
        double HLRate = 0.15;    
        Random r = new Random();
        Individual ind = this.deepCopy();
        while ( i < StateSpace.nodesCount()/2000 && this.getFitness() >= ind.getFitness() ) {
           
            for ( int j = 0; j < ind.genome.length; j++ ) {
                    int rand = r.nextInt(ind.genome.length);
                if ( rand < HLRate )  {      
                    ind.genome[j] = !ind.genome[j]; 
                }
            }
            i++;
            ind.repair(); 
        }
        
        System.arraycopy(ind.genome, 0, genome, 0, genome.length);
    }
    
    // DETERMINISTIC CROWDING
    // copmares parents to child using Hamming distance
    // returns less similar parent to leave, kill another one
    public Individual deterministicCrowding ( Individual p1, 
                            Individual p2, Individual o   ) {
        int p1_diff = 0;
        int p2_diff = 0; 
        
        for ( int i = 0; i < p1.genome.length; i++) 
            if ( p1.genome[i] != o.genome[i] ) 
                p1_diff++;
        
        for ( int i = 0; i < p2.genome.length; i++) 
            if ( p2.genome[i] != o.genome[i] ) 
                p2_diff++;
        
        if ( p1_diff > p2_diff ) {
            return p1;
        } else return p2; 
    }
    
    @Override
    public Pair crossover(AbstractIndividual other) {

        Pair<Individual,Individual> result = new Pair();
        Random r = new Random();
        int rand = r.nextInt(genome.length);
        
        Individual p1 = (Individual) other.deepCopy();
        Individual p2 = this.deepCopy();
        
        Individual child = p2.deepCopy();
        for ( int i = rand; i < genome.length; i++ ) 
            child.genome[i] = p1.genome[i]; 
        
        child.repair();
        
        if ( p1 == deterministicCrowding(p1, p2, child) ) { 
            child.hillClimbing();
                result.a = child;
                result.b = p1;   
        } else { 
            child.hillClimbing();
                result.b = child;
                result.a = p2;
        }
        
        return result;
    }
    /**
     * When you are changing an individual (eg. at crossover) you probably don't
     * want to affect the old one (you don't want to destruct it). So you have
     * to implement "deep copy" of this object.
     *
     * @return identical individual
     */
    @Override
    public Individual deepCopy() {
        Individual newOne = new Individual(evolution, false);
        System.arraycopy(this.genome, 0, newOne.genome, 0, this.genome.length);

        // TODO: at least you should copy your representation of search-space state

        // for primitive types int, double, ...
        // newOne.val = this.val;

        // for objects (String, ...)
        // for your own objects you have to implement clone (override original inherited from Objcet)
        // newOne.infoObj = thi.infoObj.clone();

        // for arrays and collections (ArrayList, int[], Node[]...)
        /*
         // new array of the same length
         newOne.pole = new MyObjects[this.pole.length];		
         // clone all items
         for (int i = 0; i < this.pole.length; i++) {
         newOne.pole[i] = this.pole[i].clone(); // object
         // in case of array of primitive types - direct assign
         //newOne.pole[i] = this.pole[i]; 
         }
         // for collections -> make new instance and clone in for/foreach cycle all members from old to new
         */

        newOne.fitness = this.fitness;
        return newOne;
    }
    private void repair() {
 
        /* We iterate over all the edges */
        for(Edge e : StateSpace.getEdges()) {
 
            if(!this.genome[e.getFromId()] && !this.genome[e.getToId()]) {
                if(random.nextBoolean()) {
                    this.genome[e.getFromId()] = true;
                }
                else {
                    this.genome[e.getToId()] = true;
                }
            }
        }
    }
    /**
     * Return a string representation of the individual.
     *
     * @return The string representing this object.
     */
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        
        boolean first = true;
        for(int i = 0; i < this.genome.length; i++) {
            if(this.genome[i]) {
                if(first) {
                    first = false;
                }
                else {
                    sb.append(",");
                }
                sb.append(i);
            }
        }

        return sb.toString();
    }
}

