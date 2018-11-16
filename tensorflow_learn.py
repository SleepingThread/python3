from numpy.random import seed
seed(1)
import tensorflow as tf
tf.set_random_seed(2)

from tensorflow.python.client import device_lib

def get_available_gpus():
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos if x.device_type == 'GPU']

tf_config = tf.ConfigProto()
if len(get_available_gpus())>0:
	tf_config.gpu_options.per_process_gpu_memory_fraction = 0.3

with tf.Session(config=tf_config) as sess:
	pass

#keras + tensorflow
#tbCallBack = keras.callbacks.TensorBoard(log_dir=log_dir,histogram_freq=1,write_graph=True,write_images=True,write_grads=True,batch_size=128)


