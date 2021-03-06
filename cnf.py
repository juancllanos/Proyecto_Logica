#-*-coding: utf-8-*-

import DPLL as D
import csv

class Tree(object):
	def __init__(self, r, iz, der):
		self.left = iz
		self.right = der
		self.label = r

def Inorder(f):
    # Imprime una formula como cadena dada una formula como arbol
    # Input: tree, que es una formula de logica proposicional
    # Output: string de la formula

    if f.right == None:
        return f.label
    elif f.label == '-':
        return f.label + Inorder(f.right)
    else:
        return "(" + Inorder(f.left) + f.label + Inorder(f.right) + ")"

def StringtoTree(A, letrasProposicionales):
    # Crea una formula como tree dada una formula como cadena escrita en notacion polaca inversa
    # Input: A, lista de caracteres con una formula escrita en notacion polaca inversa
             # letrasProposicionales, lista de letras proposicionales
    # Output: formula como tree
    conectivos = ['O', 'Y', '>']
    pila = []
    for c in A:
        if c in letrasProposicionales:
            pila.append(Tree(c, None, None))
        elif c == '-':
            aux = Tree(c, None, pila[-1])
            del pila[-1]
            pila.append(aux)
        elif c in conectivos:
            aux = Tree(c, pila[-1], pila[-2])
            del pila[-1]
            del pila[-1]
            pila.append(aux)
    return pila[-1]

def quitarDobleNegacion(f):
	# Elimina las dobles negaciones en una formula como arbol
	# Input: tree, que es una formula de logica proposicional
	# Output: tree sin dobles negaciones

	if f.right == None:
		return f
	elif f.label == '-':
		if f.right.label == '-':
			return quitarDobleNegacion(f.right.right)
		else:
			return Tree('-', \
						None, \
						quitarDobleNegacion(f.right)\
						)
	else:
		return Tree(f.label, \
					quitarDobleNegacion(f.left), \
					quitarDobleNegacion(f.right)\
					)

def reemplazarImplicacion(f):
    # Regresa la formula reemplazando p>q por -pOq
    # Input: tree, que es una formula de logica proposicional
    # Output: tree

    if f.right == None:
        return f
    elif f.label == '-':
        return Tree('-', None, reemplazarImplicacion(f.right))
    elif f.label == '>':
        noP = Tree('-', None, reemplazarImplicacion(f.left))
        Q = reemplazarImplicacion(f.right)
        return Tree('O', noP, Q)
    else:
        return Tree(f.label, reemplazarImplicacion(f.left), reemplazarImplicacion(f.right))

def deMorgan(f):
    # Regresa la formula aplicando deMorgan -(pYq) por -pO-q
    # Input: tree, que es una formula de logica proposicional
    # Output: tree

	if f.right == None:
		return f
	elif f.label == '-':
		if f.right.label == 'Y':
			print "La fórmula coincide negación Y"
			return Tree('O', \
						Tree('-', None, deMorgan(f.right.left)),\
						Tree('-', None, deMorgan(f.right.right))\
						)
		elif f.right.label == 'O':
			print "La fórmula coincide negación O"
			return Tree('Y', \
						Tree('-', None, deMorgan(f.right.left)),\
						Tree('-', None, deMorgan(f.right.right))\
						)
		else:
			return Tree('-', \
						None, \
						deMorgan(f.right) \
						)
	else:
		return Tree(f.label, \
					deMorgan(f.left),\
					deMorgan(f.right)\
					)

def distributiva(f):
    # Distribuye O sobre Ys: convierte rO(pYq) en (rOp)Y(rOq)
    # Input: tree, que es una formula de logica proposicional
    # Output: tree

	if f.right == None:
		# print("Llegamos a una rama")
		return f
	elif f.label == 'O':
		# print("Encontramos O...")
		if f.left.label == 'Y':
			# print("... encontramos Y a la izquierda")
			P = f.left.left
			Q = f.left.right
			R = f.right
			return Tree('Y', \
						Tree('O', P, R), \
						Tree('O', Q, R)
						)
		if f.right.label == 'Y':
			# print("... encontramos Y a la derecha")
			R = f.left
			P = f.right.left
			Q = f.right.right
			return Tree('Y', \
						Tree('O', R, P), \
						Tree('O', R, Q)
						)
		else:
			# print("... pero no hay Y")
			# print("Pasamos a hijos de O")
			return Tree(f.label, \
						distributiva(f.left), \
						distributiva(f.right)
						)
	elif f.label == '-':
		# print("Pasamos a hijo de negacion")
		return Tree('-', \
					None, \
					distributiva(f.right)
					)
	else:
		# print("Pasamos a hijos de ", f.label)
		return Tree(f.label, \
					distributiva(f.left), \
					distributiva(f.right)
					)

