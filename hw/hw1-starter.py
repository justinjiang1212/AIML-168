'''
Before attemping the problem, please familiarize with pandas and numpy
libraries. Tutorials can be found online:
http://pandas.pydata.org/pandas-docs/stable/tutorials.html
https://docs.scipy.org/doc/numpy-dev/user/quickstart.html

Please COMMENT OUT the second part before you finish that step. Otherwise, you
won't be able to run the program because of errors.

Note:
1. Please read the instructions and hints carefully, and use the name of the
variables we provided, otherwise, the function may not work.

2. Placeholder values are given for the variables needed, they need to be
replaced with your own code

3. Remember to comment out the TODO comment after you finish each part.
'''

import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


if __name__ == '__main__':

  # Load the four data points of this problem
  X = np.array([0, 2, 3, 4])
  y = np.array([1, 3, 6, 8])

  # Plot four data points on the plot
  plt.style.use('ggplot')
  plt.plot(X, y, 'ro')

  # TODO: Replace the m_opt and b_opt values with the values you calculuated,
  # note that y=mx+b
  '''*** START YOUR CODE HERE ***'''
  m_opt = 0
  b_opt = 0
  '''*** END YOUR CODE HERE ***'''

  # TODO: Generate 100 points along the line of optimal linear fit
  # HINT:
  #   1) Use np.linspace to get the x-coordinate of 100 points
  #   2) Calculate the y-coordinate of those 100 points with the m_opt and
  #      b_opt, remember y=mx+b
  #   3) Use a.reshape(-1,1), where a is a np.array, to reshape the array to
  #      appropraite shape for generating plot

  X_space = []
  y_space = []

  '''*** START YOUR CODE HERE ***'''

  '''*** END YOUR CODE HERE ***'''

  # Plot the optimal learn fit you obtained and save it to your current folder
  plt.plot(X_space, y_space)
  plt.savefig('original-fit.png', format='png')
  plt.close()

  # ============= Optimal linear fit with random data points=================

  # Variables to start with
  mu, sigma, sampleSize = 0, 1, 100

  # TODO: Generate white Gaussian noise
  # HINT: Use np.random.normal to generate noise

  noise = []

  '''*** START YOUR CODE HERE ***'''

  '''*** END YOUR CODE HERE ***'''

  # TODO: Generate y-coordinate of the 100 points with noise
  # HINT:
  #  1) Use X_space created in the previous part above as the x-coordinates
  #  2) In this case, y = mx + b + noise

  y_space_rand = np.zeros(len(X_space))

  '''*** START YOUR CODE HERE ***'''

  '''*** END YOUR CODE HERE ***'''

  # TODO: calculate the new parameters for optimal linear fit using the 100
  # new points generated above
  # HINT:
  #   1) Use np.ones_like to create a column of 1
  #   2) Use np.hstack to stack column of ones on X_space to create
  #      X_space_stacked
  #   3) Use np.linalg.solve to solve W_opt following the normal equation:
  #   X.T * X * W_opt = X.T * y

  X_space_stacked = X_space  # need to be replaced following hint 1 and 2
  W_opt = None

  '''*** START YOUR CODE HERE ***'''

  '''*** END YOUR CODE HERE ***'''

  # Get the new m, and new b from W_opt obtained above
  b_rand_opt, m_rand_opt = W_opt.item(0), W_opt.item(1)

  # TODO: Generate the y-coordinate of 100 points with the new parameters
  #    obtained
  # HINT:
  #   1) Use X_space for x-coordinates (same)
  #   2) y = mx + b
  #   3) Make sure the array is in appropraite shape using a.reshape(-1,1)

  y_pred_rand = []

  '''*** START YOUR CODE HERE ***'''

  '''*** END YOUR CODE HERE ***'''

  ## Generate plot
  # Plot original data points and line
  plt.plot(X, y, 'ro')
  orig_plot, = plt.plot(X_space, y_space, 'r')

  # Plot the generated 100 points with white gaussian noise and the new line
  plt.plot(X_space, y_space_rand, 'bo')
  rand_plot, = plt.plot(X_space, y_pred_rand, 'b')

  # Set up legend and save the plot to the current folder
  plt.legend((orig_plot, rand_plot),
             ('original fit', 'fit with noise'), loc='best')
  plt.savefig('fit-with-noise.png', format='png')
  plt.close()
