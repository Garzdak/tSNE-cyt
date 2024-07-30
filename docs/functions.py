import numpy as np
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import flowkit as fk


def cr_df(pop, comp_c,dsp,comp):
    
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

    X = pd.concat(dfs,keys=pop).reset_index()
    nms = X['level_0'].values.tolist()
    X = X.drop('level_1', axis=1)
    X = X.drop('level_0', axis=1)

    sample_from_df = fk.Sample(X, sample_id='my_sample_from_dataframe')
    logicle_xform = fk.transforms.LogicleTransform('logicle', param_t=262144, param_w=0.5, param_m=4.5, param_a=0)
    sample_from_df.apply_transform(logicle_xform)


    Xn = sample_from_df.as_dataframe()
    Xn.columns = Xn.columns.droplevel(1)
    for j in range(0,len(nms)):
        nms[j] = nms[j].rsplit('\\', 1)[-1][:-4]

    Xn['id'] = nms

    return Xn

def tsne(Xn,val,px,it):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(Xn[val])
    n_components = 2
    _tsne = TSNE(n_components, perplexity = px, n_iter=it)
    tsne_result = _tsne.fit_transform(X_scaled)
    Xn['tsne_1'] = tsne_result[:,0]
    Xn['tsne_2'] = tsne_result[:,1]

    return Xn