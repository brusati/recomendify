from random import randrange

class Grafo:
	def __init__(self, dirigido=True):
		self.grafo = {}
		self.peso = {}
		self.dirigido = dirigido

	def vertices(self):
		return self.grafo.keys()

	def adyacentes(self, v):
		if v not in self.grafo:
			raise Exception(f"El vértice {v} no existe en el grafo")
		return self.grafo[v]

	def agregar_vertice(self, v):
		if v in self.grafo:
			raise Exception(f"El vértice {v} ya existe en el grafo")
		self.grafo[v] = set()

	def agregar_arista(self, a, b, p=0):
		if a not in self.grafo:
			raise Exception(f"El vértice {a} no existe en el grafo")
		if b not in self.grafo:
			raise Exception(f"El vértice {b} no existe en el grafo")
		if b in self.grafo[a]:
			raise Exception(f"Ya existe la arista {a}-{b}")

		if not self.dirigido:
			self.grafo[b].add(a)
			self.peso[(b, a)] = p
		self.grafo[a].add(b)
		self.peso[(a, b)] = p

	def obtener_peso(self, a, b):
		if a not in self.grafo:
			raise Exception(f"El vértice {a} no existe en el grafo")
		if b not in self.grafo:
			raise Exception(f"El vértice {b} no existe en el grafo")
		if b not in self.grafo[a]:
			raise Exception(f"No existe la arista {a}-{b}")

		return self.peso[(a, b)]

	def adyacente_aleatorio(self, v):
		if v not in self.grafo:
			raise Exception(f"El vértice {v} no existe en el grafo")

		adyacentes = self.grafo[v]
		if len(adyacentes) == 0:
			raise Exception(f"El vértice {v} no tiene adyacentes")

		return list(adyacentes)[randrange(len(adyacentes))]

	def vertice_aleatorio(self):
		vertices = self.grafo.keys()
		if len(vertices) == 0:
			raise Exception(f"No hay vértices en el grafo")

		return list(vertices)[randrange(len(vertices))]

	def existe_arista(self, a, b):
		if a not in self.grafo:
			raise Exception(f"El vértice {a} no existe en el grafo")
		if b not in self.grafo:
			raise Exception(f"El vértice {b} no existe en el grafo")

		return b in self.grafo[a]

	def existe_vertice(self, v):
		return v in self.grafo