import numpy as np


class NaiveBayes(object):
	def __init__(self,num_class,feature_dim,num_value):
		"""Initialize a naive bayes model. 

		This function will initialize prior and likelihood, where 
		prior is P(class) with a dimension of (# of class,)
			that estimates the empirical frequencies of different classes in the training set.
		likelihood is P(F_i = f | class) with a dimension of 
			(# of features/pixels per image, # of possible values per pixel, # of class),
			that computes the probability of every pixel location i being value f for every class label.  

		Args:
			num_class(int): number of classes to classify
			feature_dim(int): feature dimension for each example 
			num_value(int): number of possible values for each pixel 
		"""

		self.num_value = num_value
		self.num_class = num_class
		self.feature_dim = feature_dim

		self.prior = np.zeros((num_class))
		self.likelihood = np.zeros((feature_dim,num_value,num_class))

	def train(self,train_set,train_label):
		""" Train naive bayes model (self.prior and self.likelihood) with training dataset. 
			self.prior(numpy.ndarray): training set class prior (in log) with a dimension of (# of class,),
			self.likelihood(numpy.ndarray): traing set likelihood (in log) with a dimension of 
				(# of features/pixels per image, # of possible values per pixel, # of class).
			You should apply Laplace smoothing to compute the likelihood. 

		Args:
			train_set(numpy.ndarray): training examples with a dimension of (# of examples, feature_dim)
			train_label(numpy.ndarray): training labels with a dimension of (# of examples, )
		"""

		# YOUR CODE HERE
		for classname in range(self.num_class):
			self.prior[classname] = np.sum(train_label == classname)/(len(train_label))

		for pic in range(len(train_set)):
			count = 0
			for pix_val in train_set[pic]:
				self.likelihood[count][pix_val][train_label[pic]] +=1
				count += 1


		k = 1
		for classname in range(self.num_class):
			for i in range(len(train_set[pic])):
				self.likelihood[i,:,classname] = (self.likelihood[i,:,classname]+1)/(k*self.num_value + self.prior[classname]*len(train_set))


		#pass

	def test(self,test_set,test_label):
		""" Test the trained naive bayes model (self.prior and self.likelihood) on testing dataset,
			by performing maximum a posteriori (MAP) classification.  
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
		#print("start to test")
		#pass
		for i in range(len(test_label)):
			problist = []
			for classname in range(self.num_class):
				sum = np.log10(self.prior[classname])
				for dimval in range(self.feature_dim):
					sum += np.log10(self.likelihood[dimval, test_set[i,dimval], classname])
				problist.append(sum)
			probarray = np.asarray(problist)
			pred_label[i] = probarray.argmax()

		for i in range(len(test_label)):
			if(test_label[i] == pred_label[i]):
				accuracy += 1
		accuracy = accuracy/len(test_label)
		print(accuracy)

		return accuracy, pred_label


	def save_model(self, prior, likelihood):
		""" Save the trained model parameters 
		"""    

		np.save(prior, self.prior)
		np.save(likelihood, self.likelihood)

	def load_model(self, prior, likelihood):
		""" Load the trained model parameters 
		""" 

		self.prior = np.load(prior)
		self.likelihood = np.load(likelihood)

	def intensity_feature_likelihoods(self, likelihood):
		"""
		Get the feature likelihoods for high intensity pixels for each of the classes,
			by sum the probabilities of the top 128 intensities at each pixel location,
			sum k<-128:255 P(F_i = k | c).
			This helps generate visualization of trained likelihood images. 
		
		Args:
			likelihood(numpy.ndarray): likelihood (in log) with a dimension of
				(# of features/pixels per image, # of possible values per pixel, # of class)
		Returns:
			feature_likelihoods(numpy.ndarray): feature likelihoods for each class with a dimension of
				(# of features/pixels per image, # of class)
		"""
		# YOUR CODE HERE
		#print("start to intensify")
		feature_likelihoods = np.zeros((likelihood.shape[0],likelihood.shape[2]))
		for classname in range(self.num_class):
			for idx in range(likelihood.shape[0]):
				sum = 0
				for i in range(128,256):
					sum += likelihood[idx][i][classname]
				feature_likelihoods[idx,classname]=sum
		#print("end intensify")
		return feature_likelihoods
