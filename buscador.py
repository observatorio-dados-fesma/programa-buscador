
from robo2 import Robo
import PySimpleGUI as sg

sg.theme('DarkBlack')

layout = [
	[sg.Text('Buscador de Processos', font = ('Lato', 20))],
	[sg.Text('Credenciais do Eprocessos')], 
	[sg.InputText('CPF', key = '-USER-'), sg.InputText('Senha', key = '-PWD-')],
	[sg.InputText('Caminho do arquivo', key = '-FILE-'), sg.FileBrowse('Buscar')],
	[sg.Button('Iniciar Consulta'), sg.Button('Testar Consulta')]
]

window = sg.Window('Buscador de Processos', layout)

while True:

	event, values = window.read()

	robo = Robo(cpf = values['-USER-'], senha = values['-PWD-'])

	if event == 'Iniciar':

		arquivo = robo.read_path(values['-FILE-'])

		robo.buscar(lista = arquivo)

	if event == 'Testar Consulta':

		robo.buscar(lista = robo.read_path('processos.txt'))

	elif event == sg.WINDOW_CLOSED:

		break

window.close()
