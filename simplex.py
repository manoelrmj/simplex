# -*- coding: utf-8 -*-
import numpy as np
import sys

class lpInput:
	lines = 0
	columns = 0
	matrix = []
	operations_matrix = []

def read_file():
	with open(sys.argv[1]) as f:
		content = f.readlines()
	lp = lpInput()
	lp.lines = int(content[0])+1
	lp.columns = int(content[1])+1
	lp.matrix = np.array(eval(content[2]))
	lp.matrix = lp.matrix.astype(float)
	return lp

def get_solution(lp):
	bases_columns = []
	index_bases = []
	solution_array = []
	for i in range(0, lp.columns-1):
		#verifica coluna
		is_base = True
		for j in range(1, lp.lines):
			if (lp.matrix[j][i] != 0 and lp.matrix[j][i] != 1):
				is_base = False
		if is_base == True: 
			bases_columns.append(i)
	for i in range(0, lp.columns-1):
		if(i in bases_columns):
			for j in range(1, lp.lines):
				if lp.matrix[j][i] == 1:
					solution_array.append(lp.matrix[j][lp.columns-1])
		else:
			solution_array.append(0)
	lp_solution = []

	for i in range(0, lp.columns-lp.lines):
		lp_solution.append(solution_array[i])

	lp_solution = np.around(lp_solution, decimals=5)
	#print lp_solution
	return lp_solution

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

	#Inicializa matriz de operações
	lpInput.operations_matrix = np.zeros((lpInput.lines, lpInput.lines-1))
	id_index_i = 1
	id_index_j = 0
	while id_index_j < lpInput.lines-1:
		lpInput.operations_matrix[id_index_i][id_index_j] = 1
		id_index_i += 1
		id_index_j += 1	
	#print lpInput.operations_matrix

def primal_pivoting(pl, output=True):
	print "Primal"
	#pl.operations_matrix = np.around(pl.operations_matrix, decimals=5)
	#pl.matrix = np.around(pl.matrix, decimals=5)
	tableaux = np.concatenate((pl.operations_matrix, pl.matrix), axis=1)
	print tableaux
	#print pl.operations_matrix
	#print pl.matrix
	while True: #Executar até não haver mais entrada negativa no c
		# Escolher coluna:
		column_index = None
		for i in range(0, pl.columns-1):
			if pl.matrix[0][i] < 0:
				column_index = i
				break
		if column_index == None: # Não existem mais elementos negativos no c
			certificate = []
			for i in range(0, pl.lines-1):
				certificate.append(pl.operations_matrix[0][i])
			if output == True:
				print "Solução ótima x = {}, com valor objetivo {} e certificado y={}".format(get_solution(pl), pl.matrix[0][pl.columns-1], certificate)
			return pl
		else: # Verifica os valores de A na coluna correspondente para checar se é ilimitada
			positive_a = False
			for i in range(1, pl.lines):
				if pl.matrix[i][column_index] > 0:
					positive_a = True
			if positive_a == False:
				#PL ilimitada
				#Calcular os valores do certificado
				d_certificate = []
				for i in range(0, pl.columns-1):
					if i == column_index:
						d_certificate.append(1)
					else:
						#Checar se a coluna faz parte da base
						is_base = True
						for j in range(1, pl.lines):
							if pl.matrix[j][i] != 0 and pl.matrix[j][i] != 1:
								is_base = False
						if is_base == True:
							for j in range(1, pl.lines):
								if pl.matrix[j][i] == 1:
									d_certificate.append(pl.matrix[j][column_index]*(-1))
									break
						else:
							d_certificate.append(0)
				if output == True:
					print "PL ilimitada, aqui esta um certificado {}".format(d_certificate)
				return pl
		#print "Coluna: {}".format(column_index)
		# Calcula a razão entre os elementos de 'b' e 'a' e escolhe o menor:
		min_ratio = None
		pivot_index = ()
		pivot_value = 0
		for i in range(1, pl.lines):
			if not (pl.matrix[i][column_index] <= 0): # A deve ser positivo
				ratio = pl.matrix[i][pl.columns-1]/pl.matrix[i][column_index]
				#print "{}/{} = {}".format(pl.matrix[i][pl.columns-1],pl.matrix[i][column_index],ratio)
				if ratio < min_ratio or min_ratio == None:
					min_ratio = ratio
					pivot_index = (i, column_index)
					pivot_value = pl.matrix[i][column_index]
		# Transformar o pivot em 1 (e sua linha correspondente)
		#if pivot_index != 1:
		#print "{}:{}".format(pivot_index, pivot_value)
		if pivot_value != 1: ##check this##
			for i in range(0, pl.columns):
				#print "{}/{}".format(pl.matrix[pivot_index[0]][i], pivot_value)
				pl.matrix[pivot_index[0]][i] = float(pl.matrix[pivot_index[0]][i]/pivot_value)
			#Atualiza matriz de operações
			for i in range(0, pl.operations_matrix.shape[1]):
				pl.operations_matrix[pivot_index[0]][i] = float(pl.operations_matrix[pivot_index[0]][i]/pivot_value)
		# Zerar elementos
		for i in range(0, pl.lines):
			if i != pivot_index[0]:
				coefficient = pl.matrix[i][pivot_index[1]]*-1 # Acha o valor que devemos multiplicar a linha do pivot para somar na linha que se deseja zerar
				for j in range(0, pl.columns):
					pl.matrix[i][j] = pl.matrix[i][j] + pl.matrix[pivot_index[0]][j]*coefficient
				# Atualiza matrix de operações
				for k in range(0, pl.operations_matrix.shape[1]):
					pl.operations_matrix[i][k] = pl.operations_matrix[i][k] + pl.operations_matrix[pivot_index[0]][k]*coefficient
		#print pl.operations_matrix
		#print pl.matrix
		#pl.operations_matrix = np.around(pl.operations_matrix, decimals=5)
		#pl.matrix = np.around(pl.matrix, decimals=5)
		tableaux = np.concatenate((pl.operations_matrix, pl.matrix), axis=1)
		print tableaux
		#tableaux = np.around(tableaux, decimals=5)
	return pl

