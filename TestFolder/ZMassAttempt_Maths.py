#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)
import ROOT

ch = ROOT.TChain('Z/DecayTree')
ch.Add('/storage/epp2/phshgg/DVTuples__v23/5TeV_2017_32_Down_EW.root')

import math

def energy(mass, PT, ETA):
    temp = PT**2 * (math.cosh(ETA))**2
    return math.sqrt(mass**2+temp)

def calculation(mass, mup_PT, mup_ETA, mup_PHI, mum_PT, mum_ETA, mum_PHI, mup_energy, mum_energy):
    angles = math.cos(mup_PHI - mum_PHI) + math.sinh(mup_ETA)*math.sinh(mum_ETA)
    IMassSq = 2*(mass + mup_energy*mum_energy - mup_PT*mum_PT*angles)
    IMass = math.sqrt(IMassSq)
    return IMass
   
mass = 0.105 #GeV

nbins = 100
xmin = 40.
xmax = 120.

hist = ROOT.TH1F('hist_name','title',nbins,xmin,xmax)

for entry in ch:
    mum_PT = entry.mum_PT * 10**(-3) #MeV -> GeV
    mum_ETA = entry.mum_ETA
    mum_PHI = entry.mum_PHI

    mup_PT = entry.mup_PT * 10**(-3)
    mup_ETA = entry.mup_ETA
    mup_PHI = entry.mup_PHI
    
    mup_energy = energy(mass, mup_PT, mup_ETA)
    mum_energy = energy(mass, mum_PT, mum_ETA)

    IMass = calculation(mass, mup_PT, mup_ETA, mup_PHI, mum_PT, mum_ETA, mum_PHI, mup_energy, mum_energy)
    hist.Fill(IMass)

canv = ROOT.TCanvas()
hist.Draw()
canv.SaveAs('ZMassPlot_Maths.pdf')