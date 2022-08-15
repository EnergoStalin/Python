from datetime import timedelta
from itertools import permutations
import logging
import multiprocessing
import timeit

def solve_old(fn):
	data = map(int, open(fn , "r").readlines()[1::])
	mx = 0
	pool = multiprocessing.Pool(4)
	for n in permutations(data, r=2):
		s = sum(n)
		if not(s % 3):
			mx = max(mx, s)
		
	return mx

def solve(fn):
	data = map(int, open(fn , "r").readlines()[1::])
	mx = 0
	pool = multiprocessing.Pool(4)
	for m in pool.imap_unordered(s_worker, permutations(data, r=2), 1000):
		mx = max(mx, m)
		
	return mx

def s_worker(n):
	s = sum(n)
	return 0 if s % 3 else s

def main():
	#print(solve("./10263058/28128_A.txt"))
	logging.basicConfig(filename="27.log", filemode="w", format="[%(asctime)s] %(message)s", level=logging.INFO)
	seconds = timeit.timeit(stmt=lambda: logging.info("solve() result: " + str(solve("./10263058/28128_B.txt"))), number=3)
	logging.info("solve() " + str(timedelta(seconds=seconds)))
	seconds = timeit.timeit(stmt=lambda: logging.info("solve_old() result: " + str(solve_old("./10263058/28128_B.txt"))), number=3)
	logging.info("solve_old() " + str(timedelta(seconds=seconds)))

if __name__ == "__main__":
	main()
	