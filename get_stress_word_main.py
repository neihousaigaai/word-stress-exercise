from sys import argv
import get_stress_word_cambridge_dictionary
import get_stress_word_how_many_syllables_com
import get_stress_word_dictionary_com


def stress_on(word, word_type):
	res1 = get_stress_word_dictionary_com.stress_on(word, word_type)
	if res1 != -1 and res1 != 0:
		return res1

	res2 = get_stress_word_cambridge_dictionary.stress_on(word, word_type)
	if res2 != -1 and res2 != 0:
		return res2

	res3 = get_stress_word_how_many_syllables_com.stress_on(word)
	# print(word, res3)
	return res3


if __name__ == '__main__':
	# python get_stress_word_dictionary_com.py pronunciation_part1.txt

	with open(argv[1], 'r') as inp:
		lines = inp.readlines()
	
	for line in lines:
		solution = -2  # -2 is the initial state, -1 is no solution
		places = []
		val = [s.replace('\n', '').replace("'", "") for s in line.split('\t') if s != '']

		multicase = 0
		iter_multicase = (set(), 0)

		for i in range(1, len(val)):
			word = val[i][3:]

			if word.find('(') != -1:
				place = stress_on(word[:word.find('(')], word[word.find('(')+1:word.find(')')])
			else:
				place = stress_on(word, None)

			# print(word, place)
			places.append(place)

			'''
			if type(place) == type(set()):
				print('{}: too much stresses! {}'.format(word, place))
			elif place == -1:
				print(word + ': invalid word!')
			elif place == 0:
				print(word + ': one-syllable word!')
			else:
				if place % 10 == 1:
					print('{}: stress is on {}st syllable'.format(word, place))
				elif place % 10 == 2:
					print('{}: stress is on {}nd syllable'.format(word, place))
				elif place % 10 == 3:
					print('{}: stress is on {}rd syllable'.format(word, place))
				else:
					print('{}: stress is on {}th syllable'.format(word, place))
			'''

			if type(place) == type(set()):
				multicase += 1
				iter_multicase = (place, i)

			if place == -1 or place == 0:
				solution = -1
				break  # solution is -1
		
		if multicase > 1 or places.count(places[0]) == len(places):  # 2 cases
			solution = -1

		if solution == -2:  # haven't found the solution yet
			solution = -1

			_places = sorted([x for x in places if type(x) == type(0)])

			if _places.count(_places[0]) == len(_places):  # all items have equal stress
				if len(_places) != len(places):
					for u in iter_multicase[0]:
						if u != _places[0]:
							solution = iter_multicase[1]
							break

			elif _places.count(_places[0]) == 1:  # the first item is different from others
				if len(_places) == len(places):
					for i in range(len(places)):
						if _places.count(places[i]) == 1:
							solution = i+1
							break
				else:
					for u in iter_multicase[0]:
						if u == _places[1]:
							# find _places[0]
							for i in range(len(places)):
								if places[i] == _places[0]:
									solution = i+1
									break
							break

			elif _places.count(_places[-1]) == 1:  # the last item is different from others
				if len(_places) == len(places):
					for i in range(len(places)):
						if _places.count(places[i]) == 1:
							solution = i+1
							break
				else:
					for u in iter_multicase[0]:
						if u == _places[-2]:
							# find _places[-1]
							for i in range(len(places)):
								if places[i] == _places[-1]:
									solution = i+1
									break
							break

		if solution != -1:
			print(val[0], "DIFF:", val[solution])
		else:
			print(val[0], "NO SOLUTION")