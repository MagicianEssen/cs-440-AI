import numpy as np

class MultiClassPerceptron(object):
	def __init__(self,num_class,feature_dim):
		"""Initialize a multi class perceptron model. 

		This function will initialize a feature_dim weight vector,
		for each class. 

		The LAST index of feature_dim is assumed to be the bias term,
			self.w[:,0] = [w1,w2,w3...,BIAS] 
			where wi corresponds to each feature dimension,
			0 corresponds to class 0.  

		Args:
		    num_class(int): number of classes to classify
		    feature_dim(int): feature dimension for each example 
		"""

		self.w = np.zeros((feature_dim+1,num_class))

	def train(self,train_set,train_label):
		""" Train perceptron model (self.w) with training dataset. 

		Args:
		    train_set(numpy.ndarray): training examples with a dimension of (# of examples, feature_dim)
		    train_label(numpy.ndarray): training labels with a dimension of (# of examples, )
		"""

		# YOUR CODE HERE
		#last index of w be bias term
		x = self.w.shape[0]-1
		for i in range(self.w.shape[1]):
			self.w[x,i] = 1

		bias = 1
		learnrate = 1
		epoch = 1

		for ep in range(epoch):
			for data in range(train_set.shape[0]):
				traindata = train_set[data]
				traindata = np.append(traindata,bias)   #add to the end of feature dimension
				sumlist = []
				for classname in range(10):
					tempval = np.dot(traindata, self.w[:,classname])
					sumlist.append(tempval)
				sumarray = np.asarray(sumlist)
				predclass = np.argmax(sumarray)

				trueclass = train_label[data]
				#if(data != 0):
				#	learnrate = 1/data
				if(trueclass != predclass):
					etachange = learnrate * traindata
					self.w[:,predclass] -= etachange
					self.w[:,trueclass] += etachange


		#pass

	def test(self,test_set,test_label):
		""" Test the trained perceptron model (self.w) using testing dataset. 
			The accuracy is computed as the average of correctness 
			by comparing between predicted label and true label. 
			
		Args:
		    test_set(numpy.ndarray): testing examples with a dimension of (# of examples, feature_dim)
		    test_label(numpy.ndarray): testing labels with a dimension of (# of examples, )

		Returns:
			accuracy(float): average accuracy value 
			pred_label(numpy.ndarray): predicted labels with a dimension of (# of examples, )
		"""    

		# YOUR CODE HERE
		accuracy = 0 
		pred_label = np.zeros((len(test_set)))


		bias = 1
		for data in range(test_set.shape[0]):
			testdata = test_set[data]
			testdata = np.append(testdata,bias)   #add to the end of feature dimension
			sumlist = []
			for classname in range(10):
				tempval = np.dot(testdata, self.w[:,classname])
				sumlist.append(tempval)
			sumarray = np.asarray(sumlist)
			predclass = np.argmax(sumarray)
			pred_label[data]= predclass
			trueclass = test_label[data]
			if(predclass==trueclass):
				accuracy+=1

		accuracy = accuracy/test_set.shape[0]
		#print(accuracy)
		#pass
		
		return accuracy, pred_label

	def save_model(self, weight_file):
		""" Save the trained model parameters 
		""" 

		np.save(weight_file,self.w)

	def load_model(self, weight_file):
		""" Load the trained model parameters 
		""" 

		self.w = np.load(weight_file)

