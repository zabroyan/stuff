package bi.zum.lab3;

import cz.cvut.fit.zum.util.Pair;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import cz.cvut.fit.zum.api.ga.AbstractEvolution;
import cz.cvut.fit.zum.api.ga.AbstractIndividual;
import java.util.Random;
import org.openide.util.lookup.ServiceProvider;

/**
 * @author My name
 */
@ServiceProvider(service = AbstractEvolution.class)
public class Evolution extends AbstractEvolution<Individual> implements Runnable {

    /**
     * start and final average fitness
     */
    private Pair<Double, Double> avgFitness;
    private Pair<Double, Double> avgFitness2;
    private Pair<Double, Double> avgFitness3;
    /**
     * start and final best fitness in whole population
     */
    private Pair<Double, Double> bestFitness;
    private Pair<Double, Double> bestFitness2;
    private Pair<Double, Double> bestFitness3;
    /**
     * start and final time
     */
    private Pair<Long, Long> time;
    /**
     * How often to print status of evolution
     */
    private int debugLimit = 100;
    private Random rand = new Random();
    
    /**
     * The population to be used in the evolution
     */
            // first island
    Population population;
            // second island
    Population population2;
            // third island
     Population population3;

    public Evolution() {
        isFinished = false;
        avgFitness = new Pair<Double, Double>();
        bestFitness = new Pair<Double, Double>();
        
        avgFitness2 = new Pair<Double, Double>();
        bestFitness2 = new Pair<Double, Double>();
        
        avgFitness3 = new Pair<Double, Double>();
        bestFitness3 = new Pair<Double, Double>();
        
        time = new Pair<Long, Long>();        
    }

    @Override
    public String getName() {
        return "My semestralka's evolution";
    }

