from dearpygui.dearpygui import *
from requests import get

def oprint(text):
	if does_item_exist('output_child'):
		delete_item('output_child')
	add_child('output_child')
	add_text(text)
	end()

def cb_execute(sender, data):
	print("cb_execute!")
	stat = get_value("stat")
	oper = get_value("oper")
	val = get_value("input_1")
	set_out(val)
	if not (stat and oper and val):
		oprint("Missing data")
		return

def send(path):
	ip = get_value('ip')
	port = get_value('port')
	ip = f'http://{ip}:{str(port)}'
	r = get(ip + path)
	if r.status_code == 200:
		return r.text
	return False

def cb_service(sender, data):
	print(sender, data)
	r = send(f'/service/{sender.lower()}')
	if r:
		oprint("Success")
	else:
		oprint("Failed")

def cb_execute(sender, data):
	oper = get_value('oper').lower()
	stat = get_value('stat').lower()
	val = get_value('input_1')
	r = send(f'/{oper}/{stat}/{val}')
	if not r:
		oprint("Failed")
	else:
		oprint("Success")

##
add_menu_bar("MenuBar")

add_menu("Service")
add_menu_item("Start", callback=cb_service)
add_menu_item("Restart", callback=cb_service)
add_menu_item("Stop", callback=cb_service)
end()

add_menu("Tools")
add_menu_item("Show Logger", callback=show_logger)
add_menu_item("Show Metrics", callback=show_metrics)
add_menu_item("Show Documentation", callback=show_documentation)
add_menu_item("Show Debug", callback=show_debug)
end()

end()
#
add_text("Squid Firewall Manager")

add_input_text('ip')
add_input_int('port', default_value=3128)

add_spacing(count=5)

add_combo("stat", ["Add", "Remove", "Show"])
add_combo("oper", ["Domain", "Port", "App"])
add_input_text("input_1")
add_button('Execute!', callback=cb_execute)

start_dearpygui()