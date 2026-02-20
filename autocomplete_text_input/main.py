import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(width=400, height=200, title='Autocomplete field example')

# autocomplete global vars
autocomplete_values = ['John', 'Joanna', 'Jane', 'Jupiter', 'Jeff']
current_field = None
current_items = []
current_text = ''
current_autocomplete_item = -1
current_autocomplete_text = ''

# sets current values as global vars
def set_current_text(sender, app_data, user_data):
	global current_text, current_field
	current_text = app_data
	current_field = sender

# autocomplete logic
def autocomplete(sender, app_data, user_data):
	global current_field, current_items, current_text, current_autocomplete_item, current_autocomplete_text, autocomplete_values

	win = 'autocomplete_window'
	evaluate = False
	field = current_field
	value = None
	sort_items = True
	marked_item_color = (123, 252, 3)

	if dpg.is_item_focused(field):
		value = current_text
		evaluate = True

	if evaluate and 'select' in user_data:
		matches = list(set([item for item in autocomplete_values if value.lower() in item.lower()]))
		if sort_items: matches = sorted(matches)
		
		if len(matches):
			
			dpg.delete_item(win, children_only=True)
			pos = dpg.get_item_pos(field)
			pos[1] += 20
			dpg.set_item_pos(win, pos)
			field_rect_size = dpg.get_item_rect_size(field)
			dpg.configure_item(win, width=field_rect_size[0])

			inc = 1 if user_data=='select_down' else -1
			autocomplete_item = current_autocomplete_item+inc
			if autocomplete_item>len(matches)-1:
				autocomplete_item = 0
			if autocomplete_item<0:
				autocomplete_item = len(matches)-1

			if dpg.does_alias_exist('grp_autocomplete_values'): dpg.delete_item('grp_autocomplete_values')
			entries = []
			with dpg.group(tag='grp_autocomplete_values', parent=win):
				for i, m in enumerate(matches):
					entry = dpg.add_text(m)
					entries.append(entry)
					if i==autocomplete_item:
						dpg.configure_item(dpg.last_item(), color=marked_item_color)
						current_autocomplete_text = m

			current_autocomplete_item = autocomplete_item
			dpg.show_item(win)
			dpg.split_frame()
			size = dpg.get_item_rect_size('grp_autocomplete_values')
			dpg.configure_item(win, height=size[1]+20)

	if evaluate and user_data == 'accept':
		dpg.set_value(field, current_autocomplete_text)
		current_autocomplete_item = -1
		current_autocomplete_text = ''
		dpg.hide_item(win)
		dpg.focus_item(field)

	if evaluate and user_data == 'cancel':
		dpg.set_value(field, current_text)
		current_autocomplete_item = -1
		current_autocomplete_text = ''
		dpg.hide_item(win)
		dpg.focus_item(field)

# listen for key press to activate autocomplete
with dpg.handler_registry():
    dpg.add_key_press_handler(key=dpg.mvKey_Down, callback=autocomplete, user_data='select_down')
    dpg.add_key_press_handler(key=dpg.mvKey_Up, callback=autocomplete, user_data='select_up')
    dpg.add_key_press_handler(key=dpg.mvKey_Return, callback=autocomplete, user_data='accept')
    dpg.add_key_press_handler(key=dpg.mvKey_Escape, callback=autocomplete, user_data='cancel')

# main UI
with dpg.window() as mainwin:
	with dpg.group(horizontal=True):
		dpg.add_text('Name')
		dpg.add_input_text(tag='name', callback=set_current_text)
	dpg.add_text('Type "j", then down/up arrow.\n(Enter to select, Esc to cancel)')

# init autocomplete window
dpg.add_child_window(tag='autocomplete_window', parent=mainwin, show=False, border=True, height=-1)

# focus text field on start
dpg.set_frame_callback(2, callback=lambda: dpg.focus_item('name'))

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window(mainwin, True)
dpg.start_dearpygui()
dpg.destroy_context()