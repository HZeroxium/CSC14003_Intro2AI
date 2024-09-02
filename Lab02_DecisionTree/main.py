from ucimlrepo import fetch_ucirepo  # type: ignore
from pandas import DataFrame  # type: ignore
import pandas as pd  # type: ignore
from sklearn.model_selection import train_test_split  # type: ignore
from sklearn.tree import DecisionTreeClassifier  # type: ignore
from sklearn import tree  # type: ignore
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score  # type: ignore
import graphviz  # type: ignore
import os
import matplotlib.pyplot as plt  # type: ignore
import seaborn as sns  # type: ignore
import numpy as np  # type: ignore

# Fetch the dataset from the UCI ML repository
breast_cancer_wisconsin_diagnostic = fetch_ucirepo(id=17)

# Extract the features and labels from the dataset
data: DataFrame = breast_cancer_wisconsin_diagnostic.data  # type: ignore
features: DataFrame = data.features  # type: ignore
labels: DataFrame = data.targets  # type: ignore
headers: list = data.headers  # type: ignore

# Print the headers of the data
print(headers)

# Define the proportions for train-test splits
proportions = [(0.4, 0.6), (0.6, 0.4), (0.8, 0.2), (0.9, 0.1)]
data_splits = []

# Split the dataset into training and testing sets for each proportion
for train_size, test_size in proportions:
    X_train, X_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=test_size,
        train_size=train_size,
        stratify=labels,
        random_state=42,
        shuffle=True,
    )
    data_splits.append((X_train, X_test, y_train, y_test))


def plot_class_distribution(labels, title):
    if isinstance(labels, pd.DataFrame):
        labels = labels.iloc[:, 0]  # Chọn cột đầu tiên nếu labels là DataFrame
    elif isinstance(labels, np.ndarray) and labels.ndim > 1:
        labels = labels.ravel()  # Chuyển đổi mảng 2 chiều thành mảng 1 chiều

    sns.countplot(x=labels)
    plt.title(title)
    plt.xlabel("Class")
    plt.ylabel("Count")
    plt.show()


# Visualize the distribution in the original dataset
plot_class_distribution(labels, "Original Dataset")

# # Visualize the distribution in each train/test split
for i, (X_train, X_test, y_train, y_test) in enumerate(data_splits):
    plot_class_distribution(y_train, f"Train Set Distribution (Split {i})")
    plot_class_distribution(y_test, f"Test Set Distribution (Split {i})")


# Set up the PATH for Graphviz to ensure it can find the 'dot' executable
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

# Train a Decision Tree Classifier for each train-test split and visualize the tree
classifiers = []
for i, (X_train, X_test, y_train, y_test) in enumerate(data_splits):
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)
    classifiers.append(clf)

    # Export the tree structure to a Graphviz dot file
    dot_data = tree.export_graphviz(
        clf, out_file=None, filled=True, rounded=True, special_characters=True
    )
    # Visualize the decision tree
    graph = graphviz.Source(dot_data)
    print(f"Decision Tree {i}")
    graph.render(f"decision_tree_{i}")

# Evaluate the performance of each classifier
for clf, (X_train, X_test, y_train, y_test) in zip(classifiers, data_splits):
    y_pred = clf.predict(X_test)
    print("Classification Report:")
    report = classification_report(y_test, y_pred, output_dict=True)
    print(classification_report(y_test, y_pred))

    print("Confusion Matrix:")
    matrix = confusion_matrix(y_test, y_pred)
    print(matrix)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # Basic interpretation
    print("\nInterpretation:")
    print(
        f"Precision for Benign: {report['B']['precision']:.2f}, "
        f"Precision for Malignant: {report['M']['precision']:.2f}"
    )
    print(
        f"Recall for Benign: {report['B']['recall']:.2f}, "
        f"Recall for Malignant: {report['M']['recall']:.2f}"
    )
    print(f"Overall Accuracy: {accuracy:.2f}")
    print("-" * 40)

# Experiment with different tree depths and measure accuracy
depths = [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
accuracy_scores = []

for depth in depths:
    # Train a Decision Tree Classifier with a specified max depth
    clf = DecisionTreeClassifier(max_depth=depth, random_state=42)
    clf.fit(
        data_splits[2][0], data_splits[2][2]
    )  # Using the third data split (0.8/0.2)
    y_pred = clf.predict(data_splits[2][1])
    accuracy = accuracy_score(data_splits[2][3], y_pred)
    accuracy_scores.append(accuracy)

    # Visualize the decision tree for the current depth
    dot_data = tree.export_graphviz(
        clf, out_file=None, filled=True, rounded=True, special_characters=True
    )
    graph = graphviz.Source(dot_data)
    graph.render(f"decision_tree_depth_{depth}")

# Display the accuracy scores in a table
print("Max Depth vs. Accuracy")
for depth, accuracy in zip(depths, accuracy_scores):
    print(f"Max Depth: {depth}, Accuracy: {accuracy}")

import pandas as pd

# Create a DataFrame to store max_depth and accuracy
df_accuracy = pd.DataFrame({"Max Depth": depths, "Accuracy": accuracy_scores})

# Display the table
print(df_accuracy)

# Plotting the accuracy as a function of max_depth
plt.figure(figsize=(10, 6))
plt.plot(depths, accuracy_scores, marker="o")
plt.xlabel("Max Depth")
plt.ylabel("Accuracy")
plt.title("Accuracy vs Max Depth")
plt.grid(True)
plt.show()
