import math
import random
from numpy import interp


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
		everything = ""
		# displayLimit = min(len(self.population), 50)
		displayLimit = len(self.population)
		for i in range(displayLimit):
			everything += self.population[i].getPhrase() + "\n"
		return everything


target = "To be or not to be."
popmax = 200
mutationRate = 0.01
population = Population(target, mutationRate, popmax)
while(True):
	population.naturalSelection()
	population.generate()
	population.calcFitness()
	population.evaluate()
	print(population.getBest())
	if population.isFinished() is True:
		print("end")
		break
