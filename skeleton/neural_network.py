import numpy as np


def init_weights(d, dp):
    return 0.01 * np.random.uniform(0.0, 1.0, (d, dp)), np.zeros(dp)
"""
    Minigratch Gradient Descent Function to train model
    1. Format the data
    2. call four_nn function to obtain losses
    3. Return all the weights/biases and a list of losses at each epoch
    Args:
        epoch (int) - number of iterations to run through neural net
        w1, w2, w3, w4, b1, b2, b3, b4 (numpy arrays) - starting weights
        x_train (np array) - (n,d) numpy array where d=number of features
        y_train (np array) - (n,) all the labels corresponding to x_train
        num_classes (int) - number of classes (range of y_train)
        shuffle (bool) - shuffle data at each epoch if True. Turn this off for testing.
    Returns:
        w1, w2, w3, w4, b1, b2, b3, b4 (numpy arrays) - resulting weights
        losses (list of ints) - each index should correspond to epoch number
            Note that len(losses) == epoch
    Hints:
        Should work for any number of features and classes
        Good idea to print the epoch number at each iteration for sanity checks!
        (Stdout print will not affect autograder as long as runtime is within limits)
"""
def minibatch_gd(epoch, w1, w2, w3, w4, b1, b2, b3, b4, x_train, y_train, num_classes, shuffle=True):

    #IMPLEMENT HERE
    batchsize = 200
    #already initialized w and b
    losses = []
    for e in range(epoch):
        #randomization is consistent for both your x_train and y_train.
        loss = 0
        print(e)
        #index = np.zeros(len(x_train))
        #for i in range(len(x_train)):
        #    index[i] = int(i)
        x_new = x_train.copy()
        y_new = y_train.copy()
        if shuffle:
            index = np.random.choice(len(x_train), len(x_train), replace=False)
            #np.random.shuffle(index)
            x_new = x_train[index]
            y_new = y_train[index]

        for i in range(int(x_train.shape[0]/batchsize)):
            x = x_new[i*batchsize:(i+1)*batchsize]
            y = y_new[i*batchsize:(i+1)*batchsize]
            temploss = four_nn(x, w1, w2, w3, w4, b1, b2, b3, b4, y, False)
            loss += temploss
        print("loss",loss)
        losses.append(loss)


    return w1, w2, w3, w4, b1, b2, b3, b4, losses

"""
    Use the trained weights & biases to see how well the nn performs
        on the test data
    Args:
        All the weights/biases from minibatch_gd()
        x_test (np array) - (n', d) numpy array
        y_test (np array) - (n',) all the labels corresponding to x_test
        num_classes (int) - number of classes (range of y_test)
    Returns:
        avg_class_rate (float) - average classification rate
        class_rate_per_class (list of floats) - Classification Rate per class
            (index corresponding to class number)
    Hints:
        Good place to show your confusion matrix as well.
        The confusion matrix won't be autograded but necessary in report.
"""
def test_nn(w1, w2, w3, w4, b1, b2, b3, b4, x_test, y_test, num_classes):

    classifications = four_nn(x_test, w1, w2, w3, w4, b1, b2, b3, b4, y_test, True)
    avg_class_rate = np.sum(classifications == y_test) / len(x_test)
    class_rate_per_class = [0.0] * num_classes

    confusion_M = np.zeros((num_classes,num_classes))
    for i in range(len(classifications)):
        confusion_M[y_test[i]][classifications[i]] += 1

    for i in range(num_classes):
        total = np.sum(confusion_M[i])
        class_rate_per_class[i] = confusion_M[i][i]/total

    return avg_class_rate, class_rate_per_class

