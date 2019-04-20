import re
import pandas as pd
from nltk.corpus import stopwords
from collections import defaultdict
from TextPipe import TextPipe

# import data
data = pd.read_csv("nytimes_leadparagraphs.csv",encoding="latin1")
data["Content"] = data["Content"].astype(str)
print(data["Content"].head())

# init variables
punc = re.compile("[^\w\s]+") # remove punctuations
reg  = re.compile("\S*\d+\S*") # words with numbers
bl   = frozenset(["politics","president","rumor"]) # (random) blacklist
sw   = frozenset(stopwords.words("english")) # download this if does not exists, use nltk.download()

# =============================================================================
# Create a TextPipe object, input data, and construct the pipeline
# =============================================================================
textnorm = TextPipe(documents = data["Content"],keys = data["Article_Id"])
textnorm.apply_docs(lambda x: punc.sub(" ",x).lower().split(" ")) # remove punc, lowercase, split into list
textnorm.apply_words(lambda x: x if len(reg.findall(x)) == 0 else None) # remove words with numbers
textnorm.apply_words(lambda x: x if x is not None and len(x) > 2 else None) # remove short words
textnorm.apply_words(lambda x: None if x in sw or x in bl else x) # None stopwords and blacklisted words
textnorm.apply_docs(lambda x: x if len(x) >= 5 else None) # remove short docs
textnorm.apply_docs(lambda x: None if x in [""," "] else x) # None unnecessary chars
textnorm.filter_none() # remove Nones
textnorm.apply_docs(lambda x: " ".join(x))

# See results
print(textnorm.documents) # processed docs
print(textnorm.ops) # applied instructions
print(textnorm.ops_target) # applied data

textnorm.save('instructions',external_vars={'punc':punc,'reg':reg,'bl':bl,'sw':sw})