import random, copy

class Agent(object):
    '''
    Agents consist of a score trait and a rare trait.
    '''
    def __init__(self, score = 0, rareTrait = 0):
        self.score = score
        self.rareTrait = rareTrait

def mutate(agent, scoreMutationRate, scoreMutationRange, rareTraitMutationRate):
    '''
    '''
    mut_agent = Agent()
    # Mutations?
    score_mutation = random.random() < scoreMutationRate
    rareTrait_mutation = random.random() < rareTraitMutationRate
    # Mutate if mutations, otherwise don't mutate
    mut_agent.score = agent.score + (random.random() - 0.5) * scoreMutationRange if score_mutation else agent.score
    mut_agent.rareTrait = (agent.rareTrait + 1) & 1 if rareTrait_mutation else agent.rareTrait
    return mut_agent


def runsim(popSize, generations, numChallengers, scoreMutationRate, scoreMutationRange, rareTraitMutationRate):
    '''
    '''
    # TODO: make sure popSize is not 0
    # Randomly initialize the population with agents
    population = [Agent(score = random.random(), rareTrait = 0) for _ in range(0, popSize)]
    # Initialize average scores and rare trait counts
    #  - Indexed by generation #
    #  - Initialized to 0
    aveScores = [0 for _ in range(0, generations)]
    rareTraitCnt = [0 for _ in range(0, generations)]
    # Run simulation for # of generations equal to generations parameter
    for gen in range(0, generations):
        # Calculate current generation average score and rare trait count
        for agent in population:
            aveScores[gen] += agent.score
            rareTraitCnt[gen] += agent.rareTrait
        # calculate average score of pop from score sum
        aveScores[gen] /= popSize
        # Generate next generation with challenger selection
        new_population = []
        for i in range(0, popSize):
            # for each place in the new population,
            #   pick a member of current produce an offspring to populate new pop with
            challengerCount = 0                     # This will keep track of number of challengers so far
            winner = random.randint(0, popSize - 1) # pick a random initial winner
            for _ in range(0, numChallengers):
                # while there are still opportunities to challenge
                # Pick a new challenger from population
                challenger = random.randint(0, popSize - 1)
                # if the challenger is better than the current winner
                if population[challenger].score > population[winner].score:
                    # challenger wins
                    winner = challenger
            # Winner from tournament
            new_population.append(mutate(population[winner], scoreMutationRate, scoreMutationRange, rareTraitMutationRate))
        population = new_population
    # Return sim results
    return (aveScores, rareTraitCnt)







if __name__ == "__main__":
    popSize = 1000
    generations = 3000
    scoreMutationRate = 0.05
    scoreMutationRange = 0.025
    rareTraitMutationRate = 0.0001
    numChallengers = 1.0
    conditions = [1, 2, 4, 8]

    conditionCnt = 5
    testsPerCondition = 4

    scoreData = []
    rareData = []

    for condition in conditions:
        for i in range(0, testsPerCondition):
            numChallengers = condition
            print("=================")
            print("Condition:")
            print(" - Challenger Count: " + str(numChallengers))
            print(" - Generations: " + str(generations))
            output = runsim(popSize, generations, numChallengers, scoreMutationRate, scoreMutationRange, rareTraitMutationRate)
            print("Other stats...")
            scoreData.append(output[0])
            rareData.append(output[1])
