import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns

# Fungsi untuk menampilkan confusion matrix dengan garis pada kotaknya
def plot_confusion_matrix(y_true, y_pred, classes):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=classes,  linewidths=1, linecolor='black', square=True, yticklabels=classes[::-1])
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Values')
    plt.ylabel('True Values')
    plt.show()

# Contoh data
y_true = np.array([0, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1])
y_pred = np.array([2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2])
class_names = ['Normal', 'Stres Ringan', 'Stres Sedang', 'Stres Berat']

# Menampilkan confusion matrix dengan garis pada kotaknya
plot_confusion_matrix(y_true, y_pred, class_names)
