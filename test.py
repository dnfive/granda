from flask import Flask, render_template, request, session
import re
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cb02820a3e94d72c9f950ee10ef7e3f7a35b3f5b'



@app.route('/', methods=('GET', 'POST'))
def index():
	#print(session[0])
	errors = []
	success = ""
	number_int = ""
	ip_int = ""
	mask_int = ""
	desc_int = ""
	if request.method == 'POST':
		number_int = request.form['number_int']
		ip_int = request.form['ip_int']
		valid_ip = check_ip_address(ip_int)
		if not valid_ip:
			errors.append("Некорректный IP адрес!")
		mask_int = request.form['mask_int']
		if int(mask_int) < 0 or int(mask_int) > 32:
			errors.append("Некорректная маска!")
		desc_int = request.form['desc_int']
		# print("Number Int ", number_int)
		# print("IP Int ", ip_int)
		# print("Mask Int ", mask_int)
		# print("Desc Int ", desc_int)
		if not errors:
			interface = {
			'number_int': int(number_int),
			'ip_int': ip_int,
			'mask_int': mask_int,
			'desc_int': desc_int
			}
			save_dict_to_file(route, "interfaces/interface_" + number_int + ".json")
			success = "Интерфейс " + number_int + " Успешно сохранён!"
			number_int = ""
			ip_int = ""
			mask_int = ""
			desc_int = ""

	return render_template('index.html', success=success, errors=errors, ip_int=ip_int, number_int=number_int, mask_int=mask_int, desc_int=desc_int)

@app.route("/routing", methods=('GET', 'POST'))
def routing():
	errors = []
	success = ""
	number_route = ""
	dest_route = ""
	mask_route = ""
	gate_route = ""
	if request.method == 'POST':
		number_route = request.form['number_route']
		dest_route = request.form['dest_route']
		mask_route = request.form['mask_route']
		mask_route = int(mask_route)
		gate_route = request.form['gate_route']
		if not check_ip_address(dest_route):
			errors.append("Некорректный IP адрес сети назначения!")
		if not check_ip_address(gate_route):
			errors.append("Некорректный IP адрес шлюза!")
		if mask_route < 0 or mask_route > 32:
			errors.append("Некорректная маска!")
		if not errors:
			route = {
			'number_route': number_route,
			'dest_route': dest_route,
			'mask_route': mask_route,
			'gate_route': gate_route
			}
			save_dict_to_file(route, "routes/route_" + number_route + ".json")
			success = "Маршрут № " + number_route + " успешно сохранён!"
			number_route = ""
			dest_route = ""
			mask_route = ""
			gate_route = ""

	return render_template("routing.html", success=success, errors=errors, number_route=number_route, dest_route=dest_route, mask_route=mask_route, gate_route=gate_route)

def check_ip_address(ip_address):
	pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
	return re.match(pattern, ip_address) is not None

def save_dict_to_file(dictionary, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(dictionary, file)
        print(f"Словарь сохранен в файл '{filename}'")
    except Exception as e:
        print(f"Произошла ошибка при сохранении словаря в файл: {str(e)}")

def load_dict_from_file(filename):
    try:
        with open(filename, 'r') as file:
            loaded_dict = json.load(file)
        print(f"Словарь загружен из файла '{filename}'")
        return loaded_dict
    except Exception as e:
        print(f"Произошла ошибка при загрузке словаря из файла: {str(e)}")
        return None


if __name__ == '__main__':
	app.run(port=8080, debug=True)