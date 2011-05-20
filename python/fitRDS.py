import ROOT
from ROOT import *

gROOT.SetStyle("Plain")

### GET DATA ###

f_Zbb = TFile("File_rds_zbb_mu.root")
ws_Zbb = f_Zbb.Get("ws")
rds_zbb  = ws_Zbb.data("rds_zbb")
rrv_SV_M  = ws_Zbb.var("rrv_SV_M")
rrv_bb_M  = ws_Zbb.var("rrv_bb_M")
rrv_zeebb_M = ws_Zbb.var("rrv_zeebb_M")
rrv_zmmbb_M = ws_Zbb.var("rrv_zmmbb_M")
rc_cat    = ws_Zbb.var("rc_cat")

rds_4 = rds_zbb.reduce("rc_cat>=4") #Zj
rds_5 = rds_zbb.reduce("rc_cat>=5") #ZbHE
rds_6 = rds_zbb.reduce("rc_cat>=6") #ZbHEMET
rds_7 = rds_zbb.reduce("rc_cat>=7") #ZbHPMET
rds_8 = rds_zbb.reduce("rc_cat>=8") #ZbbHPHE
rds_9 = rds_zbb.reduce("rc_cat>=9") #ZbbHPHP

print "############################"
print "#Events level 4 = ", rds_4.numEntries() 
print "#Events level 5 = ", rds_5.numEntries() 
print "#Events level 6 = ", rds_6.numEntries() 
print "#Events level 7 = ", rds_7.numEntries() 
print "#Events level 8 = ", rds_8.numEntries() 
print "#Events level 9 = ", rds_9.numEntries() 
print "############################"

### GET BACKGROUND MC ###

f_zbb_MC    = TFile("File_rds_zbb_muMC.root")
ws_zbb_MC   = f_zbb_MC.Get("ws")
rds_zbb_MC  = ws_zbb_MC.data("rds_zbb")

rds_zbb_MC_8 = rds_zbb_MC.reduce("rc_cat>=8") #ZbbHPHE
rds_zbb_MC_9 = rds_zbb_MC.reduce("rc_cat>=9") #ZbbHPHP

### MAKE SIGNAL PDF ### (analytic or template)

mean_bb  = RooRealVar("mean_bb", "mean_bb", 300,100,500)
sigma_bb = RooRealVar("sigma_bb","sigma_bb", 50, 10,100)

sig_bb = RooGaussian("sig_bb","sig_bb",rrv_bb_M,mean_bb,sigma_bb)

### MAKE BACKGROUND PDF ### (analytic or template)


# RooKeysPdf* myRHP_b = new RooKeysPdf("myRHP_b","myRHP_b",*SV_m,*RDS_Zbb);
# RooKeysPdf* myRHP_c = new RooKeysPdf("myRHP_c","myRHP_c",*SV_m,*RDS_Zcc);
# RooKeysPdf* myRHP_l = new RooKeysPdf("myRHP_l","myRHP_l",*SV_m,*RDS_Zll);

rdh_zbb_MC_8_SV_M = RooDataHist("rdh_zbb_MC_8_SV_M", "rdh_zbb_MC_8_SV_M", RooArgSet(rrv_SV_M), rds_zbb_MC_8)
rdh_zbb_MC_8_bb_M = RooDataHist("rdh_zbb_MC_8_bb_M", "rdh_zbb_MC_8_bb_M", RooArgSet(rrv_bb_M), rds_zbb_MC_8)
rhp_zbb_MC_8_SV_M = RooHistPdf( "rhp_zbb_MC_8_SV_M", "rhp_zbb_MC_8_SV_M", RooArgSet(rrv_SV_M), rdh_zbb_MC_8_SV_M);
rhp_zbb_MC_8_bb_M = RooHistPdf( "rhp_zbb_MC_8_bb_M", "rhp_zbb_MC_8_bb_M", RooArgSet(rrv_bb_M), rdh_zbb_MC_8_bb_M);

#RooDataHist* myRDH_c = new RooDataHist("myZc", "myRDH_Zc", RooArgSet(*SV_m), *RDS_Zcc);
#RooDataHist* myRDH_l = new RooDataHist("myZl", "myRDH_Zl", RooArgSet(*SV_m), *RDS_Zll);
#RooHistPdf* myRHP_c = new RooHistPdf("myRHP_c","myRHP_c",RooArgSet(*SV_m),*myRDH_c);
#RooHistPdf* myRHP_l = new RooHistPdf("myRHP_l","myRHP_l",RooArgSet(*SV_m),*myRDH_l);

bkg_bb = rhp_zbb_MC_8_bb_M
bkg_bb.SetName("bkg_bb")

S_8=RooRealVar("S_8","S_8",0.8*rds_zbb_MC_8.numEntries(),0,rds_zbb_MC_8.numEntries())
B_8=RooRealVar("B_8","B_8",0.2*rds_zbb_MC_8.numEntries(),0,rds_zbb_MC_8.numEntries())

