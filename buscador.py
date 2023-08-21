
from robo2 import Robo
import PySimpleGUI as sg

robo = Robo()

layout = [
	[sg.Text('Buscador de Processos', font = ('Lato', 20))],
	[sg.InputText(key = '-FILE-'), sg.FileBrowse()],
	[sg.Button('Buscar')]
]

window = sg.Window('Buscador de Processos', layout)

while True:

	event, values = window.read()

	# arquivo = robo.read_path(values['-FILE-'])

	if event == 'Buscar':

		arquivo = robo.read_path(values['-FILE-'])

		robo.buscar(lista = arquivo)

	elif event == sg.WINDOW_CLOSED:

		break

window.close()
