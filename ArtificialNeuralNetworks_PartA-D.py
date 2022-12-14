# -*- coding: utf-8 -*-
"""Assignment3_AI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XJcvtRUqN8DpfDFOUbrCTN1MEKOxdV0s
"""

import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import torch
from torch import nn
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset
from torchvision import datasets
from torchvision.transforms import ToTensor, Lambda, Compose, Resize
from numpy import genfromtxt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import accuracy_score
import torch.nn.functional as F

#Problem 2.1: A single arti cial neuron

#create a tensor v
v = torch.linspace(-5.0,5.0, steps=100)
#a tensor of zeros of the same size as v
zero = torch.zeros(len(v))

#define ReLU activation function
def max(v):
    return torch.max(zero,v)
#defien tanh activation function
def tanh(v):
  return torch.tanh(v)

# #plot the two activation functions over v
plt.plot(v,max(v), v, tanh(v))

#Task A - 1D Linear and non-linear regression - using simple FANNs

#define true parameters values
a_true = 5.0
b_true = 3.0

#create X values
X = np.random.uniform(0,10,250)

#define noise level
sigma_epsilon = 5.0
noise = np.random.randn(len(X))

#compute y values
Y = a_true*X + b_true + sigma_epsilon *noise

#transforming X & Y to PyTorch tensors and reshaping them so each row has
#a single input value.
X = torch.tensor(X).reshape(len(X),1).float()
Y = torch.tensor(Y).reshape(len(Y),1).float()

#making a PyTorch dataset object for the data
my_dataset = TensorDataset(X,Y)
#making a PyTorch dataloader object 
my_dataloader = DataLoader(my_dataset, batch_size = 50, shuffle = True)

#Defining a single neuron having 1 input
model = nn.Sequential(
nn.Linear(in_features=1, out_features=1)
)
#Defining a cost function
cost_function = nn.MSELoss()

#Define and Set an optimizer object
optim = torch.optim.SGD(model.parameters(), lr=0.01)

#create an empty array to store cost values
training_minibatch_Js =[]
#define number of epochs
nr_epochs = 10

for epoch_i in range(nr_epochs):
  for X_batch, y_batch in my_dataloader:
    y_preds = model(X_batch) #make prediction on batch
    cost = cost_function(y_preds, y_batch) #compute cost value
    training_minibatch_Js.append(cost.item())
    optim.zero_grad() #zero the grads of all model params
    cost.backward() #compute J gradient of all model params
    optim.step() #take one update step for all model params

with torch.no_grad():
  y_preds = model(X)

#Print all parameters in your neural network model
for p in model.named_parameters():
  print(p)

#plotting
plt.plot(X,Y,'o',X,y_preds)

#Plot your cost
plt.figure(figsize=[8,4])
plt.plot(training_minibatch_Js)
plt.xlabel('update step i on mini-batch')
plt.ylabel('Cost')
plt.title('Cost during training on train-set (per mini-batch)')
plt.grid()

#(i) Repeat the above steps (b)-(h) for the MarvinMinsky.csv dataset

#load data from a csv file into a numpy array
my_data = genfromtxt('/content/dataset_Marvin_Minsky.csv', delimiter=',',skip_header=1) 

#extract X and Y values
X = my_data[:,0] 
y_obs = my_data[:,1] 

#transforming X & Y to PyTorch tensors and reshaping them so each row has
#a single input value
X = torch.tensor(X).reshape(len(X),1).float()
y_obs = torch.tensor(y_obs).reshape(len(y_obs),1).float()

#create a dataset by turning tensors into datasets objects
my_dataset = TensorDataset(X, y_obs) 
#making a PyTorch dataloader object 
my_dataloader = DataLoader(my_dataset, batch_size=100, shuffle=True)

#Defining a single neuron having 1 input
model = nn.Sequential(
nn.Linear(in_features=1, out_features=10),
nn.ReLU(),
nn.Linear(in_features=10, out_features=10),
nn.ReLU(),
nn.Linear(in_features=10, out_features=5),
nn.ReLU(),
nn.Linear(in_features=5, out_features=5),
nn.ReLU(),
nn.Linear(in_features=5, out_features=1)
)

#Defining a cost function
cost_function = nn.MSELoss()

#Define and Set an optimizer object
optim = torch.optim.SGD(model.parameters(), lr=0.03)

#create an empty array to store cost values
training_minibatch_Js =[]
#define number of epochs
nr_epochs = 1000

for epoch_i in range(nr_epochs):
  for X_batch, y_batch in my_dataloader:
    y_preds = model(X_batch) #make prediction on batch
    cost = cost_function(y_preds, y_batch) #compute cost value
    training_minibatch_Js.append(cost.item())
    optim.zero_grad() #zero the grads of all model params
    cost.backward() #compute J gradient of all model params
    optim.step() #take one update step for all model params