sum_bb = RooAddPdf("sum_bb","sum_bb",RooArgList(sig_bb,bkg_bb),RooArgList(S_8,B_8))


frame = rrv_bb_M.frame(0,rrv_bb_M.getMax())
rds_8.plotOn(frame)
sum_bb.plotOn(frame,RooFit.LineColor(kBlue))
sum_bb.plotOn(frame,RooFit.Components("sig_bb"),RooFit.LineColor(kGreen),RooFit.LineStyle(kDashed))
sum_bb.plotOn(frame,RooFit.Components("bkg_bb"),RooFit.LineColor(kRed),  RooFit.LineStyle(kDotted))
frame.Draw()

bla

#sum_bb.fitTo(rds_8,RooFit.Extended())

### PLOT ###

C4=TCanvas("C4","C4",900,900)
C4.Divide(2,2)

C4.cd(1)
frame_SV_M_4 = rrv_SV_M.frame(0,rrv_SV_M.getMax())
rds_4.plotOn(frame_SV_M_4)
frame_SV_M_4.Draw()

C4.cd(2)
frame_bb_M_4 = rrv_bb_M.frame(0,rrv_bb_M.getMax())
rds_4.plotOn(frame_bb_M_4)
frame_bb_M_4.Draw()

C4.cd(3)
frame_zeebb_M_4 = rrv_zeebb_M.frame(0,rrv_zeebb_M.getMax())
rds_4.plotOn(frame_zeebb_M_4)
frame_zeebb_M_4.Draw()

C4.cd(4)
frame_zmmbb_M_4 = rrv_zmmbb_M.frame(0,rrv_zmmbb_M.getMax())
rds_4.plotOn(frame_zmmbb_M_4)
frame_zmmbb_M_4.Draw()


C5=TCanvas("C5","C5",900,900)
C5.Divide(2,2)

C5.cd(1)
frame_SV_M_5 = rrv_SV_M.frame(0,rrv_SV_M.getMax())
rds_5.plotOn(frame_SV_M_5)
frame_SV_M_5.Draw()

C5.cd(2)
frame_bb_M_5 = rrv_bb_M.frame(0,rrv_bb_M.getMax())
rds_5.plotOn(frame_bb_M_5)
frame_bb_M_5.Draw()

C4.cd(3)
frame_zeebb_M_5 = rrv_zeebb_M.frame(0,rrv_zeebb_M.getMax())
rds_5.plotOn(frame_zeebb_M_5)
frame_zeebb_M_5.Draw()

C4.cd(4)
frame_zmmbb_M_5 = rrv_zmmbb_M.frame(0,rrv_zmmbb_M.getMax())
rds_5.plotOn(frame_zmmbb_M_5)
frame_zmmbb_M_5.Draw()


C8=TCanvas("C8","C8",900,900)
C8.Divide(2,2)

C8.cd(1)
frame_SV_M_8 = rrv_SV_M.frame(0,rrv_SV_M.getMax())
rds_8.plotOn(frame_SV_M_8)
frame_SV_M_8.Draw()

C8.cd(2)
frame_bb_M_8 = rrv_bb_M.frame(0,rrv_bb_M.getMax())
rds_8.plotOn(frame_bb_M_8)
frame_bb_M_8.Draw()

C8.cd(3)
frame_zeebb_M_8 = rrv_zeebb_M.frame(0,rrv_zeebb_M.getMax())
rds_8.plotOn(frame_zeebb_M_8)
frame_zeebb_M_8.Draw()

C8.cd(4)
frame_zmmbb_M_8 = rrv_zmmbb_M.frame(0,rrv_zmmbb_M.getMax())
rds_8.plotOn(frame_zmmbb_M_8)
frame_zmmbb_M_8.Draw()


C9=TCanvas("C9","C9",900,900)
C9.Divide(3)

C9.cd(1)
frame_SV_M_9 = rrv_SV_M.frame(0,rrv_SV_M.getMax())
rds_9.plotOn(frame_SV_M_9)
frame_SV_M_9.Draw()

C9.cd(2)
frame_bb_M_9 = rrv_bb_M.frame(0,rrv_bb_M.getMax())
rds_9.plotOn(frame_bb_M_9)
frame_bb_M_9.Draw()

C9.cd(3)
frame_zeebb_M_9 = rrv_zeebb_M.frame(0,rrv_zeebb_M.getMax())
rds_9.plotOn(frame_zeebb_M_9)
frame_zeebb_M_9.Draw()

C9.cd(4)
frame_zmmbb_M_9 = rrv_zmmbb_M.frame(0,rrv_zmmbb_M.getMax())
rds_9.plotOn(frame_zmmbb_M_9)
frame_zmmbb_M_9.Draw()

