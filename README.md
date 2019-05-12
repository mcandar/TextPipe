# TextPipe

## Introduction
**TextPipe is a project for textual data preprocessing, cleaning and manipulating.** It lets you to **create pipelines** with any kind of function to apply on documents. It sequentially executes all the functions added to it. This pipeline could be **saved and loaded** to use with other datasets.

**Best possible use cases:**
- When you are using the same procedure multiple times
- When you have several set of functions to apply on different datasets
- When you want to transfer the procedure to anyone else
- When you want tidier code

**Advantages:**
- Simple
- Lightweight
- No significant dependency
- Readability
- No syntax to learn!

## Installation
Clone this repository with following:

`git clone`

## Requirements
Only dill, if you want to save and load your pipelines. Install with:

`pip install dill`

## Verification
After installation, head to the directory and run:

`$ python demo_pipe.py`

## Basic Guideline
Here are some several walkthroughs. First, import `TextPipe`, read data and create a `TextPipe` object.

```
from TextPipe import TextPipe
data = pd.read_csv("nytimes_leadparagraphs.csv",encoding="latin1")
textnorm = TextPipe(documents = data["Content"],keys = data["Article_Id"])
```

Note that only two arguments needed; documents itself and their identifier keys. Now specify the functions you want to apply on the dataset to create a pipeline:

```
textnorm.apply_docs(lambda x: punc.sub(" ",x).lower().split(" ")) # remove punc, lowercase, split into list
textnorm.apply_words(lambda x: x if x is not None and len(x) > 2 else None) # remove short words
textnorm.apply_docs(lambda x: x if len(x) >= 5 else None) # remove short docs
textnorm.filter_none() # remove Nones
```

That's it, the pipeline is created! Check with:

```
print(textnorm.ops) # applied instructions
print(textnorm.ops_target) # applied data
```

Apply on any kind of textual data:

```
print(textnorm.pipeline(data["Content"][:20],data["Article_Id"][:20]))
```

Bonus: you can save this pipeline to apply later on:

```
textnorm.save('instructions')
```

Check demos for further information, [demo_pipe.py](https://github.com/mcandar/TextPipe/blob/master/demo_pipe.py), [demo_save.py](https://github.com/mcandar/TextPipe/blob/master/demo_save.py), [demo_load.py](https://github.com/mcandar/TextPipe/blob/master/demo_load.py).


## License
[MIT License](https://github.com/mcandar/TextPipe/blob/master/LICENSE)