"""
    4 Layer Neural Network
    Helper function for minibatch_gd
    Up to you on how to implement this, won't be unit tested
    Should call helper functions below
"""
def four_nn(x, w1, w2, w3, w4, b1, b2, b3, b4, y, test):
    z1, acache1 = affine_forward(x, w1, b1)
    a1, rcache1 = relu_forward(z1)
    z2, acache2 = affine_forward(a1, w2, b2)
    a2, rcache2 = relu_forward(z2)
    z3, acache3 = affine_forward(a2, w3, b3)
    a3, rcache3 = relu_forward(z3)
    f,  acache4 = affine_forward(a3, w4, b4)
    if test == True:
        classifications = np.argmax(f,axis=1)#axis
        return classifications
    loss, dF = cross_entropy(f,y)
    dA3, dW4, db4 = affine_backward(dF, acache4)
    dZ3 = relu_backward(dA3, rcache3)
    dA2, dW3, db3 = affine_backward(dZ3, acache3)
    dZ2 = relu_backward(dA2, rcache2)
    dA1, dW2, db2 = affine_backward(dZ2, acache2)
    dZ1 = relu_backward(dA1, rcache1)
    dX, dW1, db1 = affine_backward(dZ1, acache1)

    eta = 0.1
    #w1 = w1- eta*dW1
    #w2 = w2- eta*dW2
    #w3 = w3- eta*dW3
    #w4 = w4- eta*dW4
    #b1 = b1- eta*db1
    #b2 = b2- eta*db2
    #b3 = b3- eta*db3
    #b4 = b4- eta*db4
    #w1 = w1 - (eta * dW1)
    w1 -= eta * dW1
    w2 -= eta * dW2
    w3 -= eta * dW3
    w4 -= eta * dW4
    b1 -= eta * db1
    b2 -= eta * db2
    b3 -= eta * db3
    b4 -= eta * db4
    return loss
    #pass


"""
    Next five functions will be used in four_nn() as helper functions.
    All these functions will be autograded, and a unit test script is provided as unit_test.py.
    The cache object format is up to you, we will only autograde the computed matrices.

    Args and Return values are specified in the MP docs
    Hint: Utilize numpy as much as possible for max efficiency.
        This is a great time to review on your linear algebra as well.
"""
def affine_forward(A, W, b):
    Z = np.matmul(A,W)+b
    cache = (A,W,b)
    return Z, cache

def affine_backward(dZ, cache):
    A,W,b = cache
    # Z(i,j), W(k,j), A(i,k)
    dA = np.dot(dZ, W.T)
    dW = np.dot(A.T, dZ)
    dB = np.sum(dZ,0)
    return dA, dW, dB

def relu_forward(Z):
    #Z(n,d)
    A = Z.copy()
    A[A<0]=0
    #for n in range(A.shape[0]):
    #    for d in range(A.shape[1]):
    #        A[n][d] = max(A[n][d],0)
    cache = Z
    return A, cache

def relu_backward(dA, cache):
    Z = cache
    dA[Z<0] = 0
    return dA

#def cross_entropy(F, y):
#    n = F.shape[0]
#    outersum = 0
#    for i in range(n):
#        logsum = np.log(np.sum(np.exp(F[i])))
#        outersum += F[i,int(y[i])] - logsum
#    loss = (-1/n) * outersum
#
#    dF = F.copy()
#    for i in range(dF.shape[0]):
#        for j in range(dF.shape[1]):
#            factor = np.exp(F[i][j])/np.sum(np.exp(F[i]))
#            dF[i][j] = (-1/n)*(1*(j==y[i])-factor)
#
#    return loss, dF
def cross_entropy(F, y):
    n = len(F)
    exp_F = np.exp(F)
    sum_exp_F = np.sum(exp_F, axis=1)
    Fiyi = F[np.arange(n), y.astype(int)]
    log_stuff = np.log(sum_exp_F)
    loss = (-1 / n) * np.sum(Fiyi - log_stuff)

    first_item = np.zeros(F.shape)
    first_item[np.arange(n), y.astype(int)] = 1
    second_item = exp_F / sum_exp_F.reshape((-1, 1))
    dF = (-1 / n) * (first_item - second_item)

    return loss, dF

