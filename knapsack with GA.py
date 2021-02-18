#   solving knapsack problem with n item and random values with GA(genetic algorithm) 
#   by mohammad asadolahi
#   mohmad.asa1994@gmail.com
import random

from matplotlib import pyplot as plt


class Chromosome:
    def __init__(self, solution, value, weight, absoluteWorth):
        self.solution = solution
        self.value = value
        self.weight = weight
        self.absoluteWorth = absoluteWorth


class GeneticSolver:
    def __init__(self, populationSize, generationCount, mutationRate, itemCount, threshold):
        self.populationSize = populationSize
        self.generationCount = generationCount
        self.mutationRate = mutationRate
        self.threshold = threshold
        self.population = []
        self.elitePopulation = []
        self.generationAverage = []
        self.invalidPopulation = []
        self.itemCount = itemCount
        self.objects = []  #[{43: 29}, {53: 36}, {55: 28}, {68: 38}, {46: 29}, {64: 23}, {69: 21}, {40: 36}, {77: 21}, {80: 36}, {65: 37}, {49: 25}, {68: 35}, {61: 25}, {67: 37}, {72: 34}, {57: 33}, {45: 22}, {46: 31}, {51: 24}]

        self.initialPopulation()

    def initialPopulation(self):
        for i in range(0, self.itemCount):
            self.objects.append({random.randint(int(self.threshold / 10),int(self.threshold / 5)): random.randint(
                int(self.threshold / 20), int(self.threshold /10))})
        index = 0
        while index < self.populationSize:
            solution = []
            for number in range(0, self.itemCount):
                solution.append(random.randint(0, 1))
            tmpChromosome = self.generateChromosome(solution)
            if (tmpChromosome.value != 0) and tmpChromosome.weight <= self.threshold and (
                    not self.isChromosomeExist(self.population, tmpChromosome)):
                self.population.append(tmpChromosome)
                index += 1
        self.population.sort(key=lambda chrom: chrom.absoluteWorth, reverse=True)
        self.elitePopulation.append(self.population[0])
        self.generationAverage.append((sum(chrom.absoluteWorth for chrom in self.population)) / self.populationSize)

    def getSolutionProperties(self, solution):
        chromosomeValue = 0
        chromosomeWeight = 0
        chromosomeAbsoluteWeight = 0
        index = 0
        for case in solution:
            if case == 1:
                value, weight = zip(*(self.objects[index].items()))
                chromosomeValue += value[0]
                chromosomeWeight += weight[0]
            index += 1
        if (chromosomeWeight != 0):
            chromosomeAbsoluteWeight = (chromosomeValue * chromosomeWeight - (
                    chromosomeValue * abs(self.threshold - chromosomeWeight))) / chromosomeWeight
        return [chromosomeValue, chromosomeWeight, chromosomeAbsoluteWeight]

    def generateChromosome(self, solution):
        chromosomeProperties = self.getSolutionProperties(solution)
        return Chromosome(solution[::], chromosomeProperties[0], chromosomeProperties[1], chromosomeProperties[2])

    def mutate(self, population, chromosome):
        tmpChromosome = self.generateChromosome(chromosome.solution[::])
        while self.isChromosomeExist(population, tmpChromosome) or (
                not (1 in tmpChromosome.solution)) or tmpChromosome.weight > self.threshold:
            mutationIndex = random.randint(0, len(chromosome.solution) - 1)
            if tmpChromosome.solution[mutationIndex] == 1:
                tmpChromosome.solution[mutationIndex] = 0
            else:
                tmpChromosome.solution[mutationIndex] = 1
            tmpChromosome = self.generateChromosome(tmpChromosome.solution[::])
        return self.generateChromosome(tmpChromosome.solution[::])

    def isChromosomeExist(self, population, chromosome):
        for gene in population:
            if gene.solution == chromosome.solution:
                return True
        return False

    def printPopulation(self):
        for chromosome in self.population:
            print(
                f"{chromosome.solution} with value: {chromosome.value} and weight: {chromosome.weight} and absolute worth: {chromosome.absoluteWorth}")

    def printElitePopulation(self):
        generation = 0
        print("******************************************************************************************")
        print(f"printing elite chromosomes of all generations")
        for chromosome in self.elitePopulation:
            print(
                f"elite chromosome of generation:{generation} is: {chromosome.solution} with value: {chromosome.value} and weight: {chromosome.weight} and absolute worth: {chromosome.absoluteWorth}")
            generation += 1
        print("******************************************************************************************")
        index = 0
        answer = ""
        for innercase in (self.elitePopulation.pop().solution):
            if innercase == 1:
                value, weight = zip(*(self.objects[index].items()))
                print(
                    f"object{index} value: {value[0]}  and weight: {weight[0]} and absolute worth: {chromosome.absoluteWorth}")
            index += 1

    def crossOver(self, firstParent, secondParent):
        crossOverPosition = int(len(firstParent.solution) / 2)
        return firstParent.solution[0:crossOverPosition] + secondParent.solution[
                                                           crossOverPosition:len(firstParent.solution)]

    def lunchEvolution(self):
        generation = 0
        while generation < self.generationCount:
            print("******************************************************************************************")
            print(f"generation: {generation}")
            newPopulation = self.population[::]
            crossoverIndex = 0
            while crossoverIndex < self.populationSize:
                firstChildPprobability = random.randint(0, 100)
                secondChildPprobability = random.randint(0, 100)
                child1 = self.generateChromosome(
                    self.crossOver(self.population[crossoverIndex], self.population[crossoverIndex + 1]))
                if (child1.value == 0) or (firstChildPprobability < self.mutationRate) or self.isChromosomeExist(
                        newPopulation, child1) or child1.weight > self.threshold:
                    child1 = self.mutate(newPopulation, child1)
                newPopulation.append(child1)
                child2 = self.generateChromosome(
                    self.crossOver(self.population[crossoverIndex + 1], self.population[crossoverIndex]))
                if (child2.value == 0) or (secondChildPprobability < self.mutationRate) or self.isChromosomeExist(
                        newPopulation, child2) or child2.weight > self.threshold:
                    child2 = self.mutate(newPopulation, child2)
                newPopulation.append(child2)
                crossoverIndex += 2
            newPopulation.sort(key=lambda chromosome: chromosome.absoluteWorth, reverse=True)
            self.population.clear()
            self.population = newPopulation[0:self.populationSize]
            self.elitePopulation.append(self.population[0])
            self.generationAverage.append((sum(x.absoluteWorth for x in self.population)) / self.populationSize)
            print(
                f"the best arrange of generation: {generation} is{self.elitePopulation[generation].solution} "
                f"wit" f"h {self.elitePopulation[generation].value} values and wight: {self.elitePopulation[generation].weight} and absolute worth: {self.elitePopulation[generation].absoluteWorth}")
            print(
                f"the average worth of generation: {generation} is {self.generationAverage[generation]} ")
            self.printPopulation()
            generation += 1

    def solve(self):
        self.lunchEvolution()
        plt.plot([x.absoluteWorth for x in self.elitePopulation], label="Elites")
        plt.xlabel('x - Generations')
        plt.ylabel('y - Absolute Worth ')
        plt.title('Evolution of elite chromosomes')
        plt.show()

        plt.plot([x for x in self.generationAverage], label="Average of Absolute Worth")
        plt.title('Averge Absolute Worth of each generatins')
        plt.xlabel('x - Generation')
        plt.ylabel('y - Absolute Worth ')
        plt.show()

        plt.plot([x.absoluteWorth for x in self.elitePopulation], label="Elites")
        plt.xlabel('x - Generations')
        plt.ylabel('y - Absolute Worth ')
        plt.title('Evolution of elite chromosomes')
        plt.legend()
        plt.plot([x for x in self.generationAverage], label="Average worthes")
        plt.xlabel('x - Generations')
        plt.ylabel('y - Absolute Worth ')
        plt.title('Averge Absolute Worth of each generatins')
        plt.legend()
        plt.show()
        print(self.objects)

# populationSize, generationCount, mutationRate, itemCount, threshold
#knapsack = GeneticSolver(6, 200, 10, 10, 100)
knapsack = GeneticSolver(10, 100, 20, 20, 400) #generated objects are produced for this properties
# knapsack = GeneticSolver(10, 80, 10, 25, 600)

knapsack.solve()
# knapsack.printElitePopulation()
