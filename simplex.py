# -*- coding: utf-8 -*-
import numpy as np
from fractions import Fraction
import sys

class Tableaux:
	lines = 0
	columns = 0
	matrix = []	
	operations_matrix = []

	def __init__(self, lines, columns, matrix):
		
		self.lines = lines
		self.columns = columns
		self.matrix = matrix

		# 1 - Coloca a PL em FPI
		#Exapande a matriz com zeros
		for i in range(0, self.lines-1):
			self.matrix = np.insert(self.matrix,self.columns-1,0,axis=1)
		
		#Adiciona 1's na diagonal da identidade
		id_index_i = 1
		id_index_j = self.columns-1
		while id_index_j < self.columns-1 + self.lines-1:
			self.matrix[id_index_i][id_index_j] = 1
			id_index_i += 1
			id_index_j += 1

		#2 - Multiplica o vetor c por -1
		for i in range(0, self.columns-1):
			self.matrix[0][i] = self.matrix[0][i]*(-1)

		#Atualiza o tamanho de linhas e colunas no objeto
		self.lines = self.matrix.shape[0]
		self.columns = self.matrix.shape[1]


		# Transforma matriz em Fraction
		#tableaux.matrix = np.array(eval(content[2]), dtype="object")
		for i in range(0, self.lines):
			for j in range(0, self.columns):
				self.matrix[i][j] = Fraction(self.matrix[i][j], 1)


		#Inicializa matriz de operações
		self.operations_matrix = np.zeros((self.lines, self.lines-1), dtype="object")
		id_index_i = 1
		id_index_j = 0
		while id_index_j < self.lines-1:
			self.operations_matrix[id_index_i][id_index_j] = 1
			id_index_i += 1
			id_index_j += 1	
		# Transforma matriz de operações em fractions
		for i in range(0, self.operations_matrix.shape[0]):
			for j in range(0, self.operations_matrix.shape[1]):
				self.operations_matrix[i][j] = Fraction(self.operations_matrix[i][j], 1)
		#print self.operations_matrix
		#print self.matrix

	def _print(self):
		tableaux = np.concatenate((self.operations_matrix, self.matrix), axis=1)
		for i in range(0, tableaux.shape[0]):
			for j in range(0, tableaux.shape[1]):
				sys.stdout.write("%4s" % np.format_float_positional(float(tableaux[i,j]), precision=5))
				if(j != (tableaux.shape[1]-1)):
					sys.stdout.write(', ')
			if(i != (tableaux.shape[0]-1)):
				print("\n") 
		print("\n") 
		sys.stdout.flush()

def write_sol_output(pl):
	# Cast to float
	for i in range(0, pl.operations_matrix.shape[0]):
		for j in range(0, pl.operations_matrix.shape[1]):
			pl.operations_matrix[i][j] = float(pl.operations_matrix[i][j].numerator)/float(pl.operations_matrix[i][j].denominator)
	# Cast to float
	for i in range(0, pl.matrix.shape[0]):
		for j in range(0, pl.matrix.shape[1]):
			pl.matrix[i][j] = float(pl.matrix[i][j].numerator)/float(pl.matrix[i][j].denominator)

	certificate = []
	for i in range(0, pl.lines-1):
		certificate.append(pl.operations_matrix[0][i])
	#if output == True:
	conclusionFile = open("conclusao.txt", "w")
	conclusionFile.write("2\n")
	conclusionFile.write(str(get_solution(pl)) + "\n")
	conclusionFile.write(str(pl.matrix[0][pl.columns-1]) + "\n")
	conclusionFile.write(str(certificate))
	conclusionFile.close()
	

def write_pivoting_output(file, tableaux):
	file.write("[")
	for i in range(0, tableaux.shape[0]):
		file.write("[")
		for j in range(0, tableaux.shape[1]):
			file.write(np.format_float_positional(float(tableaux[i,j]), precision=5))
			if(j != (tableaux.shape[1]-1)):
				file.write(', ')
		if(i != (tableaux.shape[0]-1)):
			file.write("]\n") 
		else:
			file.write("]") 
	file.write("]\n\n")

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

	return lp_solution