with torch.no_grad():
  y_preds = model(X)

#print cost value
print(f'The final value of the cost function is {cost}')

#Print all parameters in your neural network model
# for p in model.named_parameters():
#   print(p)

#plotting
plt.figure(figsize=[8,4])
plt.plot(X,y_obs,'o',X,y_preds,'x')

#Plot your cost
plt.figure(figsize=[8,4])
plt.plot(training_minibatch_Js)
plt.xlabel('update step i on mini-batch')
plt.ylabel('Cost')
plt.title('Cost during training on train-set (per mini-batch)')
plt.grid()

#Task B: 2-variable regression - using FANNs to  t data drawn from a bell curve.

#Number of data points to generate and sample from
N = 1000 
#Create X values
x = 10*torch.rand(size=[N,2]) - 5
mean_true = torch.tensor([0.0, 0.0])
#Create an empty tensor to store y values
y = torch.zeros(N).reshape(-1,1)

#Compute y values
for i in range(len(x)):
  y[i] = torch.exp(-((x[i,:]-mean_true).T@(x[i,:]-mean_true))/4) + 0.04*torch.randn(1)

#create a dataset by turning tensors into datasets objects
my_dataset = TensorDataset(x, y) 
#define a batch size
batch_size = 200
#making a PyTorch dataloader object 
my_dataloader = DataLoader(my_dataset, batch_size=batch_size, shuffle=True)

#model architecture 1
model_one = nn.Sequential(
nn.Linear(in_features=2, out_features=10),
nn.ReLU(),
nn.Linear(in_features=10, out_features=1)
)
#model architecture 2
model_two = nn.Sequential(
nn.Linear(in_features=2, out_features=50),
nn.ReLU(),
nn.Linear(in_features=50, out_features=1)
)
#model architecture 3
model_three = nn.Sequential(
nn.Linear(in_features=2, out_features=300),
nn.ReLU(),
nn.Linear(in_features=300, out_features=1)
)
#model architecture 4
model_four = nn.Sequential(
nn.Linear(in_features=2, out_features=100),
nn.ReLU(),
nn.Linear(in_features=100, out_features=20),
nn.ReLU(),
nn.Linear(in_features=20, out_features=5),
nn.ReLU(),
nn.Linear(in_features=5, out_features=1)
)
#model architecture 5
model_five = nn.Sequential(
nn.Linear(in_features=2, out_features=300),
nn.ReLU(),
nn.Linear(in_features=300, out_features=100),
nn.ReLU(),
nn.Linear(in_features=100, out_features=20),
nn.ReLU(),
nn.Linear(in_features=20, out_features=1)
)

#Defining a cost function
cost_function = nn.MSELoss()

#Task B: 2-variable regression - using FANNs to  t data drawn from a bell curve.
#model one

#learning rate
lr = 0.009

#Define and Set an optimizer object
optim = torch.optim.SGD(model_one.parameters(), lr=lr)

#create an empty array to store cost values
training_minibatch_Js =[]
#define number of epochs
nr_epochs = 1000

for epoch_i in range(nr_epochs):
  for X_batch, y_batch in my_dataloader:
    y_preds = model_one(X_batch) #make prediction on batch
    cost = cost_function(y_preds, y_batch) #compute cost value
    training_minibatch_Js.append(cost.item())
    optim.zero_grad() #zero the grads of all model params
    cost.backward() #compute J gradient of all model params
    optim.step() #take one update step for all model params

#print cost value
print(f'The final value of the cost function is {cost}')
#print learning rate
print(f'Learning rate is: {lr}')
#print number of epochs
print(f'Number of epochs: {nr_epochs}')

x1 = torch.linspace(start=-5, end=5, steps=100)
x2 = torch.linspace(start=-5, end=5, steps=100)
X, Y = torch.meshgrid(x1, x2)

s = torch.stack([X.ravel(), Y.ravel()]).T # all grid coordinates for region.

with torch.no_grad():
  y_preds = model_one(s) # making predictions on surface grid to get surface values.

# 3D surface plotting
fig = plt.figure()
fig.set_figwidth(10)
fig.set_figheight(10)
ax = Axes3D(fig)
ax.scatter(s[:,0], s[:,1], y_preds, label='Fitted FANN')
ax.scatter(x[:,0], x[:,1], y, label='datapoints')
# plotting data points
ax.legend()
ax.set_xlabel('x1')
ax.set_ylabel('x2')

