import dearpygui.dearpygui as dpg
from requests import get

def oprint(text):
	if dpg.does_item_exist('output_child'):
		dpg.delete_item('output_child')
	dpg.add_child_window(tag='output_child', parent='main_window', height=100)
	dpg.add_text(text, parent='output_child')

def send(path):
	ip = dpg.get_value('ip')
	port = dpg.get_value('port')
	url = f'http://{ip}:{port}{path}'
	try:
		r = get(url)
		if r.status_code == 200:
			return r.text
	except Exception as e:
		return False
	return False

def cb_service(sender, data, user_data):
	print(f"Service: {user_data}")
	r = send(f'/service/{user_data.lower()}')
	if r:
		oprint(f"Success: {r}")
	else:
		oprint("Failed")

def cb_execute(sender, data):
	oper = dpg.get_value('oper')
	stat = dpg.get_value('stat')
	val = dpg.get_value('input_1')
	
	if not oper or not stat or not val:
		oprint("Missing data")
		return
	
	oper = oper.lower()
	stat = stat.lower()
	
	r = send(f'/{oper}/{stat}/{val}')
	if not r:
		oprint("Failed")
	else:
		oprint(f"Success: {r}")

def show_logger():
	dpg.show_tool(dpg.mvTool_Logger)

def show_metrics():
	dpg.show_tool(dpg.mvTool_Metrics)

def show_documentation():
	dpg.show_tool(dpg.mvTool_Doc)

def show_debug():
	dpg.show_tool(dpg.mvTool_Debug)

dpg.create_context()
dpg.create_viewport(title='Squid Firewall Manager', width=600, height=500)
dpg.setup_dearpygui()

with dpg.viewport_menu_bar():
	with dpg.menu(label="Service"):
		dpg.add_menu_item(label="Start", callback=cb_service, user_data="Start")
		dpg.add_menu_item(label="Restart", callback=cb_service, user_data="Restart")
		dpg.add_menu_item(label="Stop", callback=cb_service, user_data="Stop")
	
	with dpg.menu(label="Tools"):
		dpg.add_menu_item(label="Show Logger", callback=show_logger)
		dpg.add_menu_item(label="Show Metrics", callback=show_metrics)
		dpg.add_menu_item(label="Show Documentation", callback=show_documentation)
		dpg.add_menu_item(label="Show Debug", callback=show_debug)

with dpg.window(tag='main_window', label='Squid Firewall Manager', width=600, height=500):
	dpg.add_text("Squid Firewall Manager")
	dpg.add_separator()
	
	dpg.add_input_text(tag='ip', label='IP Address', default_value='127.0.0.1')
	dpg.add_input_int(tag='port', label='Port', default_value=7505)
	
	dpg.add_spacer(height=10)
	dpg.add_separator()
	dpg.add_spacer(height=10)
	
	dpg.add_combo(tag='stat', label='Action', items=["Add", "Remove", "Show"], default_value="Show")
	dpg.add_combo(tag='oper', label='Type', items=["Domain", "Port", "Arp"], default_value="Domain")
	dpg.add_input_text(tag='input_1', label='Value', default_value='')
	dpg.add_button(label='Execute!', callback=cb_execute)
	
	dpg.add_spacer(height=10)
	dpg.add_separator()
	dpg.add_text("Output:")

# Create output child window
with dpg.child_window(tag='output_child', parent='main_window', height=100):
	dpg.add_text("Ready...")

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()