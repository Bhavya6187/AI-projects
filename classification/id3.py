import util
import classificationMethod
import math
import pdb

class id3Classifier(classificationMethod.ClassificationMethod):

   def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "id3"
    self.tree = {};
    self.counts = {};
    self.attribute = {};
    for label in self.legalLabels:
      self.counts[label]=0;\

    self.condCounts = util.Counter();
    self.treeIter = 0


   def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    self.trainingData = trainingData;
    self.trainingLabels = trainingLabels;
    self.attribute = trainingData[0].keys();
    self.tree = self.make_tree(trainingData)
    
   def entropy(self, trainingData):

     entropy = 0
     counts = {}
     for label in self.legalLabels:
      counts[label]=0
     c = 0
     maxC = 0;
     for i in range (0,len(self.trainingLabels)):
       if trainingData[i] != None:  
         counts[self.trainingLabels[i]] += 1.0
         c+=1
     for label in self.legalLabels:
       if c == 0 or counts[label] == 0:
         continue
       entropy += (-1*counts[label]/(1.0*c) )* math.log( counts[label] / (1.0*c) ) 
       if counts[label] > 0:
         maxC = label

     return entropy, maxC


   def chooseBest(self,trainingData):
    
    #print len(trainingLabels)
    finalAttr = (-1, -1)
    self.condCounts = util.Counter();
    empty = False;
    trainingLabels = self.trainingLabels;
    for i in range (0,len(trainingLabels)):
      self.counts[trainingLabels[i]] += 1.0
      if trainingData[i] != None:  
        empty = True;
        for data in trainingData[i].keys():
          #print data, trainingData[i][data]
          if trainingData[i][data] == None:
            continue;
          if trainingData[i][data] ==0:
            self.condCounts[(data,0,trainingLabels[i])] +=1.0 
          else:
            self.condCounts[(data,1,trainingLabels[i])] +=1.0
#    print len(self.condCounts)
#    print self.condCounts
#    print tdata[0].keys()
    mingainFactor= -float("inf")
    chkdAttr = {}
    for data in self.attribute:
      attTrue = 0
      attFalse = 0
      gf1 = 0
      gf2 =0
      for label in self.legalLabels:
        attTrue += self.condCounts[(data, 1, label)]
        attFalse += self.condCounts[(data, 0, label)]

      for label in self.legalLabels:
        if attTrue != 0:
          if (self.condCounts[(data, 1, label)]) != 0:
            gf1 += (self.condCounts[(data, 1, label)]) * math.log( (self.condCounts[(data, 1, label)]) /  (1.0*attTrue) ) / (1.0*attTrue)
        if attFalse != 0:
          if (self.condCounts[(data, 0, label)]) != 0:
            gf2 += (self.condCounts[(data, 0, label)]) * math.log( (self.condCounts[(data, 0, label)]) /  (1.0*attFalse) ) / (1.0*attFalse)
      
      if attTrue + attFalse == 0:
        continue
      gainFactor = (attTrue*gf1 + attFalse*gf2) / (1.0*(attTrue + attFalse))
      if mingainFactor < gainFactor :
        mingainFactor = gainFactor
        finalAttr = data
      #print 'attr = ', data, attTrue, attFalse,  '  gain =', gainFactor, ' ', mingainFactor
      
#    print 'min gain =', mingainFactor
    return finalAttr

   	

   def make_tree(self, tdata):
    
    trainingLabels=self.trainingLabels;
    count0 = 0;
    count1 = 0;
    tdata0 = [];
    tdata1 = [];
    tree = {};
    self.treeIter +=1
    print self.treeIter 
    [entropy, maxC] = self.entropy(tdata)
    if entropy == 0:
      print 'entropy zero reached', maxC 
      return maxC
    
    best = self.chooseBest(tdata);
    print best
    
    #pdb.set_trace()
    for i in  range(0,len(trainingLabels)):
      if tdata[i] == None:
        tdata0.insert(i,None);
        tdata1.insert(i,None);
        continue;
      if tdata[i][best] == 0:
        tdata0.insert(i, (tdata[i]));
        tdata0[i][best]=None;
        tdata1.insert(i, None);
        count0+=1;
      else:
        tdata1.insert(i, tdata[i]);
        tdata1[i][best]=None;
        tdata0.insert(i, None);
        count1+=1;

    tree = {best:{}}
    tree[best][0] = self.make_tree(tdata0);
    print tree
    tree[best][1] = self.make_tree(tdata1);
    print tree
    return tree;
