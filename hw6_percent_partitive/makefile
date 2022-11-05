JAVA = java
JAVAC = javac
JAVA_PATH = maxent
PY = python3
JFLAGS=-Xmx16g -cp
TASK?=percent
TYPE?=dev

compile:
	$(JAVAC) -cp $(JAVA_PATH)/maxent-3.0.0.jar:$(JAVA_PATH)/trove.jar $(JAVA_PATH)/*.java

run: 
	$(PY) hw5.py $(TYPE) $(TASK)
	$(JAVA) $(JFLAGS) $(JAVA_PATH)/.:$(JAVA_PATH)/maxent-3.0.0.jar:$(JAVA_PATH)/trove.jar MEtrain training.feature model.chunk
	$(JAVA) $(JFLAGS) $(JAVA_PATH)/.:$(JAVA_PATH)/maxent-3.0.0.jar:$(JAVA_PATH)/trove.jar MEtag test.feature model.chunk $(TASK)_$(TYPE).txt

score:
    ifeq  ($(TASK), percent)
		$(PY) score.py data/%_nombank.clean.dev $(TASK)_$(TYPE).txt
    else
		$(PY) score.py data/partitive_group_nombank.clean.dev $(TASK)_$(TYPE).txt
    endif

submit: 
	@cp percent_test.txt percent.txt
	@cp partitive_test.txt partitive.txt

# clean:
# 	rm -f $(JAVA_PATH)/*.class
