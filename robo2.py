'''Robô de Monitoramento de Processos'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from json import dump, load
from os import listdir, mkdir, rmdir, remove
from pandas import DataFrame
from datetime import datetime
from time import sleep
from re import search, findall

path = ''

class Robo(object):

	def __init__(self, cpf, senha):

		self.cpf = cpf
		self.senha = senha

	def numero(self, num):

		d = {6: '00000', 7: '0000', 8: '000', 9: '00', 10: '0'}

		return d.get(len(num)) + num 

	def create_dir(self):

		nome_pasta = 'temp_' + str(int(datetime.now().timestamp()))

		mkdir(nome_pasta)

	def base(self, data, nome):

		pasta = [i for i in listdir() if i[0:4] == 'temp'][0]

		with open(f'{pasta}/{nome}.json', 'w') as file:

			dump(data, file, indent = 2)

	def consulta(self, list_proc):

		user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'

		chrome_options = Options()

		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--log-level=3')
		# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
		chrome_options.add_argument(f'user-agent={user_agent}')
		# chrome_options.add_argument("--incognito")
		# chrome_options.add_argument('--disable-extensions')
		# chrome_options.add_argument('--profile-directory=Default')
	
		driver = webdriver.Chrome(options = chrome_options)

		# driver.delete_all_cookies()
		# driver.get('chrome://settings/clearBrowserData')
		# driver.find_element(By.XPATH, '//settings-ui')
		# driver.send_keys(Keys.TAB, Keys.ENTER)

		print('iniciando')

		driver.get('https://eprocessos.ma.gov.br/ged/index.jsp')

		# driver.switch_to.alert.accept()

		user = driver.find_element(By.XPATH, '//*[(@id = "login")]')
		
		user.send_keys(self.cpf, Keys.TAB, self.senha)
		
		sleep(1)
		
		botao = driver.find_element(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "botaoLogin", " " ))]')
		
		sleep(4)

		botao.click()

		print('sucesso no login')

		sleep(5)

		# img = driver.find_element(By.XPATH, '//img')
		# 
		# img.click()
		
		driver.get('https://eprocessos.ma.gov.br/ged/consultar/processos/processos.jsp')
		
		for i in list_proc:

			processo = driver.find_element(By.XPATH, '//*[(@id = "processo")]')
	
			if len(i) < 8:

				processo.send_keys(i[:-4])

				botao = driver.find_element(By.XPATH, '//*[(@id = "botaoPesquisarLocalizarProcessos")]')

				# driver.switch_to.alert.accept()
	
				botao.click()

			else:
	
				processo.send_keys(i)
	
				botao = driver.find_element(By.XPATH, '//*[(@id = "botaoPesquisarLocalizarProcessos")]')
	
				botao.click()
			
			sleep(4)

			try:

				html = driver.page_source
		
				x = search('id="Processos', html)
	
				x = x.end()
	
				pagina = driver.get(f'https://eprocessos.ma.gov.br/ged/cadastrar/processos/processos.jsp?codigoProcesso={html[int(x):int(x) + 7]}&numeroProcesso={self.numero(num = i)}&virtual=n')
				
				sleep(2)
				
				botao_mov = driver.find_element(By.XPATH, '//*[@id="abaMovimentacoes"]/a')
	
				botao_mov.click()
	
				sleep(1)
				
				body = driver.find_element(By.TAG_NAME, 'body')
	
				body = body.text
	
				localizacao2 = search(r'Data/Hora Mov\n(.*?)   ', body).group(1)

				datahora = search(r'Data/Hora Mov\n(.*?)\n', body).group(1)[-19:][0:10]
	
				data = {'processo': self.numero(num = i), 'ultima': localizacao2, 'data': datahora}
		
				self.base(data = data, nome = i)
	
				print(i)
	
				driver.get('https://eprocessos.ma.gov.br/ged/consultar/processos/processos.jsp')
	
				sleep(1)
	
			except:
				
				localizacao2 = 'Não Localizado ou Número Incorreto / Não Encontrado'
				
				datahora = 'Não Localizado ou Número Incorreto / Não Encontrado'

				data = {'processo': self.numero(num = i), 'ultima': localizacao2, 'data': datahora}

				self.base(data = data, nome = i)
			
				print(i + ' com falha')

				driver.get('https://eprocessos.ma.gov.br/ged/consultar/processos/processos.jsp')

				sleep(1)

	def numero_correto(self, x):

		return x[0:7].lstrip('0') + '/' + x[-4:]

	def buscar(self, lista):

		self.create_dir()

		self.consulta(list_proc = lista)

		l = []

		pasta = [i for i in listdir() if i[0:4] == 'temp'][0] + '/'

		for i in listdir(pasta):
		
			with open(pasta + i) as file:
		
				l.append(load(file))
		
		d = DataFrame(l)

		d['processos'] = d['processo'].apply(self.numero_correto)

		del d['processo']

		tmsp = str(int(datetime.now().timestamp()))

		d.to_excel(f'processos_coleta_{tmsp}.xlsx', index = False)

		for i in listdir(pasta):

			remove(pasta + i)

		rmdir(pasta)

	def read_path(self, path):

		with open(path, 'r') as file:

			data = file.read()

		return data.split()