#Plot your cost
plt.figure(figsize=[8,4])
plt.plot(training_minibatch_Js)
plt.xlabel('update step i on mini-batch')
plt.ylabel('Cost')
plt.title('Cost during training on train-set (per mini-batch)')
plt.grid()

#Task B: 2-variable regression - using FANNs to  t data drawn from a bell curve.
#model two

#learning rate
lr = 0.009

#Define and Set an optimizer object
optim = torch.optim.SGD(model_two.parameters(), lr=lr)

#create an empty array to store cost values
training_minibatch_Js =[]
#define number of epochs
nr_epochs = 1000

for epoch_i in range(nr_epochs):
  for X_batch, y_batch in my_dataloader:
    y_preds = model_two(X_batch) #make prediction on batch
    cost = cost_function(y_preds, y_batch) #compute cost value
    training_minibatch_Js.append(cost.item())
    optim.zero_grad() #zero the grads of all model params
    cost.backward() #compute J gradient of all model params
    optim.step() #take one update step for all model params

#print cost value
print(f'The final value of the cost function is {cost}')
#print learning rate
print(f'Learning rate is: {lr}')
#print number of epochs
print(f'Number of epochs: {nr_epochs}')


x1 = torch.linspace(start=-5, end=5, steps=100)
x2 = torch.linspace(start=-5, end=5, steps=100)
X, Y = torch.meshgrid(x1, x2)

s = torch.stack([X.ravel(), Y.ravel()]).T # all grid coordinates for region.

with torch.no_grad():
  y_preds = model_two(s) # making predictions on surface grid to get surface values.

# 3D surface plotting
fig = plt.figure()
fig.set_figwidth(10)
fig.set_figheight(10)
ax = Axes3D(fig)
ax.scatter(s[:,0], s[:,1], y_preds, label='Fitted FANN')
ax.scatter(x[:,0], x[:,1], y, label='datapoints')
# plotting data points
ax.legend()
ax.set_xlabel('x1')
ax.set_ylabel('x2')

#Plot your cost
plt.figure(figsize=[8,4])
plt.plot(training_minibatch_Js)
plt.xlabel('update step i on mini-batch')
plt.ylabel('Cost')
plt.title('Cost during training on train-set (per mini-batch)')
plt.grid()

#Task B: 2-variable regression - using FANNs to  t data drawn from a bell curve.
#model three

#learning rate
lr = 0.009

#Define and Set an optimizer object
optim = torch.optim.SGD(model_three.parameters(), lr=lr)

#create an empty array to store cost values
training_minibatch_Js =[]
#define number of epochs
nr_epochs = 1000

for epoch_i in range(nr_epochs):
  for X_batch, y_batch in my_dataloader:
    y_preds = model_three(X_batch) #make prediction on batch
    cost = cost_function(y_preds, y_batch) #compute cost value
    training_minibatch_Js.append(cost.item())
    optim.zero_grad() #zero the grads of all model params
    cost.backward() #compute J gradient of all model params
    optim.step() #take one update step for all model params

#print cost value
print(f'The final value of the cost function is {cost}')
#print learning rate
print(f'Learning rate is: {lr}')
#print number of epochs
print(f'Number of epochs: {nr_epochs}')

x1 = torch.linspace(start=-5, end=5, steps=100)
x2 = torch.linspace(start=-5, end=5, steps=100)
X, Y = torch.meshgrid(x1, x2)

s = torch.stack([X.ravel(), Y.ravel()]).T # all grid coordinates for region.

with torch.no_grad():
  y_preds = model_three(s) # making predictions on surface grid to get surface values.

# 3D surface plotting
fig = plt.figure()
fig.set_figwidth(10)
fig.set_figheight(10)
ax = Axes3D(fig)
ax.scatter(s[:,0], s[:,1], y_preds, label='Fitted FANN')
ax.scatter(x[:,0], x[:,1], y, label='datapoints')
# plotting data points
ax.legend()
ax.set_xlabel('x1')
ax.set_ylabel('x2')

#Plot your cost
plt.figure(figsize=[8,4])
plt.plot(training_minibatch_Js)
plt.xlabel('update step i on mini-batch')
plt.ylabel('Cost')
plt.title('Cost during training on train-set (per mini-batch)')
plt.grid()

#Task B: 2-variable regression - using FANNs to  t data drawn from a bell curve.
#model four

#learning rate
lr = 0.009

#Define and Set an optimizer object
optim = torch.optim.SGD(model_four.parameters(), lr=lr)

#create an empty array to store cost values
training_minibatch_Js =[]
#define number of epochs
nr_epochs = 2000

