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

def main():
	lp = read_file()
	print lp.matrix
	build_tableaux(lp)
	print lp.matrix

if __name__ == "__main__":
	main()