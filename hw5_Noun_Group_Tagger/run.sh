javac -cp maxent-3.0.0.jar:trove.jar *.java ### compiling
java -cp .:maxent-3.0.0.jar:trove.jar MEtrain training.feature model.chunk ### creating the model of the training data
java -cp .:maxent-3.0.0.jar:trove.jar MEtag test.feature model.chunk response.chunk ### creating the system output