for epoch_i in range(nr_epochs):
  for X_batch, y_batch in my_dataloader:
    y_preds = model_four(X_batch) #make prediction on batch
    cost = cost_function(y_preds, y_batch) #compute cost value
    training_minibatch_Js.append(cost.item())
    optim.zero_grad() #zero the grads of all model params
    cost.backward() #compute J gradient of all model params
    optim.step() #take one update step for all model params

#print cost value
print(f'The final value of the cost function is {cost}')
#print learning rate
print(f'Learning rate is: {lr}')
#print number of epochs
print(f'Number of epochs: {nr_epochs}')


x1 = torch.linspace(start=-5, end=5, steps=100)
x2 = torch.linspace(start=-5, end=5, steps=100)
X, Y = torch.meshgrid(x1, x2)

s = torch.stack([X.ravel(), Y.ravel()]).T # all grid coordinates for region.

with torch.no_grad():
  y_preds = model_four(s) # making predictions on surface grid to get surface values.

# 3D surface plotting
fig = plt.figure()
fig.set_figwidth(10)
fig.set_figheight(10)
ax = Axes3D(fig)
ax.scatter(s[:,0], s[:,1], y_preds, label='Fitted FANN')
ax.scatter(x[:,0], x[:,1], y, label='datapoints')
# plotting data points
ax.legend()
ax.set_xlabel('x1')
ax.set_ylabel('x2')

#Plot your cost
plt.figure(figsize=[8,4])
plt.plot(training_minibatch_Js)
plt.xlabel('update step i on mini-batch')
plt.ylabel('Cost')
plt.title('Cost during training on train-set (per mini-batch)')
plt.grid()

#Task B: 2-variable regression - using FANNs to  t data drawn from a bell curve.
#model five

#learning rate
lr = 0.009

#Define and Set an optimizer object
optim = torch.optim.SGD(model_five.parameters(), lr=lr)

#create an empty array to store cost values
training_minibatch_Js =[]
#define number of epochs
nr_epochs = 2000

for epoch_i in range(nr_epochs):
  for X_batch, y_batch in my_dataloader:
    y_preds = model_five(X_batch) #make prediction on batch
    cost = cost_function(y_preds, y_batch) #compute cost value
    training_minibatch_Js.append(cost.item())
    optim.zero_grad() #zero the grads of all model params
    cost.backward() #compute J gradient of all model params
    optim.step() #take one update step for all model params

#print cost value
print(f'The final value of the cost function is {cost}')
#print learning rate
print(f'Learning rate is: {lr}')
#print number of epochs
print(f'Number of epochs: {nr_epochs}')

x1 = torch.linspace(start=-5, end=5, steps=100)
x2 = torch.linspace(start=-5, end=5, steps=100)
X, Y = torch.meshgrid(x1, x2)

s = torch.stack([X.ravel(), Y.ravel()]).T # all grid coordinates for region.

with torch.no_grad():
  y_preds = model_five(s) # making predictions on surface grid to get surface values.

# 3D surface plotting
fig = plt.figure()
fig.set_figwidth(10)
fig.set_figheight(10)
ax = Axes3D(fig)
ax.scatter(s[:,0], s[:,1], y_preds, label='Fitted FANN')
ax.scatter(x[:,0], x[:,1], y, label='datapoints')
# plotting data points
ax.legend()
ax.set_xlabel('x1')
ax.set_ylabel('x2')

#Plot your cost
plt.figure(figsize=[8,4])
plt.plot(training_minibatch_Js)
plt.xlabel('update step i on mini-batch')
plt.ylabel('Cost')
plt.title('Cost during training on train-set (per mini-batch)')
plt.grid()

#Task B: 2-variable regression - using FANNs to  t data drawn from a bell curve.
#(f)

#creating a test set of 1000 points
#Number of data points 
N = 1000 
#Create X values
x_test = 10*torch.rand(size=[N,2]) - 5
mean_true = torch.tensor([0.0, 0.0])
#Create an empty tensor to store y values
y_test = torch.zeros(N).reshape(-1,1)

#Compute y values
for i in range(len(x_test)):
  y_test[i] = torch.exp(-((x_test[i,:]-mean_true).T@(x_test[i,:]-mean_true))/4) + 0.04*torch.randn(1)

#compute y prediction using the five models 
with torch.no_grad():
  y_preds_model1 = model_one(x_test)
  y_preds_model2 = model_two(x_test)
  y_preds_model3 = model_three(x_test)
  y_preds_model4 = model_four(x_test)
  y_preds_model5 = model_five(x_test)

cost_model1 = cost_function(y_preds_model1, y_test)
cost_model2 = cost_function(y_preds_model2, y_test)
cost_model3 = cost_function(y_preds_model3, y_test)
cost_model4 = cost_function(y_preds_model4, y_test)
cost_model5 = cost_function(y_preds_model5, y_test)

