import csv
import ROOT
import numpy as np
import math

class SingletXSBRs():

    def __init__(self):
        self.xs_csv = 'csv_files/YR4_BSM_13TeV.csv'
        self.widths_csv = 'csv_files/YR4_BSM_Width.csv'

        self.mh = 125.  

        # read in ggH cross sections to TGraph for interpolation
        # ggH cross-section is 9th collumn, mass is first
        with open(self.xs_csv, 'r') as f:
            reader = csv.reader(f)
            xs_ggh = []
            xs_vbf = []
            masses = []
            #skip first 5 rows
            for i, row in enumerate(reader):
                if i < 5: continue
                if row[0] == '': break
                masses.append(float(row[0]))
                xs_ggh.append(float(row[8]))
                xs_vbf.append(float(row[17]))

            self.g_xs_ggh = ROOT.TGraph(len(masses), np.array(masses), np.array(xs_ggh))
            self.g_xs_ggh.SetName('g_xs_ggh')
            self.g_xs_vbf = ROOT.TGraph(len(masses), np.array(masses), np.array(xs_vbf))
            self.g_xs_vbf.SetName('g_xs_vbf')

        with open(self.widths_csv, 'r') as f:
            reader = csv.reader(f)
            masses = []
            widths = {"bb": [], "tautau": [], "mumu": [], "cc": [], "tt": [], "gg": [], "gamgam": [],  "Zgam": [], "WW": [], "ZZ": []}
            for i, row in enumerate(reader):
                if i < 5: continue
                if row[0] == '': break
                masses.append(float(row[0]))
                widths["bb"].append(float(row[1]))
                widths["tautau"].append(float(row[4]))
                widths["mumu"].append(float(row[7]))
                widths["cc"].append(float(row[10]))
                widths["tt"].append(float(row[16]))
                widths["gg"].append(float(row[21]))
                widths["gamgam"].append(float(row[24]))
                widths["Zgam"].append(float(row[27]))
                widths["WW"].append(float(row[30]))
                widths["ZZ"].append(float(row[33]))

        self.d_widths_map = {}
        for key in widths.keys():
            self.d_widths_map[key] = ROOT.TGraph(len(masses), np.array(masses), np.array(widths[key]))
            self.d_widths_map[key].SetName(f'g_width_{key}')

    def kappa_lambda_Hhh(self, sina, tanb, mH):
        """
        Return the coupling modifier for the lambda_{Hhh} trilinear coupling (relative to lambda_SM).
    
        Parameters:
        - sina (float)
        - tanb (float)
        - mH (float): the BSM Higgs mass
        """
        cosa = math.cos(math.asin(sina))
        return (2*self.mh**2 + mH**2)/self.mh**2 * (cosa**2*sina + tanb*sina**2*cosa)

    def kappa_H_t(self, sina):
        """
        Return the Yukawa coupling modifier for the H (BSM scalar).
    
        Parameters:
        - sina (float)
        """
        return sina

    def ComputeHhhWidth(self,mH):
        """
        Compute the width of the heavy Higgs boson decaying to a pair of Higgs bosons for a given mass
         and lambda_hhh set to the SM triple Higgs coupling value
        """      
        v=246.
        lam_SM = self.mh**2/(2*v)
        kap = 1. # i.e take the SM value
        if mH < 2*self.mh: return 0.
        return (kap*lam_SM)**2*(1.-4*(self.mh/mH)**2)**.5/(8*math.pi*mH)

    def ComputeWidth(self, mH, tanb, sina):
        Hhh_width = self.ComputeHhhWidth(mH)*self.kappa_lambda_Hhh(sina, tanb, mH)**2 # H->hh width is computed with the SM value of lambda_hhh then scaled by kappa_lambda_Hhh 
        total_width = 0.

        for key in self.d_widths_map.keys():
            total_width += self.d_widths_map[key].Eval(mH)*sina**2 # all width except H->hh are equal to SM width scaled by sina^2
        total_width += Hhh_width

        return total_width

    def ComputeBR(self, mH, tanb, sina, decay):
        total_width = self.ComputeWidth(mH, tanb, sina)

        if decay == 'hh':
            Hhh_width = self.ComputeHhhWidth(mH)*self.kappa_lambda_Hhh(sina, tanb, mH)**2 # H->hh width is computed with the SM value of lambda_hhh then scaled by kappa_lambda_Hhh 
            return Hhh_width/total_width
        else:
            return self.d_widths_map[decay].Eval(mH)*sina**2/total_width

    def ComputeXS(self, mH, sina, proc):
        if proc == 'gg':
            xs = self.g_xs_ggh.Eval(mH)*sina**2
        elif proc == 'vbf':
            xs = self.g_xs_vbf.Eval(mH)*sina**2
        else:
            xs = (self.g_xs_ggh.Eval(mH) + self.g_xs_vbf.Eval(mH))*sina**2
        return xs

    def ComputeXSBR(self, mH, tanb, sina, proc, decay):
        xs = self.ComputeXS(mH, sina, proc)
        br = self.ComputeBR(mH, tanb, sina, decay)
        print(xs, br)
        return xs*br

if __name__ == "__main__":
    xsbr_tool = SingletXSBRs()

    mH = 400
    tanb = 0
    sina = 0.1
    proc = 'gg'
    decay = 'hh'
    xsbr = xsbr_tool.ComputeXSBR(mH, tanb, sina, proc, decay)

    print(f'xsbr = {xsbr}')
