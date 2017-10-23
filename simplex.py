# -*- coding: utf-8 -*-
import numpy as np

class lpInput:
	lines = 0
	columns = 0
	matrix = []

def read_file():
	with open("pl.txt") as f:
		content = f.readlines()
	lp = lpInput()
	lp.lines = int(content[0])+1
	lp.columns = int(content[1])+1
	lp.matrix = np.array([[1, 2, 3, 0], [1, 1, 1, 2], [0, -1, 3, 9]])
	lp.matrix = lp.matrix.astype(float)
	return lp

# Transforma a matriz da entrada no tableaux inicial
def build_tableaux(lpInput):
	# 1 - Coloca a PL em FPI
	#Exapande a matriz com zeros
	for i in range(0, lpInput.lines-1):
		lpInput.matrix = np.insert(lpInput.matrix,lpInput.columns-1,0,axis=1)
	
	#Adiciona 1's na diagonal da identidade
	id_index_i = 1
	id_index_j = lpInput.columns-1
	while id_index_j < lpInput.columns-1 + lpInput.lines-1:
		lpInput.matrix[id_index_i][id_index_j] = 1
		id_index_i += 1
		id_index_j += 1

	#2 - Multiplica o vetor c por -1
	for i in range(0, lpInput.columns-1):
		lpInput.matrix[0][i] = lpInput.matrix[0][i]*(-1)

	#Atualiza o tamanho de linhas e colunas no objeto
	lpInput.lines = lpInput.matrix.shape[0]
	lpInput.columns = lpInput.matrix.shape[1]

def primal_pivoting(pl):
	print pl.matrix
	print "primal_pivoting:"
	while True: #Executar até não haver mais entrada negativa no c
		# Escolher coluna:
		column_index = None
		for i in range(0, pl.columns-1):
			if pl.matrix[0][i] < 0:
				column_index = i
				break
			else:
				return 0
		# Calcula a razão entre os elementos de 'b' e 'a' e escolhe o menor:
		min_ratio = None
		pivot_index = ()
		pivot_value = 0
		for i in range(1, pl.lines):
			if not (pl.matrix[i][column_index] <= 0): # A deve ser positivo
				ratio = pl.matrix[i][pl.lines-1]/pl.matrix[i][column_index]
				#print "{}/{}".format(pl.matrix[i][pl.columns-1],pl.matrix[i][column_index])
				if ratio < min_ratio or min_ratio == None:
					min_ratio = ratio
					pivot_index = (i, column_index)
					pivot_value = pl.matrix[i][column_index]
		# Transformar o pivot em 1 (e sua linha correspondente)
		if pivot_index != 1:
			for i in range(0, pl.columns):
				#print "{}/{}".format(pl.matrix[pivot_index[0]][i], pivot_value)
				pl.matrix[pivot_index[0]][i] = float(pl.matrix[pivot_index[0]][i]/pivot_value)
		# Zerar elementos
		for i in range(0, pl.lines):
			if i != pivot_index[0]:
				coefficient = pl.matrix[i][pivot_index[1]]*-1 # Acha o valor que devemos multiplicar a linha do pivot para somar na linha que se deseja zerar
				for j in range(0, pl.columns):
					pl.matrix[i][j] = pl.matrix[i][j] + pl.matrix[pivot_index[0]][j]*coefficient
		print pl.matrix


def main():
	lp = read_file()
	#print lp.matrix
	build_tableaux(lp)
	bool_dual = False
	for i in range(1, lp.lines):
		if i < 0: # Entrada negativa no vetor B -> PL Dual
			bool_dual = True
	if bool_dual:
		#dual_pivoting(lp)
		print "DUAL"
	else:
		primal_pivoting(lp)

if __name__ == "__main__":
	main()