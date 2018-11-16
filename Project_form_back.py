import torch
import numpy as np

class Data(object):
	def __init__(self,data,labels):
		self.data = data
		self.labels = labels
		return

	def split(self,l):
		"""
		param l:

		return: list of splitted dataset
		"""

		return

	@staticmethod
	def loadData(path,**kwargs):
		
		# load data and labels from path

		return Data(data,labels)

	@staticmethod
	def makeData(data_shape,labels_shape):
		data = np.random.rand(*data_shape)
		labels = np.random.rand(*labels_shape)
		return Data(data,labels)

class DataProcessor(object):
	def __init__(self, data):
		self._build(data)
		return

	def rebuild(self,data):
		self._build(data)
		return

	def _build(self,data):
		"""
		Method we can redefine anywhere
		Now it do nothing
		"""
		return

	def preprocess(self,data):
		# make check if data - instance of Data
		if isinstance(data,Data):
			proc_data = Data()
			proc_data.data = np.array(data.data)
			proc_data.labels = np.array(data.labels)
		else:
			# data - labels only, i.e. prediction
			proc_data = np.array(data)

		return proc_data

	def postprocess(self,data):
		proc_data = np.array(data)
		return proc_data

class ModelBase(object):
	"""
	Realization of model operation required

	LOAD , SAVE methods!!!

	TRACK 

	+,- operations

	+,- delta to weights and check quality
		(Quality local map)

	"""

	def __init__(self,params):
		return

	def fit(self,data,validation=None,batch_size=32,\
		epochs = 1,loss="mse",optimizer="sgd"):
		"""
		loss,optimizer - strings or objects
		"""
		return

	def predict(self,data):
		return

class Model1(ModelBase):
	"""
	Only init method, where model build,
		to redefine
	"""
	def __init__(self,<many many parameters>):
		super(Model1,self).__init__(<param>)

		self.setTorchModel(<created_model>)

		return

class TwoLayerNet(torch.nn.Module):
    def __init__(self, D_in, H, D_out):
        """
        In the constructor we instantiate two nn.Linear modules and assign them as
        member variables.
        """
        super(TwoLayerNet, self).__init__()
        self.linear1 = torch.nn.Linear(D_in, H)
        self.linear2 = torch.nn.Linear(H, D_out)

    def forward(self, x):
        """
        In the forward function we accept a Tensor of input data and we must return
        a Tensor of output data. We can use Modules defined in the constructor as
        well as arbitrary operators on Tensors.
        """
        h_relu = self.linear1(x).clamp(min=0)
        y_pred = self.linear2(h_relu)
        return y_pred
