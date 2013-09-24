import random

### DATA ###

data = { 
	"APPLE" : {
			"sentences" : 

				[

				{"string": "It is MOD DESC", "type": 0}, {"string": "This light is MOD DESC", "type": 0}, {"string": "Well, it's MOD DESC", "type": 0}, {"string": "Oh, how MOD DESC it is here.", "type": 0}, {"string": "I see that it is MOD DESC", "type": 0}, {"string": "MOD DESC now", "type": 0}, {"string": "Well, isn't it MOD DESC?", "type": 0}, {"string": "I am MOD DESC", "type": 1}, {"string": "Am I DESC?", "type": 2}, {"string": "Is it DESC?", "type": 3}, {"string": "Well now I'm MOD DESC", "type": 4}, {"string": "My skin is MOD DESC", "type": 4}, {"string": "I feel DESC me", "type": 5}, {"string": "There is DESC me once again", "type": 5}

				]

			, 

			"descriptors" : 

				[

				["light", 0, lambda m: m >= 0.5 and m <= 1.0], ["well-lit", 0, lambda m: m >= 0.5 and m <= 1.0], ["bright", 0, lambda m: m >= 0.7 and m <= 1.0], ["full of light", 0, lambda m: m >= 0.7 and m <= 1.0], ["sunny", 0, lambda m: m >= 0.5 and m <= 1.0], ["beaming", 0, lambda m: m >= 0.8 and m <= 1.0], ["dark", 0, lambda m: m >= 0.0 and m <= 0.5], ["subdued", 0, lambda m: m >= 0.0 and m <= 0.5], ["murky", 0, lambda m: m >= 0.0 and m <= 0.5], ["shadowy", 0, lambda m: m >= 0.0 and m <= 0.5], ["shady", 0, lambda m: m >= 0.0 and m <= 0.5], ["dusky", 0, lambda m: m >= 0.0 and m <= 0.5], ["dim", 0, lambda m: m >= 0.0 and m <= 0.5], ["crepuscular", 0, lambda m: m >= 0.0 and m <= 0.5], ["basking", 1, lambda m: m >= 0.5 and m <= 1.0], ["shaded", 1, lambda m: m >= 0.0 and m <= 0.5], ["ripening", 1, lambda m: m >= 0.5 and m <= 1.0], ["ripe", 2, lambda m: m >= 0.0 and m <= 1.0], ["night", 3, lambda m: m >= 0.0 and m <= 0.5], ["daytime", 3, lambda m: m >= 0.5 and m <= 1.0], ["bathed in light", 4, lambda m: m >= 0.5 and m <= 1.0], ["illuminated", 4, lambda m: m >= 0.6 and m <= 1.0], ["red", 4, lambda m: m >= 0.0 and m <= 1.0], ["cool and shaded", 4, lambda m: m >= 0.0 and m <= 0.5], ["light shining on", 5, lambda m: m >= 0.5 and m <= 1.0], ["brightness on", 5, lambda m: m >= 0.5 and m <= 1.0], ["shade on", 5, lambda m: m >= 0.5 and m <= 1.0], ["shadow falling on", 5, lambda m: m >= 0.0 and m <= 0.5], ["darkness on", 5, lambda m: m >= 0.0 and m <= 0.5]  

				]
			,
			"dreams" :

				[
				"I used to be quite small, but I am larger now.", "When I was green, there was much more firmness inside.", "The time I fell to the ground, there had been less light that day.", "I haven't noticed any bees in a while.", "There were big green leaves atop my crown.", "There were many more like me clustered on a branch.", "I have grown softer during the brightness."
				]

			  
	},
	"MUG" : {
			"sentences" : 

				[

				{"string": "It is MOD DESC", "type": 0}, {"string": "It is MOD DESC now, would you like some DRINK?", "type": 0}, {"string": "Oh, it's getting MOD DESC. Might be time for a cup of DRINK.", "type": 0}, {"string": "Aren't you MOD DESC now? Some DRINK might be a good idea.", "type": 0}, {"string": "Sure is MOD DESC. Why don't you pour youself a cup of DRINK?", "type": 0}, {"string": "A DRINK would be an excellent choice when it is MOD DESC like this.", "type": 0}, {"string": "DESC enough for you? You should consider some DRINK.", "type": 0}, {"string": "Perhaps you want to put some DRINK in me now that it is MOD DESC.", "type": 0}

				]

			, 

			"descriptors" : 

				[

				["warm", 0, lambda m: m >= 0.5 and m <= 1.0], ["balmy", 0, lambda m: m >= 0.5 and m <= 0.8], ["temperate", 0, lambda m: m >= 0.4 and m <= 0.6], ["cozy", 0, lambda m: m >= 0.5 and m <= 0.7], ["toasty", 0, lambda m: m >= 0.7 and m <= 1.0], ["hot", 0, lambda m: m >= 0.7 and m <= 1.0], ["sweltering", 0, lambda m: m >= 0.8 and m <= 1.0], ["cool", 0, lambda m: m >= 0.2 and m <= 0.5], ["cold", 0, lambda m: m >= 0.0 and m <= 0.3], ["chilly", 0, lambda m: m >= 0.0 and m <= 0.3], ["freezing", 0, lambda m: m >= 0.0 and m <= 0.3], ["brisk", 0, lambda m: m >= 0.2 and m <= 0.5], ["lukewarm", 0, lambda m: m >= 0.4 and m <= 0.6], ["mild", 0, lambda m: m >= 0.4 and m <= 0.6]

				]
			,
			"drinks" : 

				[

				["tea", lambda m: m >= 0.0 and m <= 0.5], ["coffee", lambda m: m >= 0.0 and m <= 0.5], ["cocoa", lambda m: m >= 0.0 and m <= 0.5], ["hot toddy", lambda m: m >= 0.0 and m <= 0.5], ["warm milk", lambda m: m >= 0.0 and m <= 0.5], ["hot cider", lambda m: m >= 0.0 and m <= 0.5], ["lemonade", lambda m: m >= 0.5 and m <= 1.0], ["fresh juice", lambda m: m >= 0.5 and m <= 1.0], ["water", lambda m: m >= 0.5 and m <= 1.0], ["iced tea", lambda m: m >= 0.5 and m <= 1.0], ["iced coffee", lambda m: m >= 0.5 and m <= 1.0], ["soda", lambda m: m >= 0.5 and m <= 1.0], ["seltzer", lambda m: m >= 0.5 and m <= 1.0], ["cold drink", lambda m: m >= 0.5 and m <= 1.0], ["hot or cold beverage", lambda m: m >= 0.4 and m <= 0.6], ["cold beer", lambda m: m >= 0.5 and m <= 1.0], ["cold beer", lambda m: m >= 0.5 and m <= 1.0]

				]
			,
			"dreams" :

				[
				"Sometimes I spin around and around and get very hot", "I once sat unused in darkness for a very long time", "There was a day when I was used 15 times. There were many cups of tea.", "When the spoon stirs, it clinks and clanks against my sides", "Ice dropped in makes liquid slosh around me"
				]
			  
	},
	"BLOCKS" : {
			"sentences" : 

				[

				{"string": "It is DESC", "type": 0}, {"string": "DESC here", "type": 1}, {"string": "DESC with us now", "type": 1}, {"string": "DESC present", "type": 1}, {"string": "DESC near", "type": 1}, {"string": "We see DESC", "type": 2}, {"string": "We see DESC has arrived", "type": 3}, {"string": "We see DESC is present", "type": 3}, {"string": "We see DESC has come", "type": 3}, {"string": "Oh, DESC now", "type": 4}, {"string": "Hello", "type": 5}, {"string": "Have you been here long?", "type": 5}, {"string": "Are you here to play with us?", "type": 5}, {"string": "Will we be one on top of the other again?", "type": 5}, {"string": "Will we be separated again?", "type": 5}

				]

			, 

			"descriptors" : 

				[

				["busy", 0, lambda m: m >= 0.5 and m <= 1.0], ["crowded", 0, lambda m: m >= 0.8 and m <= 1.0], ["packed", 0, lambda m: m >= 0.8 and m <= 1.0], ["teeming", 0, lambda m: m >= 0.8 and m <= 1.0], ["populated", 0, lambda m: m >= 0.5 and m <= 1.0], ["not empty", 0, lambda m: m >= 0.2 and m <= 1.0], ["empty", 0, lambda m: m >= 0.0 and m <= 0.3], ["idle", 0, lambda m: m >= 0.0 and m <= 0.2], ["clear of people", 0, lambda m: m >= 0.0 and m <= 0.2], ["devoid of people", 0, lambda m: m >= 0.0 and m <= 0.2], ["someone is", 1, lambda m: m >= 0.3 and m <= 1.0], ["people are", 1, lambda m: m >= 0.3 and m <= 1.0], ["a person is", 1, lambda m: m >= 0.3 and m <= 1.0], ["nobody is", 1, lambda m: m >= 0.0 and m <= 0.3], ["some people are", 0, lambda m: m >= 0.3 and m <= 1.0], ["few people are", 1, lambda m: m >= 0.0 and m <= 0.3], ["no one", 2, lambda m: m >= 0.0 and m <= 0.2], ["someone", 2, lambda m: m >= 0.2 and m <= 1.0], ["people", 2, lambda m: m >= 0.2 and m <= 1.0], ["you", 2, lambda m: m >= 0.2 and m <= 1.0], ["a group of people", 2, lambda m: m >= 0.4 and m <= 1.0], ["an assembly of people", 2, lambda m: m >= 0.4 and m <= 1.0], ["someone", 3, lambda m: m >= 0.3 and m <= 1.0], ["no one", 3, lambda m: m >= 0.0 and m <= 0.3], ["you are here", 4, lambda m: m >= 0.3 and m <= 1.0], ["we have company", 4, lambda m: m >= 0.3 and m <= 1.0], ["you have gone", 4, lambda m: m >= 0.0 and m <= 0.3], ["nobody is here", 4, lambda m: m >= 0.0 and m <= 0.3], ["", 5, lambda m: m >= 0.0 and m <= 1.0]

				]
			,
			"dreams" :

				[
				"We have seen many more people today than usual", "A long time ago, we sat next to one another in a container", "62 days ago, we were stacked unusually high", "Once, we moved around for a long time before we rested", "There used to be 26 of us", "Sometimes, nobody comes for a long time"
				]
			
	},
	"modifiers" :

				[

					["a tiny bit", lambda m: m >= 0.0 and m <= 0.2], ["a bit", lambda m: m >= 0.0 and m <= 0.5], ["a little", lambda m: m >= 0.0 and m <= 0.5], ["quite", lambda m: m >= 0.5 and m <= 1.0], ["very", lambda m: m >= 0.5 and m <= 1.0], ["extremely", lambda m: m >= 0.8 and m <= 1.0], ["fiercely", lambda m: m >= 0.8 and m <= 1.0], ["somewhat", lambda m: m >= 0.3 and m <= 0.6], ["fairly", lambda m: m >= 0.3 and m <= 0.6], ["rather", lambda m: m >= 0.5 and m <= 0.7]

				]
}


