def parseLen(text):
	L = []
	# add newlines to cause text to print properly
	# we need this because we're printing upside-down text
	# "call the police, it is faint-hearted" should be printed as
	# "rted" then linebreak then "Call the police, it is faint-hea"
	# which is "rted\nCall the police, it is faint-hea"

	if len(text) > 32: # 32 is defined by the printer; max chars per line
		r = len(text)%32
		L.append(text[-r:]+'\n')
		for i in reversed(range(len(text)/32)):
			L.append(text[i*32:(i+1)*32]+'\n')
	else:
		L.append(text)
	return L
