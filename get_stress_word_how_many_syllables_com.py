import urllib.request
from sys import argv


def stress_on(word):
	link = "https://www.howmanysyllables.com/words/" + word

	try:
		f = urllib.request.urlopen(link)
	except:
		return -1  # not exist
	
	info = (f.read()).decode()

	if info.find("Syllable stress:") != -1:  # check if 'word' is a one-syllable word
		return 0

	stress_id = info.find("Stressed syllable in <i>")  # word with a stress
	primary_id = info.find("Primary syllable stress")  # word with >= 2 stresses. Use primary stress only

	if stress_id != -1:
		syllable_data = info[stress_id:]
	elif primary_id != -1:
		secondary_id = info.find("Secondary syllable stress")
		syllable_data = info[primary_id:secondary_id]
	else:
		return 0

	syllables_begin = syllable_data.find('<span class="no_b">')+len('<span class="no_b">')
	syllables_tmp = syllables_begin+syllable_data[syllables_begin:].find('</span>')+len('</span>')
	syllables_end = syllables_tmp+syllable_data[syllables_tmp:].find('</span>')
	
	syllable_data = syllable_data[syllables_begin:syllables_end]

	syllables = syllable_data.split('-')

	for i in range(len(syllables)):
		syllable = syllables[i]
		if syllable.startswith('<span class="Ans_st"'):
			return i+1

	return 0
