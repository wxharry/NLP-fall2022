# percent and partitive

## Usage
Run script with file_type[dev/test] task_type[percent/partitive]
``` bash
python3 hw6.py file_type task_type
```

Run model
I found it easy to simply use the maxent model used for hw5
``` bash
make run TASK=task_type TYPE=file_type
```

Score
``` bash
make score TASK=task_type
```

## My work
1. Follow the instructions to implement program which takes two inputs and generates two outputs (training and test)
2. Features added:
   1. word itself
   1. offset of word in the sentence
   1. POS
   1. BIO
   1. capitalization
   1. previous word
   1. POS of previous word
   1. BIO of previous word
   1. previous word capitalization
   1. previous tagging
   1. following word
   1. POS of following word
   1. BIO of following word
   1. following word capitalization
   1. same as 3 words forwards and 3 words back
   1. word, POS, and BIO for 4 words forwards and 4 words back

