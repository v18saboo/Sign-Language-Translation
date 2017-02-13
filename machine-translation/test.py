from seq2seq import AttentionSeq2Seq
import numpy as np
from keras.utils.test_utils import keras_test

input_length = 10
input_dim = 2

output_length = 8
output_dim = 3

samples = 100

@keras_test
def test_AttentionSeq2Seq():
	x = np.random.random((samples, input_length, input_dim))
	y = np.random.random((samples, output_length, output_dim))

	models = []
	models += [AttentionSeq2Seq(output_dim=output_dim, output_length=output_length, input_shape=(input_length, input_dim))]
	#models += [AttentionSeq2Seq(output_dim=output_dim, output_length=output_length, input_shape=(input_length, input_dim), depth=2)]
	#models += [AttentionSeq2Seq(output_dim=output_dim, output_length=output_length, input_shape=(input_length, input_dim), depth=3)]

	for model in models:
		model.compile(loss='mse', optimizer='sgd')
		model.fit(x, y, nb_epoch=1)

test_AttentionSeq2Seq();