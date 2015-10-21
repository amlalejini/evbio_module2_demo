
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.backends.backend_pdf import PdfPages
import random
from copy import deepcopy
import sys, time

def runsim():
# make a population of Agents
  population = []
  for i in range(popSize):
    population.append([random.random(),0])

  AveScores = []
  RareTraitCount = []
  for gen in range(generations):
    # saveState
    AveScores.append(0)
    RareTraitCount.append(0)
    for agent in population:
      AveScores[gen] = AveScores[gen] + agent[0]
      RareTraitCount[gen] = RareTraitCount[gen] + agent[1]
    AveScores[gen] = AveScores[gen]/popSize
    #print(gen,AveScores[gen],RareTraitCount[gen])
    #sys.stdout.flush()
    # make new population
    new_population = []
    for i in range(popSize):
      challengerCount = 0
      winner = random.randint(0, popSize-1)
      while challengerCount < numChallengers:
        challenger = random.randint(0, popSize-1)
        if population[challenger][0] > population[winner][0]:
          winner = challenger
        challengerCount = challengerCount + 1
      new_population.append(deepcopy(population[winner]))
    population = deepcopy(new_population)
    # mutate
    for i in range(popSize):
      if random.random() < scoreMutationRate:
        population[i][0] = population[i][0]+((random.random()-.5)*scoreMutationRange)
      if random.random() < rareTraitMutationRate:
        population[i][1] = (population[i][1]+1)&1
  return [AveScores,RareTraitCount]



# Agent[Score,rareTrait]
popSize = 1000
generations = 3000
scoreMutationRate = .05
scoreMutationRange = .025
rareTraitMutationRate = .0001
numChallengers = 1 # set 0 for random selection


testsPerCondition = 4

scoreData = []
RareData = []

for outterCount in range(5):
  numChallengers = 2*outterCount
  for i in range(testsPerCondition):
    print(numChallengers)
    output = runsim()
    scoreData.append(output[0])
    RareData.append(output[1])



for outterCount in range(5):
  plt.figure(figsize=(8,6))
  plt.subplot(2,1,1)
  for i in range(testsPerCondition):
    plt.plot(scoreData[(outterCount*4)+i],label = "Score",color = 'b', linewidth = 2)
  if outterCount > 0:
    plt.ylim(0,20)
  plt.title('NumberOfChallengers_'+str(2*outterCount)+'__Population_'+str(popSize), fontsize=15,fontweight='bold')
  plt.subplot(2,1,2)
  for i in range(testsPerCondition):
    plt.plot(RareData[(outterCount*4)+i], label = "rareTraitCount", color = 'r', linewidth = 2)

  plt.ylim(-50,popSize+50)
  plt.xlabel('Time (in Updates)')
  plt.savefig('NumberOfChallengers_'+str(2*outterCount)+'_Population_'+str(popSize)+'.png', dpi=100)

plt.show()
