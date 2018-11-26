import pygame
import sys
import random
import math
from numpy import interp

pygame.init()

width = 1320
height = 710
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Genetic Algorithm")
clock = pygame.time.Clock()

small_font = pygame.font.SysFont("Courier", 18)
medium_font = pygame.font.SysFont("Courier", 25)
large_font = pygame.font.SysFont("Courier", 50)

background = (255, 255, 255)
body = (0, 0, 0)

# ------------------------------------------------------------------------------


def newChar():
	# print("newChar")
	c = math.floor(random.randint(63, 122))
	if c == 63:
		c = 32
	if c == 64:
		c = 46
	# print(chr(c))
	return chr(c)


class DNA:
	def __init__(self, numb):
		# print("DNA Constructor")
		self.genes = []
		self.fitnss = 0
		# print(num)
		for i in range(numb):
			# print(i)
			self.genes.append(newChar())
			# print(self.genes[i])

	def getPhrase(self):
		return "".join(self.genes)

	def calcFitness(self, target):
		score = 0
		for i in range(len(self.genes)):
			if self.genes[i] == target[i]:
				score += 1
		self.fitness = score / len(target)

	def crossover(self, partner):
		child = DNA(len(self.genes))
		midpoint = math.floor(random.randint(0, len(self.genes)))
		for i in range(len(self.genes)):
			if i > midpoint:
				child.genes[i] = self.genes[i]
			else:
				child.genes[i] = partner.genes[i]

		return child

	def mutate(self, mutationRate):
		for i in range(len(self.genes)):
			if random.uniform(0, 1) < mutationRate:
				self.genes[i] = newChar()


class Population:
	def __init__(self, p, m, num):
		# print("Pop Constuctor")
		self.target = p
		self.mutationRate = m
		self.perfectScore = 1
		self.finished = False
		self.generations = 0
		self.best = ""

		self.population = []
		# print(num)
		for i in range(num):
			# print(i)
			self.population.append(DNA(len(self.target)))
		self.matingPool = []
		self.calcFitness()

	def calcFitness(self):
		for i in range(len(self.population)):
			self.population[i].calcFitness(target)

	def naturalSelection(self):
		self.matingPool = []
		maxFitness = 0
		for i in range(len(self.population)):
			if self.population[i].fitness > maxFitness:
				maxFitness = self.population[i].fitness

		for i in range(len(self.population)):
			fitness = interp(self.population[i].fitness, [0, maxFitness], [0, 1])
			n = math.floor(fitness * 100)
			for j in range(n):
				self.matingPool.append(self.population[i])
				# print(self.matingPool[j])

	def generate(self):
		for i in range(len(self.population)):
			a = math.floor(random.randint(0, len(self.matingPool) - 1))
			b = math.floor(random.randint(0, len(self.matingPool) - 1))
			# print("a is {}".format(a))
			# print("b is {}".format(b))
			# print(len(self.matingPool))
			partnerA = self.matingPool[a]
			partnerB = self.matingPool[b]
			child = partnerA.crossover(partnerB)
			child.mutate(self.mutationRate)
			self.population[i] = child
		self.generations += 1

	def getBest(self):
		return self.best

	def evaluate(self):
		worldrecord = 0.0
		index = 0
		for i in range(len(self.population)):
			if self.population[i].fitness > worldrecord:
				index = i
				worldrecord = self.population[i].fitness
		self.best = self.population[index].getPhrase()
		if worldrecord == self.perfectScore:
			self.finished = True

	def isFinished(self):
		return self.finished

	def getGenerations(self):
		return self.generations

	def getAverageFitness(self):
		total = 0
		for i in range(len(self.population)):
			total += self.population[i].fitness
		return total / len(self.population)

	def allPhrases(self):
		everything = []
		displayLimit = min(len(self.population), 32)
		# displayLimit = len(self.population)
		for i in range(displayLimit):
			everything.append(self.population[i].getPhrase())
		return everything

# ------------------------------------------------------------------------------


def displayInfo():
	best_phrase = large_font.render("Best phrase:", True, body)
	answer = large_font.render(population.getBest(), True, body)
	generation = medium_font.render("total generations: " + str(population.getGenerations()), True, body)
	avgfitness = medium_font.render("average fitness: " + str(population.getAverageFitness()), True, body)
	totalpop = medium_font.render("total population: " + str(popmax), True, body)
	mutation = medium_font.render("mutation rate: " + str(math.floor(mutationRate * 100)) + "%", True, body)
	all_phrases = medium_font.render("All phrases:", True, body)
	phrases = population.allPhrases()
	label = []
	for line in phrases:
		label.append(small_font.render(line, True, body))

	display.blit(best_phrase, (30, 200))
	display.blit(answer, (30, 250))
	display.blit(generation, (30, 320))
	display.blit(avgfitness, (30, 350))
	display.blit(totalpop, (30, 380))
	display.blit(mutation, (30, 410))
	display.blit(all_phrases, (850, 15))
	for line in range(len(label)):
		display.blit(label[line], (850, 50 + (20 * line)))

	pygame.display.update()


def pause():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()


target = "To be or not to be."
popmax = 200
mutationRate = 0.01
population = Population(target, mutationRate, popmax)
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	display.fill(background)
	population.naturalSelection()
	population.generate()
	population.calcFitness()
	population.evaluate()
	displayInfo()
	if population.isFinished() is True:
		pause()
	pygame.display.update()

