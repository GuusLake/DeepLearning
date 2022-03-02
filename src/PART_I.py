from operator import ge
import numpy as np
import sklearn.datasets
import matplotlib.pyplot as plt

def Sigmoid(X):
    """Calculates the sigmoid

    Args:
        X (numpy.ndarray): Input array

    Returns:
        numpy.ndarray: Output array
    """
    return 1/(1+np.exp(-X))
    
def dSigmoid(X):
    """Calculates the derivative of the sigmoid

    Args:
        X (numpy.ndarray): Input array

    Returns:
        numpy.ndarray: Output array
    """    
    s = 1/(1+np.exp(-X))
    dX = s * (1-s)
    return dX

def Relu(X):
    """Calculates the Relu

    Args:
        X (numpy.ndarray): Input array

    Returns:
        numpy.ndarray: Output array
    """    
    return np.maximum(0,X)

def dRelu(x):
    """Calculates the derivative of the relu

    Args:
        X (numpy.ndarray): Input array

    Returns:
        numpy.ndarray: Output array
    """
    x[x<=0] = 0
    x[x>0] = 1
    return x

class perceptron:
    def __init__(self, x, y, dims = [2, 15, 1]):
        self.X = x.T
        self.Y = y
        self.nn_y = np.zeros((1, self.Y.shape[0]))
        self.layers = len(dims) - 1
        self.dims = dims

        self.weigths = []
        self.bias = []
        self.temp_z = []
        self.temp_a = []

        self.loss = []
        self.lr=0.001
        self.n_samples = self.Y.shape[0]

    def calculate_loss(self):
        """ Calculates the squared error loss

        Args:
            nn_y (numpy.ndarray): array of results generated by the neural network
        """
        squared_errors = (self.nn_y - self.Y) ** 2        
        return np.sum(squared_errors)

    def initialise(self):
        """ Intitiales several lists
        """        

        # unrandomise the randomiser for testing
        np.random.seed(1)

        for i in range(self.layers):
            # Create initial set of weights
            self.weigths.append(np.random.randn(self.dims[i+1], self.dims[i]) / np.sqrt(self.dims[i]))
            self.bias.append(np.zeros((self.dims[i+1], 1)))

            # Create temp variables with same dimensions without references to other list
            self.temp_z.append(0)
            self.temp_a.append(0)           
        return

    def forward(self):
        """ Performs the forward pass

        Returns:
            List: Returns a list of: the predicted value of y and the loss
        """        

        # Adjust weights per layer
        for i in range(self.layers):
            # First layer must be created upon the input data
            if (i == 0):
                self.temp_z[i] = self.weigths[i].dot(self.X) + self.bias[i]
                self.temp_a[i] = Relu(self.temp_z[i])

            # Intermediate hidden layers must be based on the previous values
            elif (i != self.layers - 1):
                self.temp_z[i] = self.weigths[i].dot(self.temp_a[i-1]) + self.bias[i]
                self.temp_a[i] = Relu(self.temp_z[i])
            
            # For last layer (output) use Sigmoid to generate 0 or 1 output
            else:
                self.temp_z[i] = self.weigths[i].dot(self.temp_a[i-1]) + self.bias[i]
                self.temp_a[i] = Sigmoid(self.temp_z[i])
                self.nn_y = self.temp_a[i]
                Loss = self.calculate_loss()
        
        return self.nn_y, Loss

    def backward(self):
        """ Performs the backward pass
        """        
        dLoss_nn_y = - (np.divide(self.Y, self.nn_y ) - np.divide(1 - self.Y, 1 - self.nn_y))    
        
        for i in reversed(range(self.layers)):

            # Front
            if (i == 0):
                dLossZ = dLossA * dRelu(self.temp_z[i])
                dLossA = np.dot(self.weigths[i].T, dLossZ)
                dLossW = 1./self.X.shape[1] * np.dot(dLossZ, self.X.T)
                dLossB = 1./self.X.shape[1] * np.dot(dLossZ, np.ones([dLossZ.shape[1],1]))

            # Intermediate hidden values
            elif (i != self.layers - 1):
                dLossZ = dLossA * dRelu(self.temp_z[i])
                dLossA = np.dot(self.weigths[i].T, dLossZ)
                dLossW = 1./self.temp_a[i-1].shape[1] * np.dot(dLossZ, self.temp_a[i-1].T)
                dLossB = 1./self.temp_a[i-1].shape[1] * np.dot(dLossZ, np.ones([dLossZ.shape[1],1]))

            # Start from the rear
            else:
                dLossZ = dLoss_nn_y * dSigmoid(self.temp_z[i])
                dLossA = np.dot(self.weigths[i].T, dLossZ)
                dLossW = 1./self.temp_a[i-1].shape[1] * np.dot(dLossZ, self.temp_a[i-1].T)
                dLossB = 1./self.temp_a[i-1].shape[1] * np.dot(dLossZ, np.ones([dLossZ.shape[1],1]))

            # Update weights
            self.weigths[i] = self.weigths[i] - self.lr * dLossW
            self.bias[i] = self.bias[i] - self.lr * dLossB
    
    def predict(self,x, y, treshold = 0.5):
        """Predicts values based on the weights and biases from the neural network

        Args:
            x (numpy.ndarray): Array with X values
            y (numpy.ndarray): Array with the real results
            treshold (float, optional): A threshold to differentiate between 1 and 0. Defaults to 0.5.

        Returns:
            list: A list of: A numpy array with results from the neural network and the loss
        """        
        # Set testing data as x and y
        self.X = x.T
        self.Y = y

        # Run the forward pass
        pred, loss = self.forward()

        # Convert the numbers into 1s and 0s
        temp = pred > treshold
        result = temp.astype(int)

        return result, loss
        

