from flask import Flask, render_template, request, session
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cb02820a3e94d72c9f950ee10ef7e3f7a35b3f5b'

@app.route('/', methods=('GET', 'POST'))
def index():
	print(session[0])
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
			session[int(number_int)] = {
			'ip_int': ip_int,
			'mask_int': mask_int,
			'desc_int': desc_int
			}
			success = "Интерфейс " + number_int + " Успешно сохранён!"
			number_int = ""
			ip_int = ""
			mask_int = ""
			desc_int = ""

	return render_template('index.html', success=success, errors=errors, ip_int=ip_int, number_int=number_int, mask_int=mask_int, desc_int=desc_int)

@app.route("/routing")
def routing():
	return render_template("routing.html")

@app.route('/process', methods=['POST'])
def process():
	input_data = request.form['input_data']
	# Обработка введенных данных
	# ...
	return 'Данные успешно обработаны'

def check_ip_address(ip_address):
	pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
	return re.match(pattern, ip_address) is not None

if __name__ == '__main__':
	app.run(port=8080, debug=True)