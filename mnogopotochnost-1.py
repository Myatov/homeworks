# from threading import Thread, Lock

# lock = Lock()


# def worker1():
# 	with lock: # блокировка
# 		for i in range(100):
# 			print ('Thread1 working')

# thread1 = Thread(target=worker1)
# thread1.start()

# def worker2():
# 	with lock:
# 		for i in range (100):
# 			print ('22222')

# thread2 = Thread(target=worker2)
# thread2.start()


# 2й вариант реализации - через очередь

from concurrent.futures import ThreadPoolExecutor

def work1():
	for i in range(10):
		print (f'Thread 111 is working {i}')

def work2():
	for i in range(10):
		print (f'Thread 222 is working {i}')

executor = ThreadPoolExecutor (max_workers = 10)
executor.submit(work1) # запустили 1й поток
executor.submit(work2) # запустили 2й поток

for i in range (20, 30): # запустили 3й поток
	print (i)