import dearpygui.dearpygui as dpg
import subprocess, re

# -- CALLBACKS -- #
def toogle_log_autoscroll(sender, value):
	dpg.configure_item('log', tracked=value)

def clear_log():
	dpg.set_value('log', '')
	resize_log()

def append_log(content):
	dpg.set_value('log', dpg.get_value('log')+str(content))
	resize_log()

def resize_log():
	content = dpg.get_value('log')
	dpg.set_item_height('log', dpg.get_text_size(content)[1]+20)

def update_progress(content):
	# uses regex to extract data from stdout
	pattern = re.compile(r'.* (\d+) of (\d+), (\d+).*')
	match = pattern.match(content)

	if match:
		curr_task = int(match.groups()[0])
		num_tasks = int(match.groups()[1])
		progress  = int(match.groups()[2])
		progress_normalized = progress/100 # value for dpg progressbar
		dpg.set_value('progress', progress_normalized)
		dpg.configure_item('progress', overlay=f'{progress}% ({curr_task} of {num_tasks})')

def run_dummy_program():
	clear_log()
	cmd = f'python dummy_program.py'
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
	process_started(proc)
	for line in proc.stdout:
		append_log(line)
		update_progress(line)
	proc.wait()
	process_finished(proc)

def process_started(process):
	append_log(f'PROCESS STARTED: {process.args}\n\n')

def process_finished(process):
	append_log(f'\nPROCESS FINISHED: return code {process.returncode}')

# -- DPG LAYOUT -- #
dpg.create_context()
dpg.create_viewport(title='Log with progress bar example', width=600, height=400)

with dpg.window() as main_window:

	# buttons
	with dpg.group(horizontal=True):
		dpg.add_button(label='Run command', callback=run_dummy_program)
		dpg.add_button(label='Clear log', callback=clear_log)
		dpg.add_spacer(width=20)
		dpg.add_checkbox(tag='autoscroll', label='autoscroll log', default_value=True, callback=toogle_log_autoscroll)

	# log (inside a child window, so we can use the "tracked" feature to autoscroll)
	with dpg.child_window(tag='log_window', width=-1, height=-50, border=False):
		dpg.add_input_text(tag='log', multiline=True, readonly=True, width=-1, height=-1, tracked=True, track_offset=1)

	# progress bar
	with dpg.group(horizontal=True):
		dpg.add_text('Progress:')
		dpg.add_progress_bar(tag='progress', width=-1)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window(main_window, True)
dpg.start_dearpygui()
dpg.destroy_context()