print(f"Cost model one: {cost_model1}")
print(f"Cost model two: {cost_model2}")
print(f"Cost model three: {cost_model3}")
print(f"Cost model four: {cost_model4}")
print(f"Cost model five: {cost_model5}")

#Task B: 2-variable regression - using FANNs to  t data drawn from a bell curve.
#(g)

#Number of data points to generate and sample from
N = 50 
#Create X values
x = 10*torch.rand(size=[N,2]) - 5
mean_true = torch.tensor([0.0, 0.0])
#Create an empty tensor to store y values
y = torch.zeros(N).reshape(-1,1)

#Compute y values
for i in range(len(x)):
  y[i] = torch.exp(-((x[i,:]-mean_true).T@(x[i,:]-mean_true))/4) + 0.04*torch.randn(1)

#create a dataset by turning tensors into datasets objects
my_dataset = TensorDataset(x, y) 
#define a batch size
batch_size = 5
#making a PyTorch dataloader object 
my_dataloader = DataLoader(my_dataset, batch_size=batch_size, shuffle=True)

#model architecture 1
model_one = nn.Sequential(
nn.Linear(in_features=2, out_features=10),
nn.ReLU(),
nn.Linear(in_features=10, out_features=1)
)
#model architecture 5
model_five = nn.Sequential(
nn.Linear(in_features=2, out_features=300),
nn.ReLU(),
nn.Linear(in_features=300, out_features=100),
nn.ReLU(),
nn.Linear(in_features=100, out_features=20),
nn.ReLU(),
nn.Linear(in_features=20, out_features=1)
)

#Defining a cost function
cost_function = nn.MSELoss()

#training model one and five on the 50 data points

#learning rate
lr = 0.009
#Define and Set an optimizer object
optim_one = torch.optim.SGD(model_one.parameters(), lr=lr)
optim_five = torch.optim.SGD(model_five.parameters(), lr=lr)
#create an empty array to store cost values
training_minibatch_Js_one =[]
training_minibatch_Js_five =[]
#define number of epochs
nr_epochs = 1500

for epoch_i in range(nr_epochs):
  for X_batch, y_batch in my_dataloader:
    y_preds_one = model_one(X_batch) #make prediction on batch
    y_preds_five = model_five(X_batch) 
    cost_one= cost_function(y_preds_one, y_batch) #compute cost value
    cost_five= cost_function(y_preds_five, y_batch) 
    training_minibatch_Js_one.append(cost_one.item()) #append cost value to the array
    training_minibatch_Js_five.append(cost_five.item())
    optim_one.zero_grad() #zero the grads of all model params
    optim_five.zero_grad()
    cost_one.backward() #compute J gradient of all model params
    cost_five.backward()
    optim_one.step() #take one update step for all model params
    optim_five.step()

#print cost value
print(f'The final value of the cost function for mode one on training data is {cost_one}')
print(f'The final value of the cost function for mode five on training data is {cost_five}')
#print learning rate
print(f'Learning rate is: {lr}')
#print number of epochs
print(f'Number of epochs: {nr_epochs}')

#plotting cost functions
plt.figure(figsize=[8,4])
plt.plot(training_minibatch_Js_one)
plt.xlabel('update step i on mini-batch')
plt.ylabel('Cost')
plt.title('Model one cost during training on train-set using (per mini-batch)')
plt.grid()

plt.figure(figsize=[8,4])
plt.plot(training_minibatch_Js_five)
plt.xlabel('update step i on mini-batch')
plt.ylabel('Cost')
plt.title('Model five cost during training on train-set (per mini-batch)')
plt.grid()

#creating a test set of 1000 points
#Number of data points 
N = 1000 
#Create X values
x_test = 10*torch.rand(size=[N,2]) - 5
mean_true = torch.tensor([0.0, 0.0])
#Create an empty tensor to store y values
y_test = torch.zeros(N).reshape(-1,1)

#Compute y values
for i in range(len(x_test)):
  y_test[i] = torch.exp(-((x_test[i,:]-mean_true).T@(x_test[i,:]-mean_true))/4) + 0.04*torch.randn(1)

#compute y prediction using the two models 
with torch.no_grad():
  y_preds_model_one = model_one(x_test)
  y_preds_model_five = model_five(x_test)

#compute cost function for the two models
cost_model_one = cost_function(y_preds_model_one, y_test)
cost_model_five = cost_function(y_preds_model_five, y_test)

#printing the cost values
print(f"Cost of test data for model one: {cost_model_one}")
print(f"Cost of test data for model two: {cost_model_five}")

