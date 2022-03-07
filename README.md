# Assignment 1

## Running Code

To run the the code:
```
python "Assignment 1.py"
```

This will do the following things:
- Train our neural network
- Test our neural net work
- Show its results and corresponding plots (including general plots of the data)
- Train a similar Sklearn network
- Test the  Sklearn network
- Show and plot its results

## Changing parameters

Our implementation allows for dynamic allocation of more hidden layers. This can be done by changing the following in line 332 from:
```
run_nns()
```
To:
```
run_nns(layers = [15, 3])
```
This will create two hidden layers one of 15 features and one of 3 features. More layers can be added by adding more numbers to this list, the number itself represents the amount of features this layer has. This will both affect our own model and the sklearn model.

Additionally the amount of iterations can be altered by changing the same line 332 from:
```
run_nns()
```
To:
```
run_nns(iter=20000)
```
This will both change the amount of iterations in our own model as in the sklearn model.

These two parameters can also be combined as such:
```
run_nns(layers = [15, 3], iter=20000)
```