def aplicaDistributiva(f):
    # Devuelve True si la distributiva de f es distinta a f
    # Input: tree, que es una formula de logica proposicional
    # Output: - True/False,
	# 		  - tree
	aux1 = Inorder(f)
	print "Se analiza: ", aux1
	B = distributiva(f)
	aux2 = Inorder(B)
	print "Se obtuvo : ", aux2
	if  aux1 != aux2:
		print "Hubo distribución"
		return True, B
	else:
		print "No hubo distribución"
		return False, f

def eliminaConjunciones(f):
    # Devuelve una lista de disyunciones de literales
    # Input: tree, que es una formula en CNF
    # Output: lista de cadenas
	if f.right == None:
		a = [Inorder(f)]
		print "Clausula unitaria positiva, ", a
		return a
	elif f.label == 'O':
		return [Inorder(f)]
	elif f.label == 'Y':
		print "Dividiendo los lados de la conjunción"
		a = eliminaConjunciones(f.left)
		print("a, ", a)
		b = eliminaConjunciones(f.right)
		print("b, ", b)
		c = a + b
		l = a+b

		print("c, ", c)

		archivo = 'alfil_sol_c.csv'
		with open(archivo, 'w') as output:
    			writer = csv.writer(output, lineterminator=',')

    			writer.writerows(l)



		return a + b
	else:
		if f.label == '-':
			if f.right.right == None:
				print "Clausula unitaria negativa"
				return [Inorder(f)]
			else:
				print "Oh, Oh, la formula no estaba en CNF!"

def complemento(l):
    # Devuelve el complemento de un literal
    # Input: l, que es una cadena con un literal (ej: p, -p)
    # Output: l complemento
	if '-' in l:
		return l[1:]
	else:
		return '-' + l

def formaClausal(f):
    # Obtiene la forma clausal de una formula en CNF
    # Input: tree, que es una formula de logica proposicional en CNF
    # Output: lista de clausulas

	# Primero elimino las conjunciones, obteniendo
	# una lista de disyunciones de literales
	print "Encontrando lista de disyunciones de literales..."
	aux = eliminaConjunciones(f)
	badChars = ['(', ')']
	conjuntoClausulas = []
	for C in aux:
		C = ''.join([x for x in C if x not in badChars])
		C = C.split('O')
		conjuntoClausulas.append(C)

	aux = []
	print "Eliminando cláusulas triviales..."
	for C in conjuntoClausulas:
		trivial = False
		for x in C:
			xComplemento = complemento(x)
			if xComplemento in C:
				print "Cláusula trivial encontrada"
				trivial = True
				break
		if not trivial:
			aux.append(C)

	print "Eliminando repeticiones..."
	# Eliminamos repeticiones dentro de cada clausula
	aux = [list(set(i)) for i in aux]
	# Eliminamos clausulas repetidas
	aux_set = set(tuple(x) for x in aux)
	aux = [list(x) for x in aux_set]

	conjuntoClausulas = aux

	return conjuntoClausulas

################################################
"""
letrasProposicionales = ['1', '2', '3','4','5','6','7','8','9']

# cadena = 'q--p->--'
# cadena = 'qpY-'
# cadena = 'rq-pO->'
# cadena = 'qpYprYO'
# cadena = 'qpYpr>O'
# cadena = 'pr>qpYO'
# cadena = 'q--qpYprYO->--'
cadena = '1234-5-6-7-8-9-YYYYYYYY'
# cadena = 'r-q-YpY'
# cadena = cadena + 'r-qYp-Y' + 'O'
#cadena = cadena + 'rq-Yp-Y' + 'O'
#cadena = 'qp>-qpYq-p-YOO-'

A = StringtoTree(cadena, letrasProposicionales)

print(u"Trabajando con la fórmula:\n ", Inorder(A))

A = quitarDobleNegacion(A)

print(u"La fórmula sin dobles negaciones es:\n ")
print(Inorder(A))

A = reemplazarImplicacion(A)

print(u"La fórmula reemplazando implicaciones es:\n ")
print(Inorder(A))

A = quitarDobleNegacion(A)

print(u"La fórmula sin dobles negaciones es:\n ")
print(Inorder(A))

OK = True
while OK:
	aux1 = Inorder(A)
	print("Se analiza: ", aux1)
	B = deMorgan(A)
	B = quitarDobleNegacion(B)
	aux2 = Inorder(B)
	print("Se obtuvo : ", aux2)
	if  aux1 != aux2:
		print(u"Se aplicó deMorgan")
		OK = True
		A = B
	else:
		print(u"No se aplicó deMorgan")
		OK = False

OK = True
while OK:
	OK, A = aplicaDistributiva(A)

conjuntoClausulas = formaClausal(A)

print("Conjunto de disyunciones de literales: ")
print(conjuntoClausulas)

I={}

L = D.DPLL(conjuntoClausulas,I)


print L"""

archivo = 'alfil_sol_c.csv'
print "Interpretaciones guardadas  en " + archivo
