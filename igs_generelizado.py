from ftplib import FTP
import os
import sys

print ("\n######################################################### IGS DATA DOWNLOADER ########################################################")
print ("\n\nOBS.: Ha necessidade de organizacao das pastas por ano no local onde serao gravados os arquivos (uma pasta por semana GPS desejada)")

final = False
while not final:
	s = input("Semana GPS inicial (inclusive): ")
	if not s.isdigit():
		print("\t### Semana GPS invalida, tente novamente ###")
	elif int(s) < 723 or int(s) > 366:
		print("\t### Semana GPS invalida, tente novamente ###")
	else:
		s1 = int(s)
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
for i in range(s1, s2+1):
	if not os.path.isdir(local+str(i)):
		print("\n\t### Estrutura de pastas no destino incompativel com a necessaria ###\n\t### E preciso criar uma pasta por ano no local informado ###\n\t### Tente novamente ###\n")
		final = True
		break

if not final:
	f = open(local+"log.txt", "a")
	ftp = FTP('ftp.igs.org')
	ftp.login()
	for i in range(s1, s2+1):
		print(i)
		os.chdir(local+str(i)+'/')
		dir = 'pub/gps/'
		dir+=str(i.zfill(4))+'/'
		ftp.cwd(dir)

		for j in range(0,7):
			#igs1888j.sp3.Z
			arq = "igs"+str(i)+str(j)+".sp3.Z"
			print (arq)
			print (dir)
			if arq in ftp.nlst("."):
				print ("Baixando "+arq)
				try:
					fhandle = open(arq, 'wb')
					ftp.retrbinary('RETR ' + arq, fhandle.write)
					print (arq+" baixado com sucesso em /home/eurico/Prog/Py/RBMC/efem/"+str(i)+"/"+arq+"\n\n")
				except Exception as e: 
					print (str(e))
					print ("##################### Erro baixando "+arq+" #####################\n\n")
			else:
				f.write(arq+" de "+str(i)+" não encontrado e não baixado\n")
				print (arq+" de "+str(i)+" não encontrado e não baixado\n")

		dir = '/'
		ftp.cwd(dir)
	ftp.quit()
	f.close()