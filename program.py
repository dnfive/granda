import re
import tkinter as tk
import configparser

port = []
config = {
	'IP': '',
	'Desc': '',
	'Mask': ''
}

routes = []
static_route = {
	'end_net': '',
	'mask': '',
	'next_hop': ''	
}

stop_route = {
	'end_net': '',
	'enabled': False
}



def gui():
	global entries
	global router_var
	global labels

	# Создание главного окна
	root = tk.Tk()

	# Создание столбца слева
	left_frame = tk.Frame(root)
	left_frame.pack(side=tk.LEFT, padx=10)

	# Создание кнопок в столбце слева
	button1 = tk.Button(left_frame, text="Кнопка 1", command=add_ip_fields)
	button1.pack(pady=10)

	button2 = tk.Button(left_frame, text="Кнопка 2", command=open_main_field)
	button2.pack(pady=10)

	button3 = tk.Button(left_frame, text="Кнопка 3", command=open_main_field)
	button3.pack(pady=10)

	# Создание главного поля
	main_frame = tk.Frame(root)

	# Создание строки с выбором маршрутизатора
	router_var = tk.StringVar()
	router_dropdown = tk.OptionMenu(main_frame, router_var, "Маршрутизатор 1", "Маршрутизатор 2", "Маршрутизатор 3")
	router_dropdown.pack(pady=10)

	# Создание кнопки "Сохранить"
	save_button = tk.Button(main_frame, text="Сохранить", command=save)
	save_button.pack(pady=10)

	# Размещение главного поля справа
	main_frame.pack(side=tk.RIGHT, padx=10, pady=10)

	# Запуск главного цикла
	root.mainloop()

def main():

	for i in range(0, 5): # здесь можно изменить максимальное количество настраиваемых (которые мы настраиваем) портов
		port.append(config)

	for i in range(0,10): # здесь можно изменить кол-во максимальных статических маршрутов
		routes.append(static_route)


	print("[Настройка портов/интерфейсов]")
	while True:	
		ans = input( 'Выберите порт, для настройки или введите \'-1\' для отказа: ')
		if ans == '-1':
			break
		ans = int(ans)
		while True:
			port[ans]['IP'] = input('Введите IP адрес порта ' + str(ans) + ': ')
			if not check_ip_address(port[ans]['IP']):
				print("Некорректный IP адрес!")
			else:
				break
		#if здесь будет проверка IP адреса на корректность с использование регулярных выражений
		#если всё заебись будет break
		port[ans]['Mask'] = input('Введите маску порта ' + str(ans) + ': ')
		port[ans]['Desc'] = input('Введите описание порта ' + str(ans) + ': ')
		print(port[ans])


	n = 0
	print("[Настройка статических маршрутов]")
	while True:
		while True:
			ans = input('Введите IP адрес сети назначения ' + str(n+1) + ' статического маршрута или введите \'-1\' для отказа: ')
			if ans == '-1':
				break
			if not check_ip_address(ans):
				print("Некорректный IP адрес!")
			else:
				break
		if ans == '-1':
			break
		#elif здесь будет проверка IP адреса на корректность с использование регулярных выражений
		routes[n]['end_net'] = ans
		routes[n]['mask'] = input('Введите маску сети назначение для ' + str(n+1) + '  статического маршрута: ')
		while True:
			routes[n]['next_hop'] = input('Введите IP адрес шлюза для ' + str(n+1) + ' статического маршрута: ')
			if not check_ip_address(routes[n]['next_hop']):
				print("Некорректный IP адрес!")
			else:
				break
		n += 1
		print(routes[n])

	print('[Настройка тупикового маршрута]')
	while True:
		stop_route['end_net'] = input('Введите IP адрес сети, используемой для тупикового маршрута, или введите \'-1\' для отказа: ')
		if stop_route['end_net'] == '-1':
			stop_route['enabled'] = False
			break
		else:
			stop_route['end_net'] = True
			if not check_ip_address(stop_route['end_net']):
				print("Некорректный IP адрес!")
			else:
				break
			#elif здесь будет проверка IP адреса на корректность с использование регулярных выражений

	#BGP

	#RIP

	#
	print("Good Job!")
	print(config)
	print(static_route)
	print(stop_route)
	save_dict_to_ini(config, "config.ini")
	save_dict_to_ini(static_route, "static_route.ini")
	save_dict_to_ini(stop_route, "stop_route.ini")
	print("Выберите маршрутизатор для которого вы бы хотели собрать конфигурацию:")
	print("1) Juniper")
	print("2) Dionis")
	print("3) Cisco")
	ans = input("Выберите: ")
	ans = int(ans)
	if ans == 1:
		ConvertToJuniper(config, static_route, stop_route)
	elif ans == 2:
		ConvertToDionis(config, static_route, stop_route)
	elif ans == 3:
		ConvertToCisco(config, static_route, stop_route)

def ConvertToJuniper(config, static_route, stop_route):
	pass

def ConvertToDionis(config, static_route, stop_route):
	pass

def ConvertToCisco(config, static_route, stop_route):
	pass

def check_ip_address(ip_address):
	pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
	return re.match(pattern, ip_address) is not None

def submit():
	global entries
	global router_var
	global labels
	ip_addresses = [entry.get() for entry in entries]
	selected_router = router_var.get()
	print("IP Addresses: ")
	for ip in ip_addresses:
		print(ip)

	print("Selected Router: ", selected_router)
	labels[0].config(text=f"IP Address 1.0: ")

def save_dict_to_ini(dictionary, filename):
	config = configparser.ConfigParser()
	config.read_dict({'section': dictionary})

	with open(filename, 'w') as configfile:
		config.write(configfile)

def open_main_field():
	main_field.pack()

def save():
	selected_router = router_var.get()

def add_ip_fields():
	for _ in range(4):
		ip_entry = tk.Entry(main_frame)
		ip_entry.pack(pady=5)

if __name__ == "__main__":
	gui()
	main()


