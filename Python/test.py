import numpy
from sklearn import neural_network
import joblib

sample_player0 = numpy.load('C:\\Users\\Laouen\\PycharmProjects\\Awale\\Samples\\sample_player0.npy')
target_player0 = numpy.load('C:\\Users\\Laouen\\PycharmProjects\\Awale\\Samples\\target_player0.npy')
sample_player1 = numpy.load('C:\\Users\\Laouen\\PycharmProjects\\Awale\\Samples\\sample_player1.npy')
target_player1 = numpy.load('C:\\Users\\Laouen\\PycharmProjects\\Awale\\Samples\\target_player1.npy')


n0 = len(sample_player0)
n1 = len(sample_player1)
clf_player0 = neural_network.MLPClassifier(hidden_layer_sizes=(100,), activation='relu', alpha=0.0001, max_iter=800)
clf_player1 = neural_network.MLPClassifier(hidden_layer_sizes=(100,), activation='relu', alpha=0.0001, max_iter=800)
clf_player0.fit(sample_player0[:n0 // 2], target_player0[:n0 // 2])
clf_player1.fit(sample_player1[:n1 // 2], target_player1[:n1 // 2])
# expected_player0 = target_player0[n0 // 2:]
# predicted_player0 = clf_player0.predict(sample_player0[n0 // 2:])
# expected_player1 = target_player1[n1 // 2:]
# predicted_player1 = clf_player1.predict(sample_player1[n1 // 2:])
# print(target_player0[:n0 // 2])
# print(expected_player0)
# print(predicted_player0)
# print(target_player1[:n1 // 2])
# print(expected_player1)
# print(predicted_player1)