def dual_pivoting(pl):
	print "Dual"
	#pl.operations_matrix = np.around(pl.operations_matrix, decimals=5)
	#pl.matrix = np.around(pl.matrix, decimals=5)
	tableaux = np.concatenate((pl.operations_matrix, pl.matrix), axis=1)
	print tableaux
	while True: #Executar até não haver mais entrada negativa no b
		#Escolher linha
		line_index = None
		for i in range(1, pl.lines):
			#print "[{}][{}]".format(i, pl.columns-1)
			if pl.matrix[i][pl.columns-1] < 0:
					line_index = i
					break
		if line_index == None: # Não existem mais elementos negativos no c
			certificate = []
			for i in range(0, pl.lines-1):
				certificate.append(pl.operations_matrix[0][i])
			#certificate = np.around(certificate, decimals=5)
			print "Solução ótima x = {}, com valor objetivo {} e certificado y={}".format(get_solution(pl), pl.matrix[0][pl.columns-1], certificate)
			return
		else: # Verifica se existem valores negativos em A
			negative_a = False
			for i in range(0, pl.columns-1):
				if pl.matrix[line_index][i] < 0:
					negative_a = True
					break
			if negative_a == False:
				print "PL inviável:"
				#print pl.operations_matrix
				#print pl.matrix
				#print pl.lines
				#print pl.columns
				auxiliar_lp(pl)
				return
		# Calcula a razão entre os elementos de 'b' e '-a' e escolhe o menor:
		min_ratio = None
		pivot_index = ()
		pivot_value = 0
		for i in range(0, pl.columns-1):
			if not (pl.matrix[line_index][i] >= 0): # A deve ser negativo
				ratio = pl.matrix[line_index][pl.columns-1]/(pl.matrix[line_index][i]*-1)
				#print "{}/{}".format(pl.matrix[line_index][pl.columns-1],pl.matrix[line_index][i])
				if ratio < min_ratio or min_ratio == None:
					min_ratio = ratio
					pivot_index = (line_index, i)
					pivot_value = pl.matrix[line_index][i]
		#print pivot_value
		#print "[{}][{}]".format(pivot_index[0], pivot_index[1])
		# Transformar o pivot em 1 (e sua linha correspondente)
		if pivot_value != 1:
			for i in range(0, pl.columns):
				#print "{}/{}".format(pl.matrix[pivot_index[0]][i], pivot_value)
				pl.matrix[pivot_index[0]][i] = float(pl.matrix[pivot_index[0]][i]/pivot_value)
			#Atualiza matriz de operações
			for i in range(0, pl.operations_matrix.shape[1]):
				pl.operations_matrix[pivot_index[0]][i] = float(pl.operations_matrix[pivot_index[0]][i]/pivot_value)
		# Zerar elementos
		for i in range(0, pl.lines):
			if i != pivot_index[0]:
				coefficient = pl.matrix[i][pivot_index[1]]*-1 # Acha o valor que devemos multiplicar a linha do pivot para somar na linha que se deseja zerar
				for j in range(0, pl.columns):
					pl.matrix[i][j] = pl.matrix[i][j] + pl.matrix[pivot_index[0]][j]*coefficient
				# Atualiza matrix de operações
				for k in range(0, pl.operations_matrix.shape[1]):
					pl.operations_matrix[i][k] = pl.operations_matrix[i][k] + pl.operations_matrix[pivot_index[0]][k]*coefficient
		#print pl.operations_matrix
		#print pl.matrix
		#pl.operations_matrix = np.around(pl.operations_matrix, decimals=5)
		#pl.matrix = np.around(pl.matrix, decimals=5)
		tableaux = np.concatenate((pl.operations_matrix, pl.matrix), axis=1)
		print tableaux