#creating grid points for the surface
x1 = torch.linspace(start=-5, end=5, steps=100)
x2 = torch.linspace(start=-5, end=5, steps=100)
X, Y = torch.meshgrid(x1, x2)

s = torch.stack([X.ravel(), Y.ravel()]).T # all grid coordinates for region.

with torch.no_grad():
  y_preds_one = model_one(s) # making predictions on surface grid to get surface values.
  y_preds_five = model_five(s)

# 3D surface plotting
fig = plt.figure()
fig.set_figwidth(10)
fig.set_figheight(10)
ax = Axes3D(fig)
ax.scatter(s[:,0], s[:,1], y_preds_one, label='Fitted FANN')
ax.scatter(x[:,0], x[:,1], y, label='datapoints')
# plotting data points
ax.legend()
ax.set_xlabel('x1')
ax.set_ylabel('x2')

fig = plt.figure()
fig.set_figwidth(10)
fig.set_figheight(10)
ax = Axes3D(fig)
ax.scatter(s[:,0], s[:,1], y_preds_five, label='Fitted FANN')
ax.scatter(x[:,0], x[:,1], y, label='datapoints')
# plotting data points
ax.legend()
ax.set_xlabel('x1')
ax.set_ylabel('x2')

from google.colab import drive
drive.mount('/content/drive')
import os
os.getcwd()
!pwd
os.chdir('drive')
os.chdir('MyDrive')
os.listdir()
os.chdir('Colab_Notebooks')

#Task C: Signal Classication with FANNs
import assignment_ann as a4

signal_dataset = a4.SignalDataset() # Provides back a PyTorch Dataset OBJECT!
size_of_signal_dataset = len(signal_dataset) # Print size of whole dataset
size_of_signal_vector = len(signal_dataset[0][0])
print(f'The original dataset has {size_of_signal_dataset} signals')
print(f'Each signal vector is {size_of_signal_vector} long')

fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(signal_dataset[0][0])
axs[0, 0].set_title('Normal Signal')
axs[0, 1].plot(signal_dataset[1][0])
axs[0, 1].set_title('Abnormal Signal')
axs[1, 0].plot(signal_dataset[2][0])
axs[1, 0].set_title('Abnormal Signal')
axs[1, 1].plot(signal_dataset[3][0])
axs[1, 1].set_title('Abnormal Signal')

for ax in axs.flat:
    ax.set(xlabel='x-label', ylabel='y-label')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()

original_data = signal_dataset # Init your PyTorch Dataset object
size_of_original_data = len(original_data)

#////////////////////////SPLITTING//////////////////////////////////////////////
#Specify split fractions: !Must sum to 1!
train_fraction = 0.70
val_fraction = 0.20
test_fraction = 0.10 # for show purposes

# Determine size of each set
train_dataset_size = int(train_fraction * size_of_original_data)
val_dataset_size = int(val_fraction * size_of_original_data)
test_dataset_size = int(size_of_original_data - train_dataset_size - val_dataset_size)

# Split whole original data into train, val and test datsets
train_dataset, val_dataset, test_dataset = torch.utils.data.random_split(original_data,
                                                                         [train_dataset_size,
                                                                          val_dataset_size,
                                                                          test_dataset_size])
# Sanity checking
print(f" Train set Size: {len(train_dataset)}")
print(f" Val set Size: {len(val_dataset)}")
print(f" Test set Size: {len(test_dataset)}")
#///////////////////////////////////////////////////////////////////////////////

# Making a PyTorch DataLoader Object for the signal training dataset
signal_dataloader = DataLoader(dataset=train_dataset, batch_size=100, shuffle=True)

#////////////////////////MODEL//////////////////////////////////////////////////
#model 
model = nn.Sequential(
nn.Linear(in_features=500, out_features=300),
nn.ReLU(),
nn.Linear(in_features=300, out_features=100),
nn.ReLU(),
nn.Linear(in_features=100, out_features=2)
)
#///////////////////////////////////////////////////////////////////////////////
#Defining a cost function
cost_function = nn.CrossEntropyLoss()

#Define and Set an optimizer object
optim = torch.optim.SGD(model.parameters(), lr=0.05)

#define number of epochs
nr_epochs = 100
#create an empty array to store cost values
training_minibatch_Js =[]
validation_cost =[]
validation_accuracy =[]
training_cost =[]
training_accuracy =[]

