import dearpygui.dearpygui as dpg

# this module handles checked/unckecked buttons 
# in a global dict to store selections
items = {}

def toggle_off_all_items(name_prefix):
	index = 0
	while dpg.does_item_exist(f'{name_prefix}--{index}'):
		tag = f'{name_prefix}--{index}'
		dpg.bind_item_theme(tag, 'btn_unchecked_theme')
		index += 1

def set_item(sender, app_data, user_data):
	global items
	k = user_data[0]
	v = user_data[1]

	# handles multi-selection toogles
	if len(user_data) > 2 and user_data[2]:

		if k in items.keys():

			isOFF = v not in items[k]

			if isOFF:
				items[k].append(v)
				dpg.bind_item_theme(sender, 'btn_checked_theme')
			else:
				try:
					del items[k][items[k].index(v)]
				except:
					pass
				dpg.bind_item_theme(sender, 'btn_unchecked_theme')
		else:
			items[k] = [v]
			dpg.bind_item_theme(sender, 'btn_checked_theme')

	# handles single-selection toogles
	else:
		items[k] = v
		prefix = sender.split('--')[0]
		toggle_off_all_items(prefix)
		dpg.bind_item_theme(sender, 'btn_checked_theme')