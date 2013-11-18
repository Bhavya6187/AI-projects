# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
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

    
  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    # might be useful in your code later...
    # this is a list of all features in the training set.
    self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));
    
    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
    else:
        kgrid = [self.k]
        
    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)
      
  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
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
      self.counts[trainingLabels[i]] += 1.0
      for data in trainingData[i].keys():
        if trainingData[i][data] ==0:
          self.condCounts[(data,0,trainingLabels[i])] +=1.0 
        else:
          self.condCounts[(data,1,trainingLabels[i])] +=1.0
      #print self.condCounts

    maxProb = 0.0
    for k in kgrid:
      for label in self.legalLabels:
        for feature in trainingData[i].keys():
          condsum = self.condCounts[(feature,0, label)] + self.condCounts[(feature,1,label)]
          self.condProbs[(feature,0, label)] =  (self.condCounts[(feature,0, label)] + 1.0*self.k )/(condsum + 1.0*self.k)
          self.condProbs[(feature,1, label)] =  (self.condCounts[(feature,1, label)] + 1.0*self.k )/(condsum + 1.0*self.k)
        
        self.Probs[label] = self.counts[label]/(1.0*len(trainingLabels))
        #print self.Probs[label]
        #print self.counts[label]
      guesses = []
      guesses = self.classify(validationData)
      correctV = 0.0;
      for i in range(0,len(validationLabels)) :
        if guesses[i] == validationLabels[i] :
          correctV += 1.0
      #print guesses, validationLabels
      currentProb = correctV / (1.0*len(validationLabels))
      print 'checking ', currentProb
      if maxProb < currentProb:
        maxProb = currentProb
        self.k = k
    print 'k=' , self.k
    return self.k

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()
        
  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.
    
    You shouldn't modify this method.
    """
    print 'k=', self.k
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior.argMax())
      self.posteriors.append(posterior)
    return guesses
      
  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.    
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """
    #print "in calculateLogJointProbabilities"
    #print len(self.features)
    #print self.legalLabels
    logJoint = util.Counter()
    for label in self.legalLabels:
      #print self.Probs[label]
      logJoint[label] = math.log(self.Probs[label])
      for data in datum.keys():
        if datum[data] == 0:
          logJoint[label] += math.log(self.condProbs[(data,0,label)])
        else:
          logJoint[label] += math.log(self.condProbs[(data,1,label)])
    return logJoint
 
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()
    
  
  def findHighOddsFeatures(self, label1, label2):
    """
    Returns the 100 best features for the odds ratio:
            P(feature=1 | label1)/P(feature=1 | label2) 
    
    Note: you may find 'self.features' a useful way to loop through all possible features
    """
    featuresOdds = []
       
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

    return featuresOdds
    

    
      
