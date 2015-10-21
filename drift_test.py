import random, copy, json
import matplotlib.pyplot as plt


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

def simple_get_line_color(i):
    COLORS = ['r', 'b', 'g', 'c', 'm', 'y', 'k']
    index = i % len(COLORS)
    return COLORS[index]


if __name__ == "__main__":
    settings_file = "settings.json"
    # Extract settings from settings file
    with open(settings_file) as fp:
        settings = json.load(fp)

    print("Loaded settings: " + str(settings))
    popSize = settings["population_size"]
    generations = settings["generations"]
    scoreMutationRate = settings["score_mutation_rate"]
    scoreMutationRange = settings["score_mutation_range"]
    rareTraitMutationRate = settings["rare_trait_mutation_rate"]
    conditions = settings["num_challenger_conditions"]
    testsPerCondition = settings["tests_per_condition"]

    scoreData = []
    rareData = []

    # Run each condition
    for condition in conditions:
        # Run some number of trials per condition
        for i in range(0, testsPerCondition):
            # Get number of challengers parameter
            numChallengers = condition
            print("=================")
            print("Condition:")
            print(" - Challenger Count: " + str(numChallengers))
            print(" - Generations: " + str(generations))
            # Run the simulation
            output = runsim(popSize, generations, numChallengers, scoreMutationRate, scoreMutationRange, rareTraitMutationRate)
            print("Final avg score: " + str(output[0][-1]))
            print("Final rareTraitCount: " + str(output[1][-1]))
            # Store data from run
            scoreData.append(output[0])
            rareData.append(output[1])

    # Plot!
    for k in range(0, len(conditions)):
        plt.figure(figsize = (8, 6))
        plt.subplot(2, 1, 1)
        for i in range(0, testsPerCondition):
            plt.plot(scoreData[(k * testsPerCondition) + i], label = "Score", color = simple_get_line_color(i), linewidth = 2)
        if k > 0:
            plt.ylim(0, 20)
        plt.title("Population Size: %d; Number of Challengers: %d" % (popSize, conditions[k]))
        plt.xlabel("Time (in Updates)")
        plt.ylabel("Average Score")
        plt.subplot(2, 1, 2)
        for i in range(0, testsPerCondition):
            plt.plot(rareData[(k * testsPerCondition) + i], label = "Rare Trait Count", color = simple_get_line_color(i), linewidth = 2)

        plt.ylim(-50, popSize + 50)
        plt.ylabel("Rare Trait Count")
        plt.xlabel("Time (in Updates)")
        plt.savefig("pop%d_numChall%d.png" % (popSize, conditions[k]), dpi = 100)

    plt.show()