def auxiliar_lp(lp):
	print "Auxiliar"
	#Salva o vetor c original
	original_c = []
	for i in range(0, lp.columns-1):
		original_c.append(lp.matrix[0][i])
	#print "original_c: {}".format(original_c)

	#Zera entradas do vetor c
	for i in range(0, lp.columns-1):
		lp.matrix[0][i] = 0

	# Gera colunas da pl auxiliar
	#Exapande a matriz com zeros e adiciona 1's na diagonal principal e no c
	main_diagonal_indexes = []
	for i in range(0, lp.lines-1):
		lp.matrix = np.insert(lp.matrix,lp.columns-1,0,axis=1)
		main_diagonal_indexes.append((i+1,lp.columns-1))
		lp.columns += 1		
	for index in main_diagonal_indexes:
		lp.matrix[index[0]][index[1]] = 1
		lp.matrix[0][index[1]] = 1

	#print lp.operations_matrix
	#print lp.matrix
	#lp.operations_matrix = np.around(lp.operations_matrix, decimals=5)
	#lp.matrix = np.around(lp.matrix, decimals=5)
	tableaux = np.concatenate((lp.operations_matrix, lp.matrix), axis=1)
	print tableaux
	
	for i in range(1, lp.lines):
		for j in range(0, lp.columns):
			lp.matrix[0][j] += lp.matrix[i][j]*(-1)
		for j in range(0, lp.operations_matrix.shape[1]):
			lp.operations_matrix[0][j] += lp.operations_matrix[i][j]*(-1)

	tableaux = np.concatenate((lp.operations_matrix, lp.matrix), axis=1)
	print tableaux
	
	#Cria um novo objeto lpInput com o novo tableau para enviar ao simplex
	#print "\n"
	new_lp = lpInput()
	new_lp.lines = lp.lines
	new_lp.columns = lp.columns
	new_lp.matrix = lp.matrix.copy()
	new_lp.operations_matrix = lp.operations_matrix.copy()
	#print new_lp.operations_matrix
	#print new_lp.matrix
	new_lp = primal_pivoting(new_lp, False)
	#print new_lp.operations_matrix
	#print new_lp.matrix
	if new_lp.matrix[0][new_lp.columns-1] == 0:
		# Solução viável, refazer simplex
		# 1) Remover colunas da pl auxiliar
		print "Viável"
		#print "Colunas removidas: "
		for i in range(new_lp.columns-2, new_lp.columns-new_lp.lines-1, -1):
			#print i
			new_lp.matrix = np.delete(new_lp.matrix, i, 1)
			new_lp.columns -= 1
		#print new_lp.operations_matrix
		#print new_lp.matrix
		#print "C recolocado: "
		# 2) Recolocar o c original
		for i in range(0, len(original_c)):
			new_lp.matrix[0][i] = original_c[i]
		
		# Zera o c nas colunas base
		for i in range(0, new_lp.columns):
			#Verifica se a coluna é base
			is_base = True
			index = 0
			for j in range(1, new_lp.lines):
				if new_lp.matrix[j][i] != 0 and new_lp.matrix[j][i] != 1:
					is_base = False
				elif new_lp.matrix[j][i] == 1:
					index = j
			if is_base == True:
				#print "{},{}".format(i,index)
				for k in range(0, new_lp.columns):
					new_lp.matrix[0][k] += new_lp.matrix[index][k]*(-1)
				for k in range(0, new_lp.operations_matrix.shape[1]):	
					new_lp.operations_matrix[0][k] += new_lp.operations_matrix[index][k]*(-1)
		
		#print new_lp.operations_matrix
		#print new_lp.matrix
		#new_lp.operations_matrix = np.around(new_lp.operations_matrix, decimals=5)
		#new_lp.matrix = np.around(new_lp.matrix, decimals=5)
		tableaux = np.concatenate((new_lp.operations_matrix, new_lp.matrix), axis=1)
		print tableaux
		new_lp = primal_pivoting(new_lp)

	elif new_lp.matrix[0][new_lp.columns-1] < 0:
		inviability_certificate = []
		for i in range(0, new_lp.operations_matrix.shape[1]):
			inviability_certificate.append(new_lp.operations_matrix[0][i])
		inviability_certificate = np.around(inviability_certificate, decimals=5)
		print "PL inviável, aqui esta um certificado: {}".format(inviability_certificate)
	
def main():
	lp = read_file()
	print lp.matrix
	build_tableaux(lp)
	tableaux = np.concatenate((lp.operations_matrix, lp.matrix), axis=1)
	print tableaux
	bool_auxiliar = True
	bool_dual = False

	for i in range(1, lp.lines):
		if lp.matrix[i][lp.columns-1] < 0: # Entrada negativa no vetor B
			bool_auxiliar = False
	for i in range(0, lp.columns-1):
		if lp.matrix[0][i] < 0: # Entrada negativa no vetor c
			bool_auxiliar = False

	if bool_auxiliar == False:
		for i in range(1, lp.lines):
			if lp.matrix[i][lp.columns-1] < 0: # Entrada negativa no vetor B -> PL Dual
				bool_dual = True

		if bool_dual:
			dual_pivoting(lp)
		else:
			primal_pivoting(lp)
	else:
		auxiliar_lp(lp)

if __name__ == "__main__":
	main()