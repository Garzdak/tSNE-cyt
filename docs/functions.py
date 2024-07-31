"""Module that has necessary function for tSNE and analysis modules"""

import numpy as np
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import flowkit as fk


def cr_df(pop, comp_c,dsp,comp):
    """Function for importing and handling cytometry data that creates scaled dataframe """
    dfs = []
    for i in pop:
        __df = fk.Sample(i)
        if comp_c!=0:
            __df.apply_compensation(comp)
        _df = __df.as_dataframe('raw')
        _df.columns = _df.columns.droplevel(1)
        remove_n = len(_df)-dsp
        drop_indices = np.random.choice(_df.index, remove_n, replace=False)
        df_subset = _df.drop(drop_indices)

        dfs.append(df_subset)

    x = pd.concat(dfs,keys=pop).reset_index()
    nms = x['level_0'].values.tolist()
    x = x.drop('level_1', axis=1)
    x = x.drop('level_0', axis=1)

    sample_from_df = fk.Sample(x, sample_id='my_sample_from_dataframe')
    logicle_xform = fk.transforms.LogicleTransform('logicle', param_t=262144,
                                                   param_w=0.5, param_m=4.5, param_a=0)
    sample_from_df.apply_transform(logicle_xform)


    xn = sample_from_df.as_dataframe()
    xn.columns = xn.columns.droplevel(1)
    nms_n = []
    for j, nms_var in enumerate(nms):
        nms_n.append(nms_var.rsplit('\\', 1)[-1][:-4])

    xn['id'] = nms_n

    return xn

def tsne(xn,val,px,it):
    """Function performing t-SNE"""
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(xn[val])
    n_components = 2
    _tsne = TSNE(n_components, perplexity = px, n_iter=it)
    tsne_result = _tsne.fit_transform(x_scaled)
    xn['tsne_1'] = tsne_result[:,0]
    xn['tsne_2'] = tsne_result[:,1]

    return xn

# End-of-file (EOF)
