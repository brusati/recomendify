#!/usr/bin/python3

import sys
from grafo import Grafo
import funciones
import heapq

CAMINO_MAS_CORTO = "camino"
CANCIONES_MAS_IMPORTANTES = "mas_importantes"
RECOMENDACION = "recomendacion"
CICLO_N_CANCIONES = "ciclo"
TODAS_EN_RANGO = "rango"
COEFICIENTE_DE_CLUSTERING = "clustering"
USUARIOS = "usuarios"
CANCIONES = "canciones"
ESPACIO = " "
PUNTO_Y_COMA = ";"
TAB = "	"
SEPARADOR = " >>>> "
SEPARADOR_FLECHA = " --> "
NO_HAY_RECORRIDO = "No se encontro recorrido"
FORMATO_INCORRECTO = "Tanto el origen como el destino deben ser canciones"

def camino_mas_corto(l, g_usuarios, set_canciones):
	origen, destino = (ESPACIO.join(l[1::])).rstrip().split(SEPARADOR)

	if origen not in set_canciones or destino not in set_canciones:
		print(FORMATO_INCORRECTO)
		return

	__, padre = funciones.camino_minimo(g_usuarios, origen)
	
	if destino not in padre:
		print(NO_HAY_RECORRIDO)
		return

	actual = destino
	n = -1
	cadena = f"{actual}"

	while padre[actual] != None:
		n += 1
		if n % 2 == 0: #salteamos a los usuarios
			continue
		usuario = padre[actual]
		__, playlist_name_1 = g_usuarios.obtener_peso(usuario, actual)
		__, playlist_name_2 = g_usuarios.obtener_peso(usuario, padre[usuario])

		c = f"{padre[usuario]} --> aparece en playlist --> {playlist_name_2} --> de --> {usuario} --> tiene una playlist --> {playlist_name_1} --> donde aparece --> "
		cadena = c + cadena
		actual = padre[usuario]

	print(cadena)

def canciones_mas_importantes(l, set_canciones, ranks):
	n = int(l[1])

	n_mejores = heapq.nlargest(n, ranks.items(), key=lambda x: x[1]) #nos quedamos con los n mejores

	resultado = []
	for i in range(n):
		resultado.append(n_mejores[i][0])
	print((PUNTO_Y_COMA + ESPACIO).join(resultado))

def recomendacion(l, g_usuarios):
	variable = l[1]
	n = int(l[2])
	canciones = ESPACIO.join(l[3::]).rstrip().split(SEPARADOR)

	recom_canciones, recom_usuarios = funciones.page_rank_personalizado(g_usuarios, canciones)

	n_mejores_canciones = heapq.nlargest(n, recom_canciones.items(), key=lambda x: x[1]) #nos quedamos con las n mejores canciones
	n_mejores_usuarios = heapq.nlargest(n, recom_usuarios.items(), key=lambda x: x[1]) #nos quedamos con los n mejores usuarios
	
	resultado = []
	for i in range(n):
		if variable == CANCIONES:
			resultado.append(n_mejores_canciones[i][0])
		elif variable == USUARIOS:
			resultado.append(n_mejores_usuarios[i][0])
	print((PUNTO_Y_COMA + ESPACIO).join(resultado))

def ciclo_n_canciones(l, g_canciones):
	n = int(l[1])
	cancion = ESPACIO.join(l[2:]).rstrip()

	ciclo = funciones.obtener_ciclo(g_canciones, cancion, n)

	if not ciclo:
		print(NO_HAY_RECORRIDO)
	else:
		print(SEPARADOR_FLECHA.join(ciclo))

def todas_en_rango(l, g_canciones):
	n = int(l[1])
	cancion = ESPACIO.join(l[2:]).rstrip()

	__, orden = funciones.recorrido_bfs(g_canciones, cancion)
	contador = 0
	for i in orden.values():
		if i == n:
			contador += 1

	print(contador)

def coeficiente_de_clustering(l, g_canciones):
	if ESPACIO.join(l).rstrip() == COEFICIENTE_DE_CLUSTERING:
		print(round(funciones.clustering_promedio(g_canciones), 3))
	else:
		cancion = ESPACIO.join(l[1:]).rstrip()
		print(round(funciones.clustering(g_canciones, cancion), 3))

def calcular_page_rank(g_usuarios, set_canciones):
	ranks = funciones.page_rank(g_usuarios)
	ranks_canciones = {}
	for v, i in ranks.items(): #sacamos a los usuarios
		if v in set_canciones:
			ranks_canciones[v] = i
	return ranks_canciones





def main():
	ruta_datos = sys.argv[1]

	g_usuarios = Grafo(False)
	g_canciones = Grafo(False)
	playlists = {}
	set_canciones = set()

	leer_usuarios = False
	leer_canciones = False
	hacer_page_rank = False

	lineas = []

	for linea in sys.stdin:
		l = linea.split(ESPACIO)
		comando = l[0].rstrip()
		lineas.append(linea)

		if comando in (CAMINO_MAS_CORTO, CANCIONES_MAS_IMPORTANTES, RECOMENDACION):
			if comando == CANCIONES_MAS_IMPORTANTES:
				hacer_page_rank = True
			leer_usuarios = True
		elif comando in (CICLO_N_CANCIONES, TODAS_EN_RANGO, COEFICIENTE_DE_CLUSTERING):
			leer_canciones = True

	with open(ruta_datos) as archivo:
		for i, linea in enumerate(archivo):
			if i == 0: #salteamos la primera línea del archivo
				continue
				
			__, user_id, track_name, artist, playlist_id, playlist_name, __ = linea.split(TAB)
			cancion = f"{track_name} - {artist}"

			if leer_usuarios:
				if not g_usuarios.existe_vertice(user_id): 
					g_usuarios.agregar_vertice(user_id)
				if not g_usuarios.existe_vertice(cancion): 
					g_usuarios.agregar_vertice(cancion)

				set_canciones.add(cancion)
				if not g_usuarios.existe_arista(user_id, cancion): 
					g_usuarios.agregar_arista(user_id, cancion, (playlist_id, playlist_name))

			if leer_canciones:
				if not g_canciones.existe_vertice(cancion): 
					g_canciones.agregar_vertice(cancion)

				canciones = playlists.get(playlist_name, set())
				for c in canciones:
					if c != cancion and not g_canciones.existe_arista(c, cancion):
						g_canciones.agregar_arista(c, cancion)
				canciones.add(cancion)
				playlists[playlist_name] = canciones

	ranks = {}
	if hacer_page_rank:
		ranks = calcular_page_rank(g_usuarios, set_canciones)

	for linea in lineas:
		l = linea.split(ESPACIO)
		comando = l[0].rstrip()

		if comando == CAMINO_MAS_CORTO:
			camino_mas_corto(l, g_usuarios, set_canciones)

		elif comando == CANCIONES_MAS_IMPORTANTES:
			canciones_mas_importantes(l, set_canciones, ranks)

		elif comando == RECOMENDACION:
			recomendacion(l, g_usuarios)

		elif comando == CICLO_N_CANCIONES:
			ciclo_n_canciones(l, g_canciones)

		elif comando == TODAS_EN_RANGO:
			todas_en_rango(l, g_canciones)

		elif comando == COEFICIENTE_DE_CLUSTERING:
			coeficiente_de_clustering(l, g_canciones)





main()