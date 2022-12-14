# -*- coding: utf-8 -*-
"""ِAssignment3_AI_PartE.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bWe5Ji3NRUTxpSPEkPiSsceot_vPeZ_e
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
import torchvision

#////////////////////////DOWNLOADING DATA///////////////////////////////////////

# Download training data from open datasets.
training_data = datasets.FashionMNIST(
  root="data",
  train=True,
  download=True,
  transform=ToTensor()
)

# Download test data from open datasets.
test_data = datasets.FashionMNIST(
  root="data",
  train=False,
  download=True,  
  transform=ToTensor()
)
#///////////////////////////////////////////////////////////////////////////////

#////////////////////////SPLITTING DATA/////////////////////////////////////////
data = training_data 
size_of_data = len(data)

#Specify split fractions:
train_fraction = 0.70
val_fraction = 0.30

# Determine size of each set
train_dataset_size = int(train_fraction * size_of_data)
val_dataset_size = int(val_fraction * size_of_data)

# Split whole original data into train and val 
train_dataset, val_dataset = torch.utils.data.random_split(data,
                                                           [train_dataset_size,
                                                            val_dataset_size])
# Sanity checking
print(f" Train set Size: {len(train_dataset)}")
print(f" Val set Size: {len(val_dataset)}")

#///////////////////////////////////////////////////////////////////////////////

# Making a PyTorch DataLoader Objects for the training and validation datasets
train_dataloader = DataLoader(dataset=train_dataset, batch_size=64, shuffle=True)
val_dataloader = DataLoader(dataset=val_dataset, batch_size=64, shuffle=True)

plt.imshow(training_data[10][0][0])

#////////////////////////////MODEL//////////////////////////////////////////////
def LeNet5():
  model = nn.Sequential(
      nn.Conv2d(1,6,5, padding=2),
      nn.ReLU(),
      nn.AvgPool2d(2, stride=2),

      nn.Conv2d(6,16, 5, padding=0),
      nn.ReLU(),
      nn.AvgPool2d(2, stride=2),

      nn.Flatten(),
      nn.Linear(400,120),
      nn.Linear(120,84),
      nn.Linear(84,10)
  )
  return model
#///////////////////////////////////////////////////////////////////////////////

#define number of epochs
nr_epochs = 40

#create an empty array to store cost values
training_minibatch_Js =[]
validation_cost =[]
validation_accuracy =[]
training_cost =[]
training_accuracy =[]

cnn = LeNet5()

#Defining a cost function
cost_function = nn.CrossEntropyLoss()

#Define and Set an optimizer object
optim = torch.optim.Adam(cnn.parameters(), lr=0.001)

#////////////////////////////EVALUATION/////////////////////////////////////////
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
  eval_every_kth = 1
  if epoch_i%eval_every_kth ==0: # Eval model very kth epoch.
    cnn.eval() # set model into evaluate mode 
    # EVALUATE Model performance on whole train and validation dataset
    train_cost, train_acc= evaluate_model_performance(model=cnn, dataset = train_dataset)
    val_cost, val_acc= evaluate_model_performance(model=cnn, dataset = val_dataset)
    cnn.train() # reset model into train mode.
    # track performance measures from both train and val sets
    training_cost.append(train_cost)
    training_accuracy.append(train_acc.item())
    validation_cost.append(val_cost)
    validation_accuracy.append(val_acc.item())
   
  for X_batch, y_batch in train_dataloader:
    y_preds = cnn(X_batch) #make prediction on batch
    cost = cost_function(y_preds, y_batch) #compute cost value
    training_minibatch_Js.append(cost.item())
    optim.zero_grad() #zero the grads of all model params
    cost.backward() #compute J gradient of all model params
    optim.step() #take one update step for all model params

#print cost value
print(f'The final value of the cost function is {cost}')

#plotting cost functions
plt.figure(figsize=[8,4])
plt.plot(training_minibatch_Js)
plt.xlabel('update step i on mini-batch')
plt.ylabel('Cost')
plt.title('Cost during training on trainset using (per mini-batch)')
# plt.ylim([0.0,4.0])
plt.grid()

# EVALUATE Model performance on whole train and Validation AND TEST dataset
test_cost, test_acc = evaluate_model_performance(model=cnn, dataset = test_data)

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