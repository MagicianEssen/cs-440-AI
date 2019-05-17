# TextClassifier.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Dhruv Agarwal (dhruva2@illinois.edu) on 02/21/2019
import math
"""
You should only modify code within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
class TextClassifier(object):
    def __init__(self):
        """Implementation of Naive Bayes for multiclass classification

        :param lambda_mixture - (Extra Credit) This param controls the proportion of contribution of Bigram
        and Unigram model in the mixture model. Hard Code the value you find to be most suitable for your model
        """
        self.lambda_mixture = 0.0
        self.prior = []
        self.count =[]
        self.likelihood = []
        for i in range(14):
            self.prior.append(0)
            self.likelihood.append(dict())
            self.count.append(0)

    def fit(self, train_set, train_label):
        """
        :param train_set - List of list of words corresponding with each text
            example: suppose I had two emails 'i like pie' and 'i like cake' in my training set
            Then train_set := [['i','like','pie'], ['i','like','cake']]

        :param train_labels - List of labels corresponding with train_set
            example: Suppose I had two texts, first one was class 0 and second one was class 1.
            Then train_labels := [0,1]
        """

        # TODO: Write your code here
        #pass
        self.unique = dict()

        smooth = 1

        for data in range(len(train_set)):
            traindata = train_set[data]
            trainclass = train_label[data]-1
            self.prior[trainclass] += 1

            for word in traindata:
                if word in self.likelihood[trainclass]:
                    self.likelihood[trainclass][word] += 1
                    self.count[trainclass] += 1
                else:
                    self.likelihood[trainclass][word] = 1

                if word in self.unique:
                    self.unique[word] += 1
                else:
                    self.unique[word] = 1



        for i in range(14):
            self.prior[i] = math.log(self.prior[i]/len(train_set))



    def predict(self, x_set, dev_label,lambda_mix=0.0):
        """
        :param dev_set: List of list of words corresponding with each text in dev set that we are testing on
              It follows the same format as train_set
        :param dev_label : List of class labels corresponding to each text
        :param lambda_mix : Will be supplied the value you hard code for self.lambda_mixture if you attempt extra credit

        :return:
                accuracy(float): average accuracy value for dev dataset
                result (list) : predicted class for each text
        """

        accuracy = 0.0
        result = []
        numunique = len(self.unique)

        # TODO: Write your code here
        #pass
        for data in range(len(dev_label)):
            vallist=[]
            for i in range(len(self.prior)):
                totval=self.prior[i]
                temp = dict()
                for word in x_set[data]:
                    if(word not in temp):
                        if word in self.unique:
                            totval += math.log((self.likelihood[i].get(word, 0.0)+1)/(self.count[i] + numunique))
                            temp[word] = 0
                vallist.append(totval)

            predval=vallist.index(max(vallist))
            result.append(predval +1)
            if predval+1 == dev_label[data]:
                accuracy += 1
        accuracy=accuracy/len(x_set)

        return accuracy,result

