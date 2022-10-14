# Noun Group Tagger
Create a program that takes a file like WSJ_02-21.pos-chunk as input and produces a file consisting of feature value pairs for use with the maxent trainer and classifier. As this step represents the bulk of the assignment, there will be more details below, including the format information, etc. This program should create two output files. From the training corpus (WSJ_02-21.pos-chunk), create a training feature file (training.feature). From the development corpus (WSJ_24.pos), create a test feature file (test.feature).

## Usage
Run script with dev/test
``` bash
python3 hw5.py dev
# or
python3 hw5.py test
```

Run model
``` bash
javac -cp maxent-3.0.0.jar:trove.jar *.java ### compiling
java -cp .:maxent-3.0.0.jar:trove.jar MEtrain training.feature model.chunk ### creating the model of the training data
java -cp .:maxent-3.0.0.jar:trove.jar MEtag test.feature model.chunk response.chunk ### creating the system output
```

Score
``` bash
python3 score.chunk.py WSJ_24.pos-chunk response.chunk
```

## My work
1. Follow the instructions to implement program which takes two inputs and generates two outputs (training and test)
2. Features added:
   1. word itself
   2. offset of word in the sentence
   3. POS
   4. is lowercase
   5. previous word
   6. POS of previous word
   7. is previous word lowercase
   8. previous BIO
   9. following word
   10. POS of following word
   11. is following word lowercase
   12. same as 2 words forwards and 2 words back

