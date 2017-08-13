import urllib.request
from sys import argv
import get_stress_word_cambridge_dictionary
import get_stress_word_how_many_syllables_com


def stress_on(word, word_type):
	link = "http://www.dictionary.com/browse/" + word

	try:
		f = urllib.request.urlopen(link)
	except:
		return -1  # not exist

	info = [x.decode() for x in f.readlines()]

	syllable_data = ''
	for i in range(len(info)):
		u = info[i]
		jj = -1

		for j in range(len(u)):
			if u[j] != ' ':
				jj = j
				break

		u = u[jj:]

		if u.startswith('<span class="pron ipapron">/'):
			u = u.replace('ˈ', ' ˈ')
			u = u.replace('ˌ', ' ˌ')
			
			while u.find('  ') != -1:
				u = u.replace('  ', ' ')

			u = u.replace("dbox-bold", "dbox_bold")
			u = u.replace("dbox-italic", "dbox_italic")
			syllable_data = u[u.find('<span class="pron ipapron">/')+28:u.find('/ </span>')]

			jj = -1
			for j in range(len(syllable_data)):
				if syllable_data[j] != ' ':
					jj = j
					break

			syllable_data = syllable_data[jj:]

			break

	types = syllable_data.split('; ')
	# print(word, types)

	real_type = ''
	if len(types) == 1:
		syllable_data = types[0]

	elif word_type == None:
		syllable_data = ''
		for case in types:
			if case.startswith('<span class="dbox_italic">'):
				syllable_data += case[case.find('</span>')+8:] + ', '

	else:
		if word_type == 'v':
			real_type = 'verb'
		elif word_type == 'adj':
			real_type = 'adjective'
		elif word_type == 'n':
			real_type = 'noun'
		elif word_type == 'adv':
			real_type = 'adverb'
		elif word_type == 'pron':
			real_type = 'pronoun'
		elif word_type == 'prep':
			real_type = 'preposition'
		elif word_type == 'conj':
			real_type = 'conjunction'

		for case in types:
			if case.find('>'+real_type+'</span> ') != -1:
				syllable_data = syllable_data[case.find('>'+real_type+'</span> ')+len('>'+real_type+'</span> '):]
				break

	# print(word, syllable_data, syllable_data.count('ˈ'))

	for ch in range(48, 57+1):
		if chr(ch) in syllable_data:  # found some stupid cases with numbers
			return 0

	sub_cases = syllable_data.split(', ')
	sub_cases = [x for x in sub_cases if x != '' and x[-1] != '-' and x[0] != '-' and x.count('ˈ') == 1]

	if syllable_data == '' or len(sub_cases) == 0:  # some stupid words...
		return 0

	stress_list = set()

	for sub_case in sub_cases:
		syllables = sub_case.split(' ')

		for i in range(len(syllables)):
			syllable = syllables[i]
			if syllable.startswith('ˈ'):
				stress_list.add(i+1)

	if len(stress_list) == 1:
		return stress_list.pop()
	elif len(stress_list) > 1:
		return stress_list  # too much solutions
	else:
		return 0  # no solution
