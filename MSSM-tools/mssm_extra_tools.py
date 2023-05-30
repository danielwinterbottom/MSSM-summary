"""
Functions to extrapolate cross-section x BR limits into the mA-tanb plane
"""

import numpy as np
import pandas as pd

def scale2mobs(mh, prod, decay, mobs=125.36, xs_path="./csv_files/SM_xs_13TeV.csv", br_path="./csv_files/SM_br_13TeV.csv"):
    """
    Scale xsec*BR prediction for mh to mobs=125.4 GeV
    
    mh      : value of mh as returned from model
    prod    : production mode in LHC HWG naming convention
    decay   : decay channel in LHC HWG naming convention
    xs_path : path to inputs for SM cross section predictions 
    br_path : path to inputs for SM branching fraction predictions
    
    if <decay> is None the branching fraction scale will be ignored and only 
    the cross section scale will be applied.
       
    Following recomendations as given in 
    https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWGMSSMNeutral#Adjusting_BSM_predictions_for_SM 
    """
    scale=1.
    # Linear interpolation of y to the value expected for mh
    linpol=lambda x,y,mh : y[0]+(mh-x[0])/(x[1]-x[0])*(y[1]-y[0])
    # Find values in columns x_name and y_name that embrace m in column x_name
    def brace(path, x_name, y_name, m):
        df = pd.read_csv(path)
        x=df.iloc[(df[x_name]-m).abs().argsort()[0:2]][x_name].tolist()
        y=df.iloc[(df[x_name]-m).abs().argsort()[0:2]][y_name].tolist()
        return x,y
    # Scale factor for cross section (xs)
    x,y = brace(xs_path, x_name="mH", y_name=prod, m=mh)
    scale*=linpol(x,y,mh)/linpol(x,y,mobs)
    if not decay.lower()=="none":
        # Scale factor for branching fraction (br)
        x,y = brace(br_path, x_name="mH", y_name=decay, m=mh)
        scale*=linpol(x,y,mh)/linpol(x,y,mobs)
    return scale

def mA_tanb_scan(obs, mX, mX2mA, model, start=0.5, stop=60., step_size=0.5, lockmX=False, verbose=False):
    """
    Scan tanb and find intercept of the prediction with the observed limit.

    The function uses the idea that at the point of the intercept the 
    difference "pred-obs" changes sign. When this happens the given tanb value 
    is estimated from the tanb points above and below through linear 
    interpolation.
    
    The scan can be run for fixed values of mX, in the direction from small to 
    large values for tanb, or in the direction from large to small values of 
    tanb. In the latter case note that step_size has to have a negative value.
    
    Currently the scan stops at the first crossing point. Identifying islands 
    in the mA-tanb plane, where the scan would cross at least twice is not 
    supported.

    Arguments are:
              
    obs        : observed limit
    mX         : mass value for which the obs is provided 
    mX2mA      : mapping from mX to mA
    model      : model to obtain the prediction from as function of mA and tanb
    start      : tanb value to start the scan
    stop       : tanb value to stop the scan
    step_size  : step size in tanb 
    lockmX     : lock the mX value and do not evaluate the model at mA (used 
                 for limits on charged Higgs as a function of mHp)
    verbose    : add print statements, e.g. for debugging
    
    The return value is a tuple of (mA, tanb). If no intercept is found (mA, 
    stop) is returned. 
    """
    __last_tanb__=-1
    __last_diff__= 0
    for tb in np.arange(start, stop, step_size):
        mA = mX
        if not lockmX:
            mA   = mX2mA(mX, tb)
        pred = model(mA, tb)
        if not __last_diff__==0:
            if (pred-obs)*__last_diff__<0: 
                tanb=__last_tanb__+(__last_diff__)/(__last_diff__+obs-pred)*(tb-__last_tanb__)
                if verbose:
                    print(mA, tb, pred, mX, obs)
                return (mX2mA(mX, tanb), tanb)
        if pred>0:
            __last_diff__= pred-obs
            __last_tanb__= tb
    return (mX2mA(mX, stop), stop)

if __name__=="__main__":
    # Call mA_tanb_scan with some reasonable values; example taken from 
    # HIG-21-011
    import mssm_xs_tools 
    mssm = mssm_xs_tools.mssm_xs_tools(b"root_files/hMSSM_13.root", True, 0)
    def ggHhh(mA, tb): 
        return mssm.xsec(b"gg->H", mA, tb)*mssm.br(b"H->hh", mA, tb)
    def mH2mA(mX, tb):
        return mssm.mass2mA(b"H", mX, tb)
    print(mA_tanb_scan(0.63, 260, mH2mA, ggHhh))

__version__=1.1