#////////////////////////EVALUATION FUNCTION////////////////////////////////////
def evaluate_model_performance(dataset, model):

  # Make a Dataloader for the dataset.
  d_loader = DataLoader(dataset = dataset, batch_size=len(dataset))

  cost_function = nn.CrossEntropyLoss() # For classification evaluation
  model.eval()
  # Make predictions for the eval dataset
  with torch.no_grad():
    for X, y in d_loader:
      raw_y_preds = model(X)

    y_class_preds = raw_y_preds.argmax(dim=1)
    eval_cost = cost_function(raw_y_preds, y).item()
  model.train()

  # compare predictions with true labels and compute performance metric
  # performance metric in this example is classification accuracy
  eval_acc = accuracy_score(y_pred = y_class_preds, y_true = y)

  return eval_cost, eval_acc
#///////////////////////////////////////////////////////////////////////////////
for epoch_i in range(nr_epochs):
  eval_every_kth = 4
  if epoch_i%eval_every_kth ==0: # Eval model very kth epoch.
    model.eval() # set model into evaluate mode 
    # EVALUATE Model performance on whole train and validation dataset
    train_cost, train_acc= evaluate_model_performance(model=model, dataset = train_dataset)
    val_cost, val_acc= evaluate_model_performance(model=model, dataset = val_dataset)
    model.train() # reset model into train mode.
    # track performance measures from both train and val sets
    training_cost.append(train_cost)
    training_accuracy.append(train_acc.item())
    validation_cost.append(val_cost)
    validation_accuracy.append(val_acc.item())
   
  for X_batch, y_batch in signal_dataloader:
    y_preds = model(X_batch) #make prediction on batch
    cost = cost_function(y_preds, y_batch) #compute cost value
    training_minibatch_Js.append(cost.item())
    optim.zero_grad() #zero the grads of all model params
    cost.backward() #compute J gradient of all model params
    optim.step() #take one update step for all model params

# EVALUATE Model performance on whole train and Validation AND TEST dataset
test_cost, test_acc = evaluate_model_performance(model=model, dataset = test_dataset)

#plotting cost functions
plt.figure(figsize=[8,4])
plt.plot(training_minibatch_Js)
plt.xlabel('update step i on mini-batch')
plt.ylabel('Cost')
plt.title('Cost during training on trainset using (per mini-batch)')
# plt.ylim([0.0,4.0])
plt.grid()

#printing test values
print(f'The  value of the test cost is {test_cost}')
print(f'The  value of the test accuracy is {test_acc}')

#plotting cost and accuracy values for training and validation sets. 
plt.figure(figsize=[8,4])
plt.plot(training_cost,'b',validation_cost,'r')
plt.xlabel('Epochs')
plt.ylabel('Cross-entropy Cost')
plt.legend(['Train set','Validation set'])
plt.grid()
plt.show()

plt.figure(figsize=[8,4])
plt.plot(training_accuracy,'b',validation_accuracy,'r')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend(['Train set','Validation set'])
plt.grid()
plt.show()

#printing performance metrics
print(f"Epoch: 0 - Train cost: {training_cost[0]}, - Train Acc: {training_accuracy[0]}")
print(f"Epoch: 0 - val cost: {validation_cost[0]}, - val Acc: {validation_accuracy[0]}")
print('........')
print(f"Epoch: 0 - Train cost: {training_cost[1]}, - Train Acc: {training_accuracy[1]}")
print(f"Epoch: 0 - val cost: {validation_cost[1]}, - val Acc: {validation_accuracy[1]}")
print('........')
print(f"Epoch: 0 - Train cost: {training_cost[2]}, - Train Acc: {training_accuracy[2]}")
print(f"Epoch: 0 - val cost: {validation_cost[2]}, - val Acc: {validation_accuracy[2]}")
print('........')
print(f"Epoch: 0 - Train cost: {training_cost[3]}, - Train Acc: {training_accuracy[3]}")
print(f"Epoch: 0 - val cost: {validation_cost[3]}, - val Acc: {validation_accuracy[3]}")
print('........')
print(f"Epoch: 0 - Train cost: {training_cost[4]}, - Train Acc: {training_accuracy[4]}")
print(f"Epoch: 0 - val cost: {validation_cost[4]}, - val Acc: {validation_accuracy[4]}")
print('........')
print(f"Epoch: 0 - Train cost: {training_cost[5]}, - Train Acc: {training_accuracy[5]}")
print(f"Epoch: 0 - val cost: {validation_cost[5]}, - val Acc: {validation_accuracy[5]}")
print('........')

#Task D: Image Classi cation of FashionMNIST using FANNs

#////////////////////////DOWNLOADING DATA///////////////////////////////////////
# Download training data from open datasets.
training_data = datasets.FashionMNIST(
  root="data",
  train=True,
  download=True,
  transform=ToTensor(),
)

# Download test data from open datasets.
test_data = datasets.FashionMNIST(
  root="data",
  train=False,
  download=True,  
  transform=ToTensor(),
)
#///////////////////////////////////////////////////////////////////////////////