###  FUNCTION ###
def generate(obj, reading, diff, dream=False):
	print 'received %s %s %s %s' % (obj, reading, diff, dream)

	if reading < 0:
		reading = 0
	if reading > 1:
		reading = 1

	if dream==True:
		output = random.choice(data[obj]["dreams"])
		return output

	else:
		sentence = random.choice(data[obj]["sentences"])
		print sentence
		type = sentence["type"]
		descriptor = None
		modifier = ""
		print 'sentence is %s'%sentence

		while descriptor is None:
			d = random.choice(data[obj]["descriptors"])
			print 'd is %s'%d
			if d[1] == type: # this is never True; why? Answer, lambdas all had <, needed <= etc
				if d[2](reading):
					descriptor = d[0]

		if obj == "APPLE" or obj == "MUG":
			if random.random() >= 0.5:
				while modifier is "":
					m = random.choice(data["modifiers"])
					if m[1](reading):
						modifier = m[0]

		if obj == "MUG":
			drink = None
			while drink is None:
				d = random.choice(data[obj]["drinks"])
				if d[1](reading):
					drink = d[0]
			output = sentence["string"].replace("DESC", descriptor).replace("MOD", modifier).replace("DRINK", drink).lstrip()

		elif obj == "APPLE":
			output = sentence["string"].replace("DESC", descriptor).replace("MOD", modifier).lstrip()

		elif obj == "BLOCKS":
			if "DESC" in sentence["string"]:
				output = sentence["string"].replace("DESC", descriptor).lstrip()
			else:
				output = sentence["string"].lstrip()

		# print 'returning %s'%(output[0].upper() + output[1:])
		print 'readings: %s %s %s' % (reading, diff, dream)
		return output[0].upper() + output[1:]



### EXAMPLE ###

# sentence = generate("BLOCKS", random.random(), random.random())
# for i in range(100):
# 	sentence = generate("APPLE", random.random(), random.random(), False)
# 	print sentence
# 	print '\n'


