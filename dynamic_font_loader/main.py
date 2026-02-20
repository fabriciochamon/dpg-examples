import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Font viewer example', width=600, height=400)
dpg.add_font_registry(tag='font_reg')

current_font_name = None
available_font_sizes = [14, 50, 90]

# -- CALLBACKS -- #
def add_font(sender, app_data):
	global current_font_name, available_font_sizes

	# get font name and path
	font = app_data['file_path_name']
	font_name = app_data['file_name']
	current_font_name = font_name
	dpg.set_value('font_path', font)

	# add to font registry, in multiple sizes as in "available_font_sizes"
	added_fonts = []
	for size in available_font_sizes:
		font_tag = f'{font_name} : {size}'
		if not dpg.does_item_exist(font_tag):
			dpg.add_font(file=font, tag=font_tag, size=size, parent='font_reg')
		added_fonts.append(font_tag)

	# set sample text
	sample_text = dpg.get_value('sample_text')
	size_index = dpg.get_value('font_size')-1
	dpg.bind_item_font('sample_text_with_chosen_font', added_fonts[size_index])    
	dpg.set_value('sample_text_with_chosen_font', sample_text)

def change_font_size(sender, app_data):
	global current_font_name, available_font_sizes
	size = available_font_sizes[dpg.get_value('font_size')-1]
	font_tag = f'{current_font_name} : {size}'
	dpg.bind_item_font('sample_text_with_chosen_font', font_tag)
	dpg.set_value('size_value', f'{size} px')

def change_sample_text(sender, app_data):
	sample_text = dpg.get_value('sample_text')
	dpg.set_value('sample_text_with_chosen_font', sample_text)

# -- DPG LAYOUT -- #
with dpg.window(tag='main_window', label='Font viewer'):

	# create font chooser dialog as hidden
	with dpg.file_dialog(tag='font_dialog', label='Choose font', width=400, height=200, show=False, callback=add_font):
		dpg.add_file_extension("Font files (*.ttf *.otf}{.ttf,.otf}")
		
	# choose font file
	with dpg.group(horizontal=True):
		dpg.add_text('Font:')
		dpg.add_input_text(tag='font_path')    
		dpg.add_button(label='Choose...', callback=lambda:dpg.show_item('font_dialog'))

	# set font size
	with dpg.group(horizontal=True):
		dpg.add_text('Size:')
		dpg.add_slider_int(tag='font_size', default_value=int(len(available_font_sizes)/2), min_value=1, max_value=len(available_font_sizes), callback=change_font_size)
		dpg.add_text(f'{available_font_sizes[dpg.get_value("font_size")-1]} px', tag='size_value')
	
	# sample text to preview font
	dpg.add_separator()
	with dpg.group(horizontal=True):
		dpg.add_text('Sample text:')
		dpg.add_input_text(tag='sample_text', default_value='My Text!', callback=change_sample_text)
	dpg.add_text(tag='sample_text_with_chosen_font')

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('main_window', True)
dpg.start_dearpygui()
dpg.destroy_context()