    @Override
    public void run() {
        
        // Initialize the population
        populationSize = populationSize / 3;
        population = new Population(this, populationSize);
        population2 = new Population(this, populationSize);
        population3 = new Population(this, populationSize);
        
        Random random = new Random();
        
        // Collect initial system time, average fitness, and the best fitness
        time.a = System.currentTimeMillis();
        avgFitness.a = population.getAvgFitness();
        AbstractIndividual best = population.getBestIndividual();
        bestFitness.a = best.getFitness();   
        
        avgFitness2.a = population2.getAvgFitness();
        AbstractIndividual best2 = population2.getBestIndividual();
        bestFitness2.a = best2.getFitness();  
        
        avgFitness3.a = population3.getAvgFitness();
        AbstractIndividual best3 = population3.getBestIndividual();
        bestFitness3.a = best3.getFitness();  

        // Show on map
        updateMap(best);
        System.out.println(population);
        System.out.println(population2);
        System.out.println(population3);

        int cnt = 0;
        int cnt2 = 0;
        int cnt3 = 0;
        int CatastropheCnt = 0;
        int lastFit = 0;
        int lastFit2 = 0;
        int lastFit3 = 0;
        // Run evolution cycle for the number of generations set in GUI
        for(int g = 0; g < generations; g++) {

            // the evolution may be terminate from the outside using GUI button
            if (isFinished) {
                break;
            }
            
            // initialize the next generation's population
            ArrayList<AbstractIndividual> newInds = new ArrayList<AbstractIndividual>();
            ArrayList<AbstractIndividual> newInds2 = new ArrayList<AbstractIndividual>();
            ArrayList<AbstractIndividual> newInds3 = new ArrayList<AbstractIndividual>();
            
            // elitism: Preserve the best individual
            // (this is quite exploatory and may lead to premature convergence!)
            newInds.add(population.getBestIndividual().deepCopy());
            newInds2.add(population2.getBestIndividual().deepCopy());
            newInds3.add(population3.getBestIndividual().deepCopy());

            // ISLAND MODEL
            // sends best individuals of the best population to others
            
            if (g == generations * 0.25 || g == generations * 0.5 || g == generations * 0.75 ) {
				int bestPopl = (int) population.getBestIndividual().getFitness();
				int bestPopl2 = (int) population2.getBestIndividual().getFitness();
				int bestPopl3 = (int) population3.getBestIndividual().getFitness();
			
				if (bestPopl >= bestPopl2 && bestPopl >= bestPopl3) { 
					// send elite from the first island
					System.out.println("send elite from the first island");
					List<AbstractIndividual> Elite = population.selectElite(populationSize/10, lastFit, populationSize);
					for(int i = 0; i < Elite.size(); i++)
                        population.setIndividualAt(i, Elite.get(i));
					}
				else if (bestPopl2 >= bestPopl && bestPopl2 >= bestPopl3) { 
					// send elite from the second island
					System.out.println("send elite from the second island");
					List<AbstractIndividual> Elite = population2.selectElite(populationSize/10, lastFit, populationSize);
					for(int i = 0; i < Elite.size(); i++)
                        population2.setIndividualAt(i, Elite.get(i));
					}
				else {
					// send elite from the third island
					System.out.println("send elite from the third island");
					List<AbstractIndividual> Elite = population3.selectElite(populationSize/10, lastFit, populationSize);
					for(int i = 0; i < Elite.size(); i++)
                        population3.setIndividualAt(i, Elite.get(i));
					}
            }
            //END OF ISLAND MODEL
            
            // CATASTROPHE
            //each island has its own catastrophe 
            if (lastFit == (int)population.getBestIndividual().getFitness()) 
                cnt++;
            else 
                cnt = 0;
            
            if (lastFit2 == (int)population2.getBestIndividual().getFitness()) 
                cnt2++;
            else 
                cnt2 = 0;
            
            if (lastFit3 == (int)population3.getBestIndividual().getFitness()) 
                cnt3++;
            else 
                cnt3 = 0;
            
            if (cnt == generations/25) {
                System.out.println("!!!!!CATASTROPHE!!!!!");
                CatastropheCnt++;
                
                List<AbstractIndividual> Elite = population.selectElite(populationSize/10, lastFit, populationSize);
                 
                population = new Population(this, populationSize);

                    for(int i = 0; i < Elite.size(); i++)
                        population.setIndividualAt(i, Elite.get(i));
                
                    cnt = 0;
            }
            
            if (cnt2 == generations/25) {
                System.out.println("!!!!!CATASTROPHE!!!!!");
                CatastropheCnt++;
                
                List<AbstractIndividual> Elite = population2.selectElite(populationSize/10, lastFit, populationSize);
                 
                population2 = new Population(this, populationSize);

                    for(int i = 0; i < Elite.size(); i++)
                        population2.setIndividualAt(i, Elite.get(i));
                
                    cnt = 0;
            }
            
            if (cnt3 == generations/25) {
                System.out.println("!!!!!CATASTROPHE!!!!!");
                CatastropheCnt++;
                
                List<AbstractIndividual> Elite = population3.selectElite(populationSize/10, lastFit, populationSize);
                 
                population3 = new Population(this, populationSize);

                    for(int i = 0; i < Elite.size(); i++)
                        population3.setIndividualAt(i, Elite.get(i));
                
                    cnt = 0;
            }
            
            lastFit = (int) population.getBestIndividual().getFitness();
            lastFit2 = (int) population2.getBestIndividual().getFitness();
            lastFit3 = (int) population3.getBestIndividual().getFitness();
            //END OF CATASTROPHE
            
            // keep filling the new population while not enough individuals in there
            while(     newInds.size() < populationSize 
                    || newInds2.size() < populationSize
                    || newInds3.size() < populationSize) {
                
                // select 2 parents
                List<AbstractIndividual> parents = population.selectIndividuals(2);
                List<AbstractIndividual> parents2 = population2.selectIndividuals(2);
                List<AbstractIndividual> parents3 = population3.selectIndividuals(2);
                
                Pair<AbstractIndividual,AbstractIndividual> offspring;
                Pair<AbstractIndividual,AbstractIndividual> offspring2;
                Pair<AbstractIndividual,AbstractIndividual> offspring3;
                
                // with some probability, perform crossover
                if(crossoverProbability < random.nextDouble()) {
                    offspring = parents.get(0).deepCopy().crossover(
                                    parents.get(1).deepCopy());
                }
                // otherwise, only copy the parents
                else {
                    offspring = new Pair<AbstractIndividual, AbstractIndividual>();
                    offspring.a = parents.get(0).deepCopy();
                    offspring.b = parents.get(1).deepCopy();
                }
                
                // with some probability, perform crossover
                if(crossoverProbability < random.nextDouble()) {
                    offspring2 = parents2.get(0).deepCopy().crossover(
                                    parents2.get(1).deepCopy());
                }
                // otherwise, only copy the parents
                else {
                    offspring2 = new Pair<AbstractIndividual, AbstractIndividual>();
                    offspring2.a = parents2.get(0).deepCopy();
                    offspring2.b = parents2.get(1).deepCopy();
                }
                
                // with some probability, perform crossover
                if(crossoverProbability < random.nextDouble()) {
                    offspring3 = parents3.get(0).deepCopy().crossover(
                                    parents3.get(1).deepCopy());
                }
                // otherwise, only copy the parents
                else {
                    offspring3 = new Pair<AbstractIndividual, AbstractIndividual>();
                    offspring3.a = parents3.get(0).deepCopy();
                    offspring3.b = parents3.get(1).deepCopy();
                }
                
                // mutate first offspring, add it to the new population
                offspring.a.mutate(mutationProbability);
                offspring.a.computeFitness();
                newInds.add(offspring.a);
                
                offspring2.a.mutate(mutationProbability);
                offspring2.a.computeFitness();
                newInds2.add(offspring2.a);
                
                offspring3.a.mutate(mutationProbability);
                offspring3.a.computeFitness();
                newInds3.add(offspring3.a);
                
                // if there is still space left in the new population, add also
                // the second offspring
                if(newInds.size() < populationSize) {
                    offspring.b.mutate(mutationProbability);
                    offspring.b.computeFitness();
                    newInds.add(offspring.b);
                }
                
                if(newInds2.size() < populationSize) {
                    offspring2.b.mutate(mutationProbability);
                    offspring2.b.computeFitness();
                    newInds2.add(offspring2.b);
                }
                
                if(newInds3.size() < populationSize) {
                    offspring3.b.mutate(mutationProbability);
                    offspring3.b.computeFitness();
                    newInds3.add(offspring3.b);
                }
            }
            
            // replace the current population with the new one
            for(int i = 0; i < newInds.size(); i++) {
                population.setIndividualAt(i, newInds.get(i));
            }
            
            for(int i = 0; i < newInds2.size(); i++) {
                population2.setIndividualAt(i, newInds2.get(i));
            }
            
            for(int i = 0; i < newInds3.size(); i++) {
                population3.setIndividualAt(i, newInds3.get(i));
            }
                    
            // print statistic
            System.out.println("gen1: " + g + "\t bestFit1: " + population.getBestIndividual().getFitness() + "\t avgFit1: " + population.getAvgFitness());
            System.out.println("gen2: " + g + "\t bestFit2: " + population2.getBestIndividual().getFitness() + "\t avgFit2: " + population2.getAvgFitness());
            System.out.println("gen3: " + g + "\t bestFit3: " + population3.getBestIndividual().getFitness() + "\t avgFit3: " + population3.getAvgFitness());
            // for very long evolutions print best individual each 1000 generations

            if (g % debugLimit == 0) {
                best = population.getBestIndividual();
                updateMap(best);
            }
            
            if (g % debugLimit == 0) {
                best2 = population2.getBestIndividual();
                updateMap(best2);
            }
            
            if (g % debugLimit == 0) {
                best3 = population3.getBestIndividual();
                updateMap(best3);
            }
            updateGenerationNumber(g);
        }

        // === END ===
        time.b = System.currentTimeMillis();
        population.sortByFitness();
        avgFitness.b = population.getAvgFitness();
        best = population.getBestIndividual();
        bestFitness.b = best.getFitness();
        //updateMap(best);
        
        population2.sortByFitness();
        avgFitness2.b = population2.getAvgFitness();
        best2 = population2.getBestIndividual();
        bestFitness2.b = best2.getFitness();
        //updateMap(best2);
        
        population3.sortByFitness();
        avgFitness3.b = population3.getAvgFitness();
        best3 = population3.getBestIndividual();
        bestFitness3.b = best3.getFitness();
        
        //print to the map only the best island
        AbstractIndividual the_best;
        if (bestFitness.b >= bestFitness2.b && bestFitness.b >= bestFitness3.b) 
            the_best = population.getBestIndividual();
        else if (bestFitness2.b >= bestFitness.b && bestFitness2.b >= bestFitness3.b) 
            the_best = population2.getBestIndividual();
        else 
            the_best = population3.getBestIndividual();
        updateMap(the_best);
        
        System.out.println("Evolution has finished after " + ((time.b - time.a) / 1000.0) + " s...");
        
        System.out.println("avgFit(G:0)= " + avgFitness.a + " avgFit(G:" + (generations - 1) + ")= " + avgFitness.b + " -> " + ((avgFitness.b / avgFitness.a) * 100) + " %");
        System.out.println("bstFit(G:0)= " + bestFitness.a + " bstFit(G:" + (generations - 1) + ")= " + bestFitness.b + " -> " + ((bestFitness.b / bestFitness.a) * 100) + " %");
        //System.out.println("bestIndividual= " + population.getBestIndividual());
        
        System.out.println("avgFit2(G:0)= " + avgFitness2.a + " avgFit2(G:" + (generations - 1) + ")= " + avgFitness2.b + " -> " + ((avgFitness2.b / avgFitness2.a) * 100) + " %");
        System.out.println("bstFit2(G:0)= " + bestFitness2.a + " bstFit2(G:" + (generations - 1) + ")= " + bestFitness2.b + " -> " + ((bestFitness2.b / bestFitness2.a) * 100) + " %");
        //System.out.println("bestIndividual2= " + population2.getBestIndividual());
        
        System.out.println("avgFit3(G:0)= " + avgFitness3.a + " avgFit3(G:" + (generations - 1) + ")= " + avgFitness3.b + " -> " + ((avgFitness3.b / avgFitness3.a) * 100) + " %");
        System.out.println("bstFit3(G:0)= " + bestFitness3.a + " bstFit3(G:" + (generations - 1) + ")= " + bestFitness3.b + " -> " + ((bestFitness3.b / bestFitness3.a) * 100) + " %");
        //System.out.println("bestIndividual3= " + population3.getBestIndividual());
        
        System.out.println("Catastrophe count = " + CatastropheCnt);
        //System.out.println(pop);

        isFinished = true;
        System.out.println("========== Evolution finished =============");
    }
}
