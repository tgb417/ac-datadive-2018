import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
def summary(df):
    """Takes a DataFrame and creates a summary, does different things if object or numeric features.  """
    summary_list = []
    print 'SHAPE', df.shape
    
    for i in df.columns:
        vals = df[i]    
        if df[i].dtype == 'O':
            try:
                most_frequent = Counter(df[i].tolist()).most_common(1)
                uniq = vals.nunique()
            except TypeError:
                most_frequent = 'NA'
                uniq = 'NA'
            summary_list.append([i,
                                 vals.dtype, 
                                 'NA', 
                                 'NA', 
                                 most_frequent,
                                 uniq, 
                                 sum(pd.isnull(vals)),
                                 sum(pd.isnull(vals))/(1.0*len(df))])
        elif df[i].dtype == '<M8[ns]':
            most_frequent = Counter(df[i].tolist()).most_common(1)
            summary_list.append([i,
                                 vals.dtype, 
                                 vals.min(), 
                                 vals.max(), 
                                 most_frequent,
                                 vals.nunique(), 
                                 sum(pd.isnull(vals)),
                                 sum(pd.isnull(vals))/(1.0*len(df))])
        else:
            summary_list.append([i,
                                 vals.dtype, 
                                 vals.min(), 
                                 vals.max(), 
                                 vals.mean(),
                                 vals.nunique(), 
                                 sum(pd.isnull(vals)),
                                 sum(pd.isnull(vals))/(1.0*len(df))])
    return pd.DataFrame(summary_list, columns=['col','datatype','min','max','mean_or_most_common','num_uniq','null_count','null_pct'])

    
def color_obeject(val):
    """
    Color the "Object" rows in red - just to help in looking at those fields
    """
    if val == 'O':
        color = 'red'
    elif val == '<M8[ns]':
        color = 'blue'
    else:
        color = 'black'
    return 'color: %s' % color

def color_code_summary(df):
    """Then apply the color to the DateFrame"""
    s = summary(df)
    style_s = s.style.applymap(color_obeject)
    return s, style_s


def summary_hist(df, field,label, color='blue', bins=None, dplot_args={}):
    fig, ax = plt.subplots(figsize=(14,5))         # Sample figsize in inches
    if pd.notnull(bins):
        _ = sns.distplot(df[field],bins=bins,color=color,**dplot_args)
    else:
        _ = sns.distplot(df[field],color=color,**dplot_args)

    ax.set_ylabel('Density')

    ## Get some Bounds
    xx = _.patches
    xx  = np.max([z.properties()['bbox'].bounds[-1] for z in xx]) *(1.3)
    adjustment_val = xx*.1
    color_dict = {'mean':'blue','mode':'red','median':'purple'}
    ## Text of summary metrics
    base_val = xx-adjustment_val
    for m in [('mean', np.mean),('median',np.median),('mode',pd.Series.mode)]:
        if m[0] == 'mode':
            text = m[0] +': ' + str(m[1](df[field])[0])
        else:
            text =  m[0] +': ' + str(round(m[1](df[field]),2))

        ax.text(max(df[field])*.75,
               base_val,
                text,
                fontdict={'fontsize' : 15, 'color':color_dict[m[0]]}
               )
        base_val -= adjustment_val
        ax.vlines(m[1](df[field]),0,xx,color_dict[m[0]])
    ax.set_ylim(0,xx)
    ax.set_title(label)