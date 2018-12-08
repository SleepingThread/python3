from matplotlib import pyplot as plt

def bar_fromarray(array_list,array_labels,width=0.8,color_list=None):
    fig,ax = plt.subplots()
    
    if color_list is None:
        color_list = [(0.5,0,0),(0,0.5,0)]
    color_ind = 0
    
    bar_x = []
    bar_y = []
    colors = []
    ind = 0
    
    prev_ind = 0
    
    x_ticks = []
    x_ticks_labels = []
    
    for _array,_label in zip(array_list,array_labels):
        _array = _array.reshape((-1,))
        color_ind = (color_ind+1)%len(color_list)
        for _el in _array.reshape((-1,)):
            bar_x.append(ind)
            colors.append(color_list[color_ind])
            bar_y.append(_el)    
            ind += 1

        x_ticks.append(prev_ind+(ind-1-prev_ind)/2.0)
        x_ticks_labels.append(_label)
        prev_ind = ind
    
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_ticks_labels,rotation='vertical')
    ax.bar(bar_x,bar_y,color=colors,width=width)
    
    return fig,ax