import numpy as np


# Define the impurity measure (Gini impurity)
def gini(data):
    classes = np.unique(data[:, -1])
    gini = 1
    for c in classes:
        p = (data[:, -1] == c).mean()
        gini -= p ** 2
    return gini


# Define the function to split the data
def split(data, feature, threshold):
    left = data[data[:, feature] < threshold]
    right = data[data[:, feature] >= threshold]
    return left, right


# Define the function to find the best split
def find_best_split(data):
    best_feature = None
    best_threshold = None
    best_impurity = None
    for feature in range(data.shape[1] - 1):
        for threshold in np.unique(data[:, feature]):
            left, right = split(data, feature, threshold)
            impurity = (left.shape[0] / data.shape[0]) * gini(left) + (right.shape[0] / data.shape[0]) * gini(right)
            if best_impurity is None or impurity < best_impurity:
                best_feature = feature
                best_threshold = threshold
                best_impurity = impurity
    return best_feature, best_threshold, best_impurity


# Define the function to build the decision tree
def build_tree(data, depth=0, max_depth=None):
    feature, threshold, impurity = find_best_split(data)
    if impurity == 0 or (max_depth is not None and depth >= max_depth):
        return data[:, -1][0]
    left, right = split(data, feature, threshold)
    return {'feature': feature, 'threshold': threshold,
            'left': build_tree(left, depth + 1, max_depth),
            'right': build_tree(right, depth + 1, max_depth)}


# Define the function to classify new samples
def classify(sample, tree):
    if type(tree) is not dict:
        return tree
    if sample[tree['feature']] < tree['threshold']:
        return classify(sample, tree['left'])
    else:
        return classify(sample, tree['right'])


# load the iris dataset
from sklearn import datasets

iris = datasets.load_iris()
X = iris.data
y = iris.target
# append the target variable to the data
data = np.hstack((X, y.reshape(-1, 1)))

# Build the decision tree
tree = build_tree(data, max_depth=2)

# classify new samples
new_sample = [5, 3, 1, 0.2]
class_name = classify(new_sample, tree)
print(class_name)
