import dearpygui.dearpygui as dpg
from pprint import pformat
import selectables

dpg.create_context()
dpg.create_viewport(title='Buttons as selectables', width=600, height=300)

# themes for checked/unhecked buttons
with dpg.theme(tag='btn_unchecked_theme'):
	with dpg.theme_component(dpg.mvAll):
		dpg.add_theme_color(dpg.mvThemeCol_Button, (55, 83, 125))
		dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (104, 127, 161))
		dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (250, 209, 5))
with dpg.theme(tag='btn_checked_theme'):
	with dpg.theme_component(dpg.mvAll):
		dpg.add_theme_color(dpg.mvThemeCol_Button, (232, 148, 14))
		dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (250, 209, 5))
		dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (250, 209, 5))
		dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0))

# callback
def show_selected_items():
	global selectables

	# selectables.py has a global variable "items", that stores all single/multi selections in a dict
	dpg.set_value('items_info', pformat(selectables.items))

# UI
with dpg.window() as mainwin:

	# single selection button group
	with dpg.group(horizontal=True):
		allow_multi_selection = False
		people = [
			{'name': 'Paul', 'age': 55, 'country': 'England'},
			{'name': 'Rose', 'age': 37, 'country': 'US'},
			{'name': 'Julia', 'age': 22, 'country': 'Denmark'}
		]
		dpg.add_text('Single selection:')
		for i, person in enumerate(people):
			# IMPORTANT: 
			#    tag needs to be in this specific format: "btn_group_identifier--index"
			#    user_data needs to be in this specific format: [btn_group_identifier, data_to_be_stored, allow_multi_selection_for_group]
			btn_group = 'people'
			tag = f'{btn_group}--{i}' 
			dpg.add_button(tag=tag, label=person['name'], user_data=[btn_group, person, allow_multi_selection], callback=selectables.set_item)
			dpg.bind_item_theme(dpg.last_item(), 'btn_unchecked_theme')
		
	# multi selection button group
	with dpg.group(horizontal=True):
		allow_multi_selection = True
		cars = [
			{'brand': 'Mercedes-Benz', 'year': 2022},
			{'brand': 'BMW', 'year': 2026},
			{'brand': 'General Motors', 'year': 2023}
		]
		dpg.add_text('Multi selection:')
		for i, car in enumerate(cars):
			# IMPORTANT: 
			#    tag needs to be in this specific format: "btn_group_identifier--index"
			#    user_data needs to be in this specific format: [btn_group_identifier, data_to_be_stored, allow_multi_selection_for_group]
			btn_group = 'cars'
			tag = f'{btn_group}--{i}' 
			dpg.add_button(tag=tag, label=car['brand'], user_data=[btn_group, car, allow_multi_selection], callback=selectables.set_item)
			dpg.bind_item_theme(dpg.last_item(), 'btn_unchecked_theme')
	
	# show stored selections
	dpg.add_separator()
	dpg.add_button(label='Show selected items', callback=show_selected_items)
	dpg.add_input_text(tag='items_info', width=-1, height=-1, multiline=True)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window(mainwin, True)
dpg.start_dearpygui()
dpg.destroy_context()