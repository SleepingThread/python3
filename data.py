import numpy as np

#def GenerateTimeseries(data,labels,look_back,stride,sampling_rate):
#look_back_data
#look_forward_data
#stride_data
#stride_labels
# sampling_rate
# padding = 'none' | 'zero'

def GenerateTimeseries(data,labels,
                       look_back_data=0,look_back_labels=0,look_forward_data=0,look_forward_labels=0,
                       stride=1,
                       start = 0, end = 0,
                       sampling_rate_data=1,sampling_rate_labels=1, 
                       padding = 'none',
                       reverse_data = False, reverse_labels=False):
    """
    padding = 'none' | 'zero'
    """
    
    data = np.asarray(data)
    labels = np.asarray(labels)
    
    if len(data)!=len(labels):
        raise Exception("len(data)!=len(labels)")
        
    if len(data)==0:
        return [],[]
    
    if look_back_data<0 or look_back_labels<0:
        raise Exception("look_back must be >= 0")
    elif look_forward_data<0 or look_forward_labels<0:
        raise Exception("look_forward must be >= 0")
    
    if (data[0].shape!=() or labels[0].shape!=()) and padding=='zero':
        raise Exception("Cannot use zero filling with shape "+data.shape)
    
    max_look_back = max(look_back_data*sampling_rate_data,look_back_labels*sampling_rate_labels)
    max_look_forward = max(look_forward_data*sampling_rate_data,look_forward_labels*sampling_rate_labels)
    
    new_data = []
    new_labels = []
    
    if end<=0:
        end = len(data)-end
        
    data = data[start:end]
    labels = labels[start:end]
    pos_start = 0
    pos_end = len(data)
    
    if padding=='none':
        pos_start = start+max_look_back
        pos_end = end-max_look_forward
    elif padding=='zero':
        pos_start = start
        pos_end = end
    else:
        raise Exception("Unknown padding")
    
    #len(data)==len(labels)
    #start<=_pos - look_back_data, _pos+look_forward_data<len(data)-end
    #start<=_pos - look_back_labels, _pos+look_forward_labels<len(data)-end
    
    for _pos in range(pos_start,pos_end,stride):
        n_look_back = min(look_back_data*sampling_rate_data,_pos-start)//sampling_rate_data
        n_look_forward = min(end-_pos-1,look_forward_data*sampling_rate_data)//sampling_rate_data
        real_look_back = n_look_back*sampling_rate_data
        real_look_forward = n_look_forward*sampling_rate_data
        data_timeseries = data[_pos-real_look_back:_pos+real_look_forward+1:sampling_rate_data]
        if n_look_back<look_back_data or n_look_forward<look_forward_data:
            _left = max(0,look_back_data-n_look_back)
            _right = max(0,look_forward_data-n_look_forward)
            data_timeseries = np.pad(data_timeseries,(_left,_right),mode='constant')
        
        n_look_back = min(look_back_labels*sampling_rate_labels,_pos-start)//sampling_rate_labels
        n_look_forward = min(end-_pos-1,look_forward_labels*sampling_rate_labels)//sampling_rate_labels
        real_look_back = n_look_back*sampling_rate_labels
        real_look_forward = n_look_forward*sampling_rate_labels
        labels_timeseries = labels[_pos-real_look_back:_pos+real_look_forward+1:sampling_rate_labels]
        if n_look_back<look_back_labels or n_look_forward<look_forward_labels:
            _left = max(0,look_back_labels-n_look_back)
            _right = max(0,look_forward_labels-n_look_forward)
            labels_timeseries = np.pad(labels_timeseries,(_left,_right),mode='constant')
        
        if not reverse_data:
            new_data.append(data_timeseries)
        else:
            new_data.append(np.flip(data_timeseries))
            
        if not reverse_labels:
            new_labels.append(labels_timeseries)
        else:
            new_labels.append(np.flip(labels_timeseries))
        
    return new_data,new_labels
