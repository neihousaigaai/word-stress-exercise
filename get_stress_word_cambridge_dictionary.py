import urllib.request
from sys import argv


def stress_on(word, _type):
	link = "http://dictionary.cambridge.org/dictionary/english/" + word

	try:
		f = urllib.request.urlopen(link)
	except:
		return -1  # not exist

	info = [x.decode() for x in f.readlines()]

	syllable_data = ''
	found_type = ''

	tmp = '<h3 class="di-title cdo-section-title-hw"><span class="headword"><span class="hw">'+word+'</span></span><span class="posgram ico-bg"><span class="pos" '

	word_types = [
		('verb', tmp + 'title="A word that describes an action, condition or experience.">verb</span>'),
		('adjective', tmp + 'title="A word that describes a noun or pronoun.">adjective</span>'),
		('noun', tmp + 'title="A word that refers to a person, place, idea, event or thing.">noun</span>'),
		('adverb', tmp + 'title="A word that gives information about a verb, adjective, another adverb, or a sentence.">adverb</span>'),
		('pronoun', tmp + 'title="A word such as it, or mine used to replace a noun.">pronoun</span>'),
		('preposition', tmp + 'title="A word that is used before a noun, a noun phrase, or a pronoun, connecting it to another word.">preposition</span>'),
		('conjunction', tmp + 'title="A word such as and or although used to link two parts of a sentence.">conjunction</span>'),
	]

	type_line_found = -1

	if _type != None:
		if _type == 'v':
			found_type = 'verb'
			st = word_types[0][1]
		elif _type == 'adj':
			found_type = 'adjective'
			st = word_types[1][1]
		elif _type == 'n':
			found_type = 'noun'
			st = word_types[2][1]
		elif _type == 'adv':
			found_type = 'adverb'
			st = word_types[3][1]
		elif _type == 'pron':
			found_type = 'pronoun'
			st = word_types[4][1]
		elif _type == 'prep':
			found_type = 'preposition'
			st = word_types[5][1]
		elif _type == 'conj':
			found_type = 'conjunction'
			st = word_types[6][1]

		for i in range(len(info)):
			s = info[i]
			if s.find(st) != -1:
				type_line_found = i
				break
	else:
		for i in range(len(info)):
			s = info[i]
			for word_type, st in word_types:
				if s.find(st) != -1:
					found_type = word_type
					type_line_found = i
					break

			if type_line_found != -1:
				break

	ipa = ''

	for i in range(type_line_found+1, len(info)):
		s = info[i].replace('\t', '')
		jj = -1
		for j in range(len(s)):
			if s[j] != ' ':
				jj = j
				break

		s = s[jj:]
		if s.startswith('</span><span class="uk"><span class="pron">/<span class="ipa">'):
			ipa = s[62:s.find('</span>/</span></span>  ')]

			ipa = ipa.replace('ˈ', '.ˈ')
			ipa = ipa.replace('ˌ', '.ˌ')
			
			while ipa.find('..') != -1:
				ipa = ipa.replace('..', '.')

			break

	syllables = [x for x in ipa.split('.') if x != '']
	stress_list = set()

	for i in range(len(syllables)):
		syllable = syllables[i]
		if syllable.startswith('ˈ'):
			stress_list.add(i+1)

	# print(ipa, stress_list)

	if len(stress_list) == 1:
		return stress_list.pop()
	elif len(stress_list) > 1:
		return stress_list  # too much solutions
	else:
		return 0  # no solution
