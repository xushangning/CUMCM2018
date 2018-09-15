# A deep-learning classifier for decision making.
# All CNCs will be classified into 2 status: be served next or not.
# The parameters for the classifier can be:
# 1. The working status of the CNC. (How much time left for processing)
# 2. The position of the RGV.
# 3. The load time for this CNC.
# 4. The last step the CNC does
# The return will be a whole sequence of the work line.

import numpy as np
import tensorflow as tf
import time
import pandas as pd


# training parameters
data = pd.read_csv("training_set.csv")
X_train, y_train =

y_train = tf.concat([1 - y_train, y_train], 1)

learning_rate = 0.001
training_epochs = 30
batch_size = 40
display_step = 1

n_samples = X_train.shape[0]
n_features = 9
n_class = 2
x = tf.placeholder(tf.float32, [None, n_features])
y = tf.placeholder(tf.float32, [None, n_class])

W = tf.Variable(tf.zeros([n_features, n_class]))
b = tf.Variable(tf.zeros([n_class]))

pred = tf.nn.softmax(tf.matmul(x, W) + b)

cost = tf.reduce_mean(-tf.reduce_sum(y*tf.log(pred), reduction_indices=1))

optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

init = tf.initialize_all_variables()

startTime = time.clock()

saver = tf.train.Saver()
model_path = "model\model.ckpt"

with tf.Session() as sess:
    sess.run(init)
    for