def load_data():
    """ Loads data for perceptron

    Returns:
        tuple: A tuple with two numpy arrays: with x values with two features and binary y values
    """    
    N = 500
    gq = sklearn.datasets.make_gaussian_quantiles (
                                        mean=None,
                                        cov =0.7,
                                        n_samples =N,
                                        n_features =2,
                                        n_classes =2,
                                        shuffle =True,
                                        random_state =None)
    return gq

def split_data():
    """Creates an 80/20 train/test split for the generated data

    Returns:
        List: a list of the four parts (as arrays) of the input (X) and output (y)
    """    
    X, y = load_data()
    cutoff = int(0.8 * y.size)
    return X[:cutoff], X[cutoff:], y[:cutoff], y[cutoff:]

def train_nn(per, iter = 10000):
    """Trains the neural network

    Args:
        per (perceptron): The neural network class
        iter (int, optional): The amount of iterations the perceptron should run. Defaults to 10000.
    """    
    # Run the forward and backward a specified amount of iterations
    for i in range(iter):
        nn_y, loss = per.forward()
        per.backward()

        if i % (iter/10) == 0:
                print ("Iteration: {}, Loss: {}".format(i, loss))
                per.loss.append(loss)

def calculate_stats(y, result, loss):
    """Calculates and prints statistics like accuracy and F1-score

    Args:
        y (numpy.ndarray): Real data
        result (numpy.ndarray): Results from the neural network
        loss (double): The loss
    """    
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    diff = []
    for i in range(y.size):
        if (y[i] == result[0][i] == 1):
            TP += 1
            diff.append(1)
        elif(y[i] == result[0][i] == 0):
            TN += 1
            diff.append(0)
        elif(y[i] == 0 and result[0][i] == 1):
            FP += 1
            diff.append(0.5)
        elif(y[i] == 1 and result[0][i] == 0):
            FN += 1
            diff.append(0.5)
        else:
            print("Calculation Error")
        
    acc = (TP + TN) / (y.size)
    recall = TP / (TP + FP)
    precision = TP / (TP + FN)
    F1 = 2 * (precision * recall) / (precision + recall)

    print("Accuracy: {}\nLoss: {}\nRecall: {}\nPrecision: {}\nF1: {}\n".format(acc, loss, recall, precision, F1))
    return np.array(diff)

def run_nn():
    """ Trains the homemade perceptron, then tests on the test set and finally calculates results and create plots

    Args:
        iter (int, optional): Amount of iterations. Defaults to 3000.
    """    
    X_train, X_test, y_train, y_test = split_data()

    per = perceptron(X_train, y_train)
    per.initialise()
    train_nn(per)

    result, loss = per.predict(X_test, y_test)

    diff = calculate_stats(y_test, result, loss)
    create_plot(X_train, y_train)
    create_plot(X_test, y_test)
    create_plot(X_test, diff)

def split_array(X_input):
    """Splits a numpy array into two seperate parts

    Args:
        X_input (numpy.ndarray): An input array to be split

    Returns:
        list: Returns a list of two numpy arrays of the split 
    """    
    X1 = []
    X2 = []
    for X, Y in X_input:
        X1.append(X)
        X2.append(Y)
    return np.array(X1), np.array(X2)


def create_plot(X, y):
    """Creates a scatterplot with the given inputs

    Args:
        X (numpy.ndarray): Array of X1 and X2 values
        y (numpy.ndarray): Array of results to color the values with
    """    
    X1, X2 = split_array(X)
    plt.scatter(X1, X2, c=y, cmap='cividis')
    plt.show()



def main():
    run_nn()

if __name__ == "__main__":
    main()