data = training_data 
size_of_data = len(data)

#////////////////////////SPLITTING//////////////////////////////////////////////
#Specify split fractions:
train_fraction = 0.80
val_fraction = 0.20

# Determine size of each set
train_dataset_size = int(train_fraction * size_of_data)
val_dataset_size = int(val_fraction * size_of_data)

# Split whole original data into train and val
train_dataset, val_dataset = torch.utils.data.random_split(data,[train_dataset_size,
                                                                 val_dataset_size])

# Sanity checking
print(f" Train set Size: {len(train_dataset)}")
print(f" Val set Size: {len(val_dataset)}")
#///////////////////////////////////////////////////////////////////////////////

# Making a PyTorch DataLoader Object for the fashion training dataset
fashion_dataloader = DataLoader(dataset=train_dataset, batch_size=100, shuffle=True)

#////////////////////////////MODEL//////////////////////////////////////////////
model = nn.Sequential(nn.Flatten(1,-1),
                      nn.Linear(784, 300),
                      nn.ReLU(),
                      nn.Linear(300, 100),
                      nn.ReLU(),
                      nn.Linear(100, 10))             
# #/////////////////////////////////////////////////////////////////////////////
#Defining a cost function
cost_function = nn.CrossEntropyLoss()

#Define and Set an optimizer object
optim = torch.optim.SGD(model.parameters(), lr=0.05)

#define number of epochs
nr_epochs = 40
#create an empty array to store cost values
training_minibatch_Js =[]
validation_cost =[]
validation_accuracy =[]
training_cost =[]
training_accuracy =[]

#////////////////////////EVALUATION FUNCTION////////////////////////////////////
def evaluate_model_performance(dataset, model):

  # Make a Dataloader for the dataset.
  d_loader = DataLoader(dataset = dataset, batch_size=len(dataset))

  cost_function = nn.CrossEntropyLoss() # For classification evaluation
  model.eval()
  # Make predictions for the eval dataset
  with torch.no_grad():
    for X, y in d_loader:
      raw_y_preds = model(X)

    y_class_preds = raw_y_preds.argmax(dim=1)
    eval_cost = cost_function(raw_y_preds, y).item()
  model.train()

  # compare predictions with true labels and compute performance metric
  # performance metric in this example is classification accuracy
  eval_acc = accuracy_score(y_pred = y_class_preds, y_true = y)

  return eval_cost, eval_acc
#////////////////////////////////TRAINING///////////////////////////////////////
for epoch_i in range(nr_epochs):
  eval_every_kth = 5
  if epoch_i%eval_every_kth ==0: # Eval model very kth epoch.
    model.eval() # set model into evaluate mode 
    # EVALUATE Model performance on whole train and validation dataset
    train_cost, train_acc= evaluate_model_performance(model=model, dataset = train_dataset)
    val_cost, val_acc= evaluate_model_performance(model=model, dataset = val_dataset)
    model.train() # reset model into train mode.
    # track performance measures from both train and val sets
    training_cost.append(train_cost)
    training_accuracy.append(train_acc.item())
    validation_cost.append(val_cost)
    validation_accuracy.append(val_acc.item())
   
  for X_batch, y_batch in fashion_dataloader:
    y_preds = model(X_batch) #make prediction on batch
    cost = cost_function(y_preds, y_batch) #compute cost value
    training_minibatch_Js.append(cost.item())
    optim.zero_grad() #zero the grads of all model params
    cost.backward() #compute J gradient of all model params
    optim.step() #take one update step for all model params

# EVALUATE Model performance on whole train and Validation AND TEST dataset
test_cost, test_acc = evaluate_model_performance(model=model, dataset = test_data)

#plotting cost functions
plt.figure(figsize=[8,4])
plt.plot(training_minibatch_Js)
plt.xlabel('update step i on mini-batch')
plt.ylabel('Cost')
plt.title('Cost during training on trainset using (per mini-batch)')
# plt.ylim([0.0,4.0])
plt.grid()

#printing test values
print(f'The  value of the test cost is {test_cost}')
print(f'The  value of the test accuracy is {test_acc}')

#plotting cost and accuracy values for training and validation sets. 
figure(figsize=(8, 5))
plt.plot(training_cost,'b',validation_cost,'r')
plt.xlabel('Epochs')
plt.ylabel('Cross-entropy Cost')
plt.legend(['Train set','Validation set'])
plt.grid()
plt.show()

figure(figsize=(8, 5))
plt.plot(training_accuracy,'b',validation_accuracy,'r')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend(['Train set','Validation set'])
plt.grid()
plt.show()