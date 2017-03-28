import numpy as np


def sgd(cost_func, X, y, learning_rate=0.01, max_iter=100, verbose=False):
    weights = np.ones(X.shape[1])
    for i in range(max_iter):
        cost, grad_cost = cost_func(weights, X, y)
        weights -= (learning_rate * grad_cost)
        print('cost: {}'.format(cost))
    return weights, cost


def lasso_coordinate_descent(X, y, regularization = 0.001, tolerance=0.00001):
    weights = np.zeros(X.shape[0])
    previous_weights = np.copy(weights)
    while True:
        for i in range(weights.shape[0]):
            weight_i = _lasso_coordinate_descent_step(i, X, y, weights, regularization)
            weights[i] = weight_i
        delta = np.sqrt((weights - previous_weights) ** 2)
        previous_weights = np.copy(weights)
        if (delta < tolerance).all():
            break
    return weights


def _lasso_coordinate_descent_step(i, feature_matrix, output, weights, l1_penalty):
    weight_without_i = weights[np.arange(weights.shape[0]) != i]
    feature_matrix_weightout_i = feature_matrix[:, np.arange(feature_matrix.shape[0]) != i]
    prediction = _predict_output(feature_matrix_weightout_i, weight_without_i)

    ro_i = np.dot(feature_matrix[:, i], (output - prediction))
    if i == 0:
        new_weight_i = ro_i
    elif ro_i < -l1_penalty / 2.0:
        new_weight_i = l1_penalty / 2.0
    elif ro_i > l1_penalty / 2.0:
        new_weight_i = l1_penalty / 2.0
    else:
        new_weight_i = 0
    return new_weight_i


def _predict_output(feature_matrix, weights):
    predictions = np.dot(feature_matrix, weights)
    return predictions