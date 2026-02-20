import sys, time

ntasks = 35
for i in range(ntasks):
	sys.stdout.write(f'status: executing task {i+1} of {ntasks}, {int((i+1)/ntasks*100)}% done.\n')
	sys.stdout.flush() 
	time.sleep(0.1)