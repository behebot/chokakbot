#!/usr/bin/python

from fuzzywuzzy import process

choices = ["what time is it", "tell me the time", "how much watch"]

phrases = ["how much watch", "tell me time please", "time please",
           "good weather, isn't it?", "what time is it now?"]

for i in phrases:
    print i
    print process.extractOne(i, choices, score_cutoff=75)
