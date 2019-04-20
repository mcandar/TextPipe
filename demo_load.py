import pandas as pd
from TextPipe import TextPipe

# import data
data = pd.read_csv("nytimes_leadparagraphs.csv",encoding="latin1")
data["Content"] = data["Content"].astype(str)
print(data["Content"].head())

# =============================================================================
# Create a TextPipe object, input data, and construct the pipeline
# =============================================================================
textnorm = TextPipe(documents = data["Content"],keys = data["Article_Id"])
a = textnorm.load('instructions')

# Execute the same procedure on another data
print(textnorm.pipeline(data["Content"][:20],
                        data["Article_Id"][:20]))