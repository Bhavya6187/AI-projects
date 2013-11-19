
import util
import classificationMethod
import math

class id3Classifier(classificationMethod.ClassificationMethod):

   def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **
    self.counts = {}
    for label in self.legalLabels:
      self.counts[label]=0;
    self.condCounts = util.Counter()
    self.Probs = util.Counter()
    self.condProbs = util.Counter()

   def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    # might be useful in your code later...
    # this is a list of all features in the training set.
    self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));
    
    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels)

   def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter 
    that gives the best accuracy on the held-out validationData.
    
    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """
    condCounts = {} 
    for i in range (0,len(trainingLabels)):
      print trainingLabels[i];
#      for data in trainingData[i].keys():
#        if trainingData[i][data] ==1:
#          print data," ->>  ",trainingData[i][data]
    util.raiseNotDefined();

 