def primal_pivoting(pl, output=True):
	print "Primal"
	pivotingFile = open("pivoting.txt", "w")
	tableaux = np.concatenate((pl.operations_matrix, pl.matrix), axis=1)
	while True: #Executar até não haver mais entrada negativa no c
		# Escolher coluna:
		column_index = None
		for i in range(0, pl.columns-1):
			if pl.matrix[0][i] < 0:
				column_index = i
				break
		if column_index == None: # Não existem mais elementos negativos no c
			if(output == True):
				write_sol_output(pl)
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
					for i in range(0, len(d_certificate)):
						d_certificate[i] = float(d_certificate[i].numerator)/float(d_certificate[i].denominator)
					
					conclusionFile = open("conclusao.txt", "w")
					conclusionFile.write("1\n")
					conclusionFile.write(str(d_certificate))
				return pl
		# Calcula a razão entre os elementos de 'b' e 'a' e escolhe o menor:
		min_ratio = None
		pivot_index = ()
		pivot_value = 0
		for i in range(1, pl.lines):
			if not (pl.matrix[i][column_index] <= 0): # A deve ser positivo
				ratio = pl.matrix[i][pl.columns-1]/pl.matrix[i][column_index]
				if ratio < min_ratio or min_ratio == None:
					min_ratio = ratio
					pivot_index = (i, column_index)
					pivot_value = pl.matrix[i][column_index]
		# Transformar o pivot em 1 (e sua linha correspondente)
		
		if pivot_value != 1: ##check this##
			for i in range(0, pl.columns):
				pl.matrix[pivot_index[0]][i] = pl.matrix[pivot_index[0]][i]/pivot_value
			#Atualiza matriz de operações
			for i in range(0, pl.operations_matrix.shape[1]):
				pl.operations_matrix[pivot_index[0]][i] = pl.operations_matrix[pivot_index[0]][i]/pivot_value
		# Zerar elementos
		for i in range(0, pl.lines):
			if i != pivot_index[0]:
				coefficient = pl.matrix[i][pivot_index[1]]*-1 # Acha o valor que devemos multiplicar a linha do pivot para somar na linha que se deseja zerar
				for j in range(0, pl.columns):
					pl.matrix[i][j] = pl.matrix[i][j] + pl.matrix[pivot_index[0]][j]*coefficient
				# Atualiza matrix de operações
				for k in range(0, pl.operations_matrix.shape[1]):
					pl.operations_matrix[i][k] = pl.operations_matrix[i][k] + pl.operations_matrix[pivot_index[0]][k]*coefficient
				

		tableaux = np.concatenate((pl.operations_matrix, pl.matrix), axis=1)
		write_pivoting_output(pivotingFile, tableaux)

	pivotingFile.close()
	return pl

def dual_pivoting(pl):
	print "Dual"
	pivotingFile = open("pivoting.txt", "w")
	tableaux = np.concatenate((pl.operations_matrix, pl.matrix), axis=1)
	
	while True: #Executar até não haver mais entrada negativa no b
		#Escolher linha
		line_index = None
		for i in range(1, pl.lines):
			if pl.matrix[i][pl.columns-1] < 0:
					line_index = i
					break
		if line_index == None: # Não existem mais elementos negativos no b
			write_sol_output(pl)
			return
		else: # Verifica se existem valores negativos em A
			negative_a = False
			for i in range(0, pl.columns-1):
				if pl.matrix[line_index][i] < 0:
					negative_a = True
					break
			if negative_a == False:
				certificate = []
				for i in range(0, pl.operations_matrix.shape[1]):
					certificate.append(float(pl.operations_matrix[line_index][i]))
				conclusionFile = open("conclusao.txt", "w")
				conclusionFile.write("0\n")
				conclusionFile.write(str(certificate))
				return
		# Calcula a razão entre os elementos de 'c' e '-a' e escolhe o menor:
		min_ratio = None
		pivot_index = ()
		pivot_value = 0
		for i in range(0, pl.columns-1):
			if not (pl.matrix[line_index][i] >= 0): # A deve ser negativo
				ratio = pl.matrix[0][i]/(pl.matrix[line_index][i]*-1)
				if ratio < min_ratio or min_ratio == None:
					min_ratio = ratio
					pivot_index = (line_index, i)
					pivot_value = pl.matrix[line_index][i]
		# Transformar o pivot em 1 (e sua linha correspondente)
		if pivot_value != 1:
			for i in range(0, pl.columns):
				pl.matrix[pivot_index[0]][i] = (pl.matrix[pivot_index[0]][i]/pivot_value)
			#Atualiza matriz de operações
			for i in range(0, pl.operations_matrix.shape[1]):
				pl.operations_matrix[pivot_index[0]][i] = (pl.operations_matrix[pivot_index[0]][i]/pivot_value)
		# Zerar elementos
		for i in range(0, pl.lines):
			if i != pivot_index[0]:
				coefficient = pl.matrix[i][pivot_index[1]]*-1 # Acha o valor que devemos multiplicar a linha do pivot para somar na linha que se deseja zerar
				for j in range(0, pl.columns):
					pl.matrix[i][j] = pl.matrix[i][j] + pl.matrix[pivot_index[0]][j]*coefficient
				# Atualiza matrix de operações
				for k in range(0, pl.operations_matrix.shape[1]):
					pl.operations_matrix[i][k] = pl.operations_matrix[i][k] + pl.operations_matrix[pivot_index[0]][k]*coefficient
		tableaux = np.concatenate((pl.operations_matrix, pl.matrix), axis=1)
		write_pivoting_output(pivotingFile, tableaux)

def auxiliar_lp(lp):
	
	original_lp = lp #bkp
	#Salva o vetor c original
	original_c = []
	for i in range(0, lp.columns-1):
		original_c.append(lp.matrix[0][i])
	
	#--- Multiplica por -1 linhas com b negativo
	for i in range(1, lp.lines):
		if(lp.matrix[i][lp.columns-1] < 0):
			#Matriz de operações
			for j in range(0, lp.operations_matrix.shape[1]):
				lp.operations_matrix[i][j] *= -1
			# Matriz
			for j in range(0, lp.columns):
				lp.matrix[i][j] *= -1

	#--- Monta Pl auxiliar (c = 0, nova identidade com custo 1 em cima)
	#Zera entradas do vetor c
	for i in range(0, lp.columns):
		lp.matrix[0][i] = 0
	
	#Exapande a matriz com zeros e adiciona 1's na diagonal principal e no c
	main_diagonal_indexes = []
	for i in range(0, lp.lines-1):
		lp.matrix = np.insert(lp.matrix,lp.columns-1,0,axis=1)
		main_diagonal_indexes.append((i+1,lp.columns-1))
		lp.columns += 1		
	for index in main_diagonal_indexes:
		lp.matrix[index[0]][index[1]] = 1
		lp.matrix[0][index[1]] = 1

	#--- Pivoteia p/ identidade nova
	for i in range(1, lp.lines):
		for j in range(0, lp.columns):
			lp.matrix[0][j] += lp.matrix[i][j]*(-1)
		for j in range(0, lp.operations_matrix.shape[1]):
			lp.operations_matrix[0][j] += lp.operations_matrix[i][j]*(-1)

	#Faz simplex
	lp = primal_pivoting(lp, False)
	if(lp.matrix[0][lp.matrix.shape[1]-1] == 0): # Se VO = 0, viável
		# Recoloca o c
		for i in range(0, len(original_c)):
			lp.matrix[0][i] = original_c[i]

		## Recupera as bases
		bases_columns = []
		for i in range(0, lp.columns-1):
			#verifica coluna
			is_base = True
			for j in range(1, lp.lines):
				if (lp.matrix[j][i] != 0 and lp.matrix[j][i] != 1):
					is_base = False
			if is_base == True: 
				bases_columns.append(i)
		for base in bases_columns:
			for i in range(1, lp.lines):
				if (lp.matrix[i][base] == 1):
					line_index = i
					break
			base_value = lp.matrix[0][base]
			for i in range(0, lp.columns):
				lp.matrix[0][i] = lp.matrix[0][i] + (lp.matrix[line_index][i] * (base_value*-1))
			for i in range(0, lp.operations_matrix.shape[1]):
				lp.operations_matrix[0][i] = lp.operations_matrix[0][i] + (lp.operations_matrix[line_index][i] * (base_value*-1))

		# Remove colunas da pl auxiliar
		for i in range(lp.columns-2, lp.columns-lp.lines-1, -1):
			#print i
			lp.matrix = np.delete(lp.matrix, i, 1)
			lp.columns -= 1
		
		lp = primal_pivoting(lp)
		
	else:
		certificate = []
		for i in range(0, lp.operations_matrix.shape[1]):
			certificate.append(float(lp.operations_matrix[0][i]))
		
		conclusionFile = open("conclusao.txt", "w")
		conclusionFile.write("0\n")
		conclusionFile.write(str(certificate))

	
def read_file():
	with open(sys.argv[1]) as f:
		content = f.readlines()
	
	tableaux = Tableaux(int(content[0])+1, int(content[1])+1, np.array(eval(content[2]), dtype="object"))
	
	return tableaux

def main():
	tableaux = read_file()
	np.set_printoptions(precision=6, suppress=True)
	
	# Checar qual método usar (primal ou dual)
	negative_b = False
	negative_c = False

	
	for i in range(1, tableaux.lines):
		if tableaux.matrix[i][tableaux.columns-1] < 0: # Entrada negativa no vetor B
			negative_b = True
	
	for i in range(0, tableaux.columns-1):
		if tableaux.matrix[0][i] < 0: # Entrada negativa no vetor c
			negative_c = True

	if (negative_b == True and negative_c == True) or (negative_b == False and negative_c == False): # Entrada negativa no b e no c -> AUXILIAR
		auxiliar_lp(tableaux)
	
	elif negative_b == True and negative_c == False: # Entrada negativa no B -> DUAL
		dual_pivoting(tableaux)
	
	elif negative_c == True and negative_b == False: # Entrada negativa no C -> PRIMAL
		primal_pivoting(tableaux)


if __name__ == "__main__":
	main()