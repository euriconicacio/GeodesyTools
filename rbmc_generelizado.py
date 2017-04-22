from ftplib import FTP
import datetime
import os

def bissexto(ano): return (ano % 4 == 0 and (ano % 400 == 0 or ano % 100 != 0))

dm_normal = [31,28,31,30,31,30,31,31,30,31,30,31]
dm_bissexto = [31,29,31,30,31,30,31,31,30,31,30,31]
nomes = ['PITN','MTSR','AMCO','EESC','SPBO','RSAL','BAIL','GOGY','SCFL','PEAF','PICR','MABB','UBE1','GVA1','RSCL','PIFL','MTJI','PASM','AMHA','AMTA','MSAQ','SPS1','SEAJ','AMTE','SPDR','SPPI','RNPF','COAM','SPFE','SPFR','SPC1','IFSC','AMBC','BABJ','PRCV','MSDR','SCAQ','MGV1','RSPE','JAMG','BEPA','APLJ','AMPR','AMUA','ITAM','MTNX','PBJP','CESB','MCL1','SPTU','SPLI','BAIT','AMMU','GOUR','APS1','MTCN','ALAR','BABR','BAIR','BATF','BAVC','BELE','BOAV','BRAZ','BRFT','CEEU','CEFE','CEFT','CHPI','CRAT','CRUZ','CUIB','GOJA','ILHA','IMBT','IMPZ','MABA','MABS','MAPA','MGBH','MGIN','MGMC','MGRP','MGUB','MSCG','MTCO','MTSF','NAUS','NEIA','ONRJ','OURI','PAAT','PAIT','PBCG','PEPE','PISR','POAL','POLI','POVE','PPTE','PRGU','PRMA','RECF','RIOB','RIOD','RJCG','RNMO','RNNA','ROCD','ROGM','ROJI','ROSA','SAGA','SALU','SAVO','SCCH','SCLA','SJRP','SMAR','SPAR','SSA1','TOGU','TOPL','UBA1','UFPR','VICO','SPJA','SJSP']
		
print ("\n###################################### RBMC DATA DOWNLOADER ######################################")
print ("\n\nOBS.: Ha necessidade de organizacao das pastas por ano no local onde serao gravados os arquivos")
print ("\n\nDigite as estacoes desejadas no formato XXXX; digite \"f\" para encerrar digitacao.")
final = False
l = 1
lista = []
while not final:
	est = input("\t"+str(l)+"a estacao: ")
	if est != 'f' and len(est) == 4 and est.upper() in nomes:
		lista.append(est.lower())
		l+=1
	elif est != 'f' and (len(est) != 4 or est.upper() not in nomes):
		print("\t### Entrada invalida, tente novamente ###")
	else:
		final = True


final = False
while not final:
	x = input("Ano de inicio: ")
	if not x.isdigit():
		print("\t### Ano de inicio invalido, tente novamente ###")
	elif int(x) > datetime.datetime.now().year:
		print("\t### Ano de inicio invalido, tente novamente ###")
	else:
		ano_inicio = int(x)
		final = True


final = False
while not final:
	x = input("Ano de termino: ")
	if not x.isdigit():
		print("\t### Ano de termino invalido, tente novamente ###")
	elif int(x) > datetime.datetime.now().year or int(x) < ano_inicio:
		print("\t### Ano de termino invalido, tente novamente ###")
	else:
		ano_final = int(x)
		final = True		


final = False
while not final:
	x = input("Mes de inicio: ")
	if not x.isdigit():
		print("\t### Mes de inicio invalido, tente novamente ###")
	elif int(x) > 12 or int(x) < 1:
		print("\t### Mes de inicio invalido, tente novamente ###")
	else:
		mes_inicio = int(x)
		final = True


final = False
while not final:
	x = input("Mes de termino: ")
	if not x.isdigit():
		print("\t### Mes de termino invalido, tente novamente ###")
	elif (int(x) > 12 or int(x) < 1) or (ano_inicio == ano_final and int(x) < mes_inicio):
		print("\t### Mes de termino invalido, tente novamente ###")
	else:
		mes_final = int(x)
		final = True	


final = False
while not final:
	x = input("Dia de inicio (inclusive): ")
	if not x.isdigit():
		print("\t### Dia de inicio invalido, tente novamente ###")
	elif (int(x) < 1 or (bissexto(ano_inicio) and int(x) > dm_bissexto[mes_inicio-1]) or (not bissexto(ano_inicio) and int(x) > dm_normal[mes_inicio-1])):
		print("\t### Dia de inicio invalido, tente novamente ###")
	else:
		dia_inicio = int(x)
		final = True


final = False
while not final:
	x = input("Dia de termino (inclusive): ")
	if not x.isdigit():
		print("\t### Dia de termino invalido, tente novamente ###")
	elif (int(x) < 1 or (bissexto(ano_final) and int(x) > dm_bissexto[mes_final-1]) or (not bissexto(ano_final) and int(x) > dm_normal[mes_final-1])):
		print("\t### Dia de termino invalido, tente novamente ###")
	else:
		dia_final = int(x)
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
for i in range(ano_inicio, ano_final+1):
	if not os.path.isdir(local+str(i)):
		print("\n\t### Estrutura de pastas no destino incompativel com a necessaria ###\n\t### E preciso criar uma pasta por ano no local informado ###\n\t### Tente novamente ###\n")
		final = True
		break

diac_i = int(datetime.datetime(year=ano_inicio, month=mes_inicio, day=dia_inicio).strftime('%j'))
diac_f = int(datetime.datetime(year=ano_final, month=mes_final, day=dia_final).strftime('%j'))
		
if not final:
	f = open(local+"/log.txt", "a")
	ftp = FTP('geoftp.ibge.gov.br')
	ftp.login()
	for i in range(ano_inicio, ano_final+1):
		print("Ano "+str(i))
		os.chdir(local+str(i)+'/')
		if i == ano_inicio and ano_inicio != ano_final:
			dia_i = diac_i
			if bissexto(ano_inicio):
				dia_f = 366
			else:
				dia_f = 365
		elif i == ano_final and ano_inicio != ano_final:
			dia_i = 1
			dia_f = diac_f
		elif ano_inicio == ano_final:
			dia_i = diac_i
			dia_f = diac_f
		else:
			dia_i = 1
			if bissexto(ano_inicio):
				dia_f = 366
			else:
				dia_f = 365		
			
		for j in range(dia_i,dia_f+1):
			dir = 'informacoes_sobre_posicionamento_geodesico/rbmc/dados/'
			if j<10:
				a = '00'+str(j)
			elif j<100:
				a = '0'+str(j)
			else:
				a = str(j)
			print ("Dia "+a)
			dir+=str(i)+'/'+a
			ftp.cwd(dir)

			p = 0
			while p<len(lista):
				arq = lista[p]+a+"1.zip"
				print (arq)
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
	print ("\nArquivos baixados com sucesso!\nFinalizando RBMC Data Downloader.\n")
