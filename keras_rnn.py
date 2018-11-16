import keras
import keras.backend as K
from keras.layers import RNN

class MinimalRNNCell(keras.layers.Layer):
    def __init__(self,units):
        self.units = units
        self.state_size = units #??
        super(MinimalRNNCell,self).__init__()
        return
    
    def build(self,input_shape):
        self.kernel = self.add_weight(shape=(input_shape[-1],self.units),
                                      initializer='uniform', name='kernel')
        self.r_kernel = self.add_weight(shape=(self.units,self.units),
                                      initializer='uniform', name='r_kernel')
        self.built = True #??
        return
    
    def call(self,inputs,states):
        prev_out = states[0]
        h = K.dot(inputs,self.kernel)
        output = h+K.dot(prev_out,self.r_kernel)
        return output, [output]

cell = [MinimalRNNCell(32), MinimalRNNCell(28)]
# or can be cells = []
# None - for time distribution?
x = keras.Input((None,5))
layer = RNN(cell,return_sequences=True)
y = layer(x)

from keras.models import Model
model = Model(inputs=[x],outputs=[y])
