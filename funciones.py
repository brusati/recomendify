from collections import deque
import heapq

D = 0.85
ITERACIONES_PR = 100

PROFUNDIDAD_RW = 10 #haciendo pruebas, este coeficiente nos devolvió canciones más parecidas a nuestros gustos
CANTIDAD_RW = 1000


def camino_minimo(grafo, origen):
	"""obtiene los caminos mínimos partiendo desde un origen a todos los nodos del grafo usando bfs"""
	visitados = set()
	distancia = {}
	padre = {}
	for v in grafo.vertices():
		distancia[v] = float("inf")
	distancia[origen] = 0
	padre[origen] = None
	visitados.add(origen)
	cola = deque()
	cola.append(origen)
	while len(cola) != 0:
		v = cola.popleft()
		for w in grafo.adyacentes(v):
			if w not in visitados:
				distancia[w] = distancia[v] + 1
				padre[w] = v
				visitados.add(w)
				cola.append(w)
	return distancia, padre

def page_rank(grafo):
	ranks = {}
	for v in grafo.vertices():
		ranks[v] = 1
	cte = (1 - D) / len(grafo.vertices())
	for __ in range(ITERACIONES_PR):
		for v in grafo.vertices():
			n = 0
			for w in grafo.adyacentes(v):
				n += ranks[w] / len(grafo.adyacentes(w))
			ranks[v] = cte + (D * n)
	return ranks

def random_walk(grafo, v):
	recorrido = []
	actual = v
	for i in range(0, PROFUNDIDAD_RW):
		recorrido.append(actual)
		actual = grafo.adyacente_aleatorio(actual)
	return recorrido

def page_rank_personalizado(grafo, nodos):
	d_1 = {}
	d_2 = {}
	for i, v in enumerate(nodos):
		for __ in range(0, CANTIDAD_RW):
			recorrido = random_walk(grafo, nodos[i])
			for j in range(2, len(recorrido), 2):
				if recorrido[j] not in nodos:
					suma = d_1.get(recorrido[j], 0) + 1
					d_1[recorrido[j]] = suma
			for j in range(1, len(recorrido), 2):
				if recorrido[j] not in nodos:
					suma = d_2.get(recorrido[j], 0) + 1
					d_2[recorrido[j]] = suma
	return d_1, d_2

def reconstruir_camino(padre, inicio, fin):
	camino = []
	v = fin
	camino.append(inicio)
	while v != inicio:
		camino.append(v)
		v = padre[v]
	camino.append(inicio)
	return camino[::-1]

def _obtener_ciclo(grafo, visitados, v, padre, orden, actual, n):
	if orden[actual] >= n:
		return None
	for w in grafo.adyacentes(actual):
		if w not in visitados:
			padre[w] = actual
			orden[w] = orden[actual] + 1
			visitados.add(w)
			ciclo = _obtener_ciclo(grafo, visitados, v, padre, orden, w, n)
			if ciclo:
				return ciclo
			visitados.remove(w)
			orden.pop(w)
			padre.pop(w)
		elif w != padre[actual] and orden[actual] == n - 1 and w == v:
			return reconstruir_camino(padre, v, actual)
	return None

def obtener_ciclo(grafo, v, n):
	"""devuelve un ciclo de largo n partiendo desde el nodo v"""
	visitados = set()
	padre = {}
	orden = {}
	visitados.add(v)
	padre[v] = None
	orden[v] = 0
	ciclo = _obtener_ciclo(grafo, visitados, v, padre, orden, v, n)
	if ciclo:
		return ciclo
	return None

def recorrido_bfs(grafo, v):
	"""realiza un recorrido bfs por todo el grafo partiendo del nodo v"""
	"""devuelve un diccionario de padres y orden de los nodos visitados"""
	visitados = set()
	padre = {}
	orden = {}
	visitados.add(v)
	padre[v] = None
	orden[v] = 0
	cola = deque()
	cola.append(v)
	while len(cola) != 0:
		v = cola.popleft()
		for w in grafo.adyacentes(v):
			if w not in visitados:
				padre[w] = v
				orden[w] = orden[v] + 1
				visitados.add(w)
				cola.append(w)
	return padre, orden

def clustering(grafo, v):
	"""devuelve el coeficiente de clustering de un nodo v"""
	n = len(grafo.adyacentes(v))
	if n < 2:
		return 0
	contador = 0
	for w in grafo.adyacentes(v):
		for x in grafo.adyacentes(w):
			if x in grafo.adyacentes(v):
				contador += 1
	return contador / (n * (n - 1))

def clustering_promedio(grafo):
	"""devuelve el coeficiente de clustering promedio de todo el grafo"""
	n = len(grafo.vertices())
	suma = 0
	for v in grafo.vertices():
		suma += clustering(grafo, v)
	return suma / n