from ftplib import FTP
from datetime import date
import os
import sys

print ("\n###################################### RBMC DATA DOWNLOADER ######################################")
print ("\n\nOBS.: Ha necessidade de organizacao das pastas por ano no local onde serao gravados os arquivos")
print ("\n\nDigite as estacoes desejadas no formato XXXX; digite \"f\" para encerrar digitacao.")
final = False
l = 1
lista = []
while not final:
	est = input("\t"+str(l)+"a estacao: ")
	if est != "f" and len(est) == 4:
		lista.append(est.lower())
		l+=1
	elif est != "f" and len(est) != 4:
		print("\t### Formato inadequado, tente novamente ###")
	else:
		final = True

final = False
while not final:
	ano = input("Ano de inicio: ")
	if not ano.isdigit():
		print("\t### Ano de inicio invalido, tente novamente ###")
	elif int(ano) < 2010:
		print("\t### Ano de inicio invalido, tente novamente ###")
	else:
		ano_i = int(ano)
		final = True

final = False
while not final:
	ano = input("Ano de termino: ")
	if not ano.isdigit():
		print("\t### Ano de termino invalido, tente novamente ###")
	elif int(ano) > date.today().year:
		print("\t### Ano de termino invalido, tente novamente ###")
	else:
		ano_f = int(ano)
		final = True

final = False
while not final:
	dia = input("Dia de inicio por ano (inclusive): ")
	if not dia.isdigit():
		print("\t### Dia de inicio invalido, tente novamente ###")
	elif int(dia) < 1 or int(dia) > 366:
		print("\t### Dia de inicio invalido, tente novamente ###")
	else:
		dia_i = int(dia)
		final = True


final = False
while not final:
	dia = input("Dia de termino por ano (inclusive): ")
	if not dia.isdigit():
		print("\t### Dia de termino invalido, tente novamente ###")
	elif int(dia) < 1 or int(dia) > 366 or int(dia) < dia_i:
		print("\t### Dia de termino invalido, tente novamente ###")
	else:
		dia_f = int(dia)
		final = True

final = False
while not final:
	local = input("\n\nEndereco onde deseja salvar os arquivos (sem barra no final): ")
	if os.path.isdir(local):
		local += "/"
		final = True
	else:
		print("\n\t### Endereco invalido, tente novamente ###")

final = False		
for i in range(ano_i, ano_f+1):
	if not os.path.isdir(local+str(i)):
		print("\n\t### Estrutura de pastas no destino incompativel com a necessaria ###\n\t### E preciso criar uma pasta por ano no local informado ###\n\t### Tente novamente ###\n")
		final = True
		break

if not final:

	f = open(local+"/log.txt", "a")
	ftp = FTP('geoftp.ibge.gov.br')
	ftp.login()
	for i in range(ano_i, ano_f+1):
		print(i)
		os.chdir(local+str(i)+'/')
		for j in range(dia_i,dia_f+1):
			dir = 'informacoes_sobre_posicionamento_geodesico/rbmc/dados/'
			if j<10:
				a = '00'+str(j)
			elif j<100:
				a = '0'+str(j)
			else:
				a = str(j)
			print (a)
			dir+=str(i)+'/'+a
			ftp.cwd(dir)

			p = 0
			while p<len(lista):
				arq = lista[p]+a+"1.zip"
				print (arq)
				print (dir)
				if arq in ftp.nlst("."):
					print ("Baixando "+arq)
					try:
						fhandle = open(arq, 'wb')
						ftp.retrbinary('RETR ' + arq, fhandle.write)
						print (arq+" baixado com sucesso em "+local+str(i)+"/"+arq+"\n\n")
					except Exception as e: 
						print (str(e))
						print ("##################### Erro baixando "+arq+" #####################\n\n")
				else:
					f.write(arq+" de "+str(i)+" não encontrado e não baixado\n")
					print (arq+" de "+str(i)+" não encontrado e não baixado\n")
				p+=1
			dir = '/'
			ftp.cwd(dir)
	ftp.quit()
	f.close()