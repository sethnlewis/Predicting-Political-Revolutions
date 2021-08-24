import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import f1_score, precision_score, accuracy_score, recall_score
from sklearn.metrics import plot_confusion_matrix


def evaluate_model_performance(grid, x_test, y_test):
    
    # Calculate predictions
    pred = grid.best_estimator_.predict(x_test)
    
    # Print metrics
    print_scores(pred, y_test)
    
    # Display confusion matrix
    plt.figure()
    plot_confusion_matrix(grid.best_estimator_, x_test, y_test)
    plt.show();
    
    return grid.best_estimator_


def print_scores(prediction, actual):
    print(f'- f1: {f1_score(actual, prediction)}')
    print(f'- accuracy: {accuracy_score(actual, prediction)}')
    print(f'- precision: {precision_score(actual, prediction)}')
    print(f'- recall: {recall_score(actual, prediction)}')
    