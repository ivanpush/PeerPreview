## **Elastomeric sensor surfaces for high-throughput** **single-cell force cytometry**

**Ivan Pushkarsky** **[1,9]** **, Peter Tseng** **[1,2,9]** **, Dylan Black** **[1]** **, Bryan France** **[3]** **, Lyndon Warfe** **[1]** **, Cynthia J. Koziol-White** **[4]** **,**
**William F. Jester Jr** **[4]** **, Ryan K. Trinh** **[5]** **, Jonathan Lin** **[1]** **, Philip O. Scumpia** **[6]** **, Sherie L. Morrison** **[5]** **,**
**Reynold A. Panettieri Jr** **[4]** **, Robert Damoiseaux** **[3,7]** **and Dino Di Carlo** **[1,3,8]** *****


**As cells with aberrant force-generating phenotypes can directly lead to disease, cellular force-generation mechanisms are high-**
**value targets for new therapies. Here, we show that single-cell force sensors embedded in elastomers enable single-cell force**
**measurements with ~100-fold improvement in throughput than was previously possible. The microtechnology is scalable and**
**seamlessly integrates with the multi-well plate format, enabling highly parallelized time-course studies. In this regard, we show**
**that airway smooth muscle cells isolated from fatally asthmatic patients have innately greater and faster force-generation**
**capacity in response to stimulation than healthy control cells. By simultaneously tracing agonist-induced calcium flux and con-**
**tractility in the same cell, we show that the calcium level is ultimately a poor quantitative predictor of cellular force generation.**
**Finally, by quantifying phagocytic forces in thousands of individual human macrophages, we show that force initiation is a digi-**
**tal response (rather than a proportional one) to the proper immunogen. By combining mechanobiology at the single-cell level**
**with high-throughput capabilities, this microtechnology can support drug-discovery efforts for clinical conditions associated**
**with aberrant cellular force generation.**



ell-generated mechanical forces, which normally fulfil
essential biological roles at both the cellular level (such as
# Cmechanotransduction [1], migration [2], cytokinesis [3], immune

processes [4] and vasoregulation [5] ) and the tissue level (such as tone
maintenance and concerted contractions) can at times become
dysregulated, leading to diseased anatomical states or loss of function. Abnormally high force generation underlies bronchoconstriction [6] in asthma, hypertensive vasoconstriction and stroke [7],
and muscle spasms, and is also involved in fibrotic tissue stiffening [8] and in the pathogenesis of cancer [9] . Conversely, the inability of
cells to generate force describes the phenotypic basis for cardiac
insufficiency and congenital defects such as X-linked neutropenia and muscular dystrophy. Furthermore, undesired vasodilation
in the brain has been identified as the physiological trigger for
migraine pain [10] . Therefore, cellular force generation can serve as a
useful measure for evaluating disease state and provides a valuable
therapeutic target.
For several therapeutic indications, existing treatments promote
the relaxation of cell shortening through established molecular
pathways. However, the coupling of the molecular pathways to the
contractile force remains poorly understood. Because conventional
therapies induce severe side effects and tolerance development or
are simply ineffective, new approaches are needed that act specifically and effectively on mechanical force transduction. A scalable
cellular force cytometer of general use that could rapidly evaluate
large screening libraries would accelerate drug-development efforts
and anchor research in force biology.



Existing techniques for performing these measurements suffer
from strict trade-offs between the quality of the data on the one
hand and throughput and ease of use on the other. Traction force
microscopy (TFM) [11][,][12] and elastomeric micropost array [13] assays
can resolve sub-cellular forces, but require laborious manual steps
that have limited throughput to only a few dozen cells in a typical
experiment [14][–][17] . TFM serially implemented in a microtiter plate format increased throughput but lost its single-cell resolution, instead
reporting a noise-prone, bulk 'response-ratio' measurement [11] that
overlooked clinically important sub-populations, such as the highly
contractile platelets present in patients with normal clotting function [18] . A concept combining TFM and fluorescent micropatterns
was also proposed, but was ultimately limited to proof-of-principle
due to practical fabrication challenges [19] . To address the need to
scale up data acquisition, both in terms of cell numbers and temporal resolution, we introduce an integrated biosensor material
comprising fluorescently labelled elastomeric contractible surfaces
(FLECS) for making single-cell force measurements at throughputs
~100-fold higher than was previously possible.
In the FLECS system, each cell adhering to one of thousands of uniform adhesive and fluorescent micropatterns generates comparable
mechanical forces onto the underlying elastomeric film and produces
unique, well-calibrated displacements at their respective micropatterns’ peripheries (Fig. 1a and Supplementary Videos 1 and 2),
which can easily be quantified using image analysis algorithms
(Fig. 1c). By combining micro-contact printing of proteins with sacrificial layers, we can stably encode micropatterns consisting of any



1Department of Bioengineering, University of California, Los Angeles, Los Angeles, CA, USA. 2Department of Electrical Engineering and Computer
Science, University of California, Los Angeles, Irvine, CA, USA. [3] California NanoSystems Institute, University of California, Los Angeles, Los Angeles,
CA, USA. [4] Rutgers Institute for Translational Medicine and Science, Child Health Institute, Rutgers University, New Brunswick, NJ, USA. [5] Department of
Microbiology, Immunology and Molecular Genetics and The Molecular Biology Institute, University of California, Los Angeles, Los Angeles, CA, USA.

6Division of Dermatology, David Geffen School of Medicine, University of California, Los Angeles, Los Angeles, CA, USA. 7Department of Molecular and
Medicinal Pharmacology, University of California, Los Angeles, Los Angeles, CA, USA. [8] Department of Mechanical Engineering, University of California,
Los Angeles, Los Angeles, CA, USA. [9] [These authors contributed equally: Ivan Pushkarsky and Peter Tseng. *e-mail: dicarlo@seas.ucla.edu](mailto:dicarlo@seas.ucla.edu)


**124** **Nature Biomedical Engineering** [| VOL 2 | FEBRUARY 2018 | 124–137 | www.nature.com/natbiomedeng](http://www.nature.com/natbiomedeng)


© 2018 Macmillan Publishers Limited, part of Springer Nature. All rights reserved.


#### NATure BIomedIcAl EngIneerIng Articles



















**Fig. 1 |** **Operational principles of the general-use FLECS force cytometer.** **a**, Top: technology schematic showing cells adhered to functionalized adhesive
micropatterns embedded into a thin glass-supported elastomeric film. Left: top view showing multiple pattern shapes and a blow-up of a cell contracting
an 'X' pattern and inwardly displacing its terminals. Middle: overlay of fluorescent patterns and phase contrast images of adhered contracting cells. Right:
time-lapsed images of a contracting cell and the underlying micropattern. Scale bars, 25 μ​m. **b**, Well-plate implementation. **c**, Image analysis workflow.
Input: image sets of the micropatterns (set 1) and stained cell nuclei (set 2). Processing: the algorithm (1) identifies and measures all micropatterns
in image set 1, (2) cross-references the positions of each micropattern in image set 2, and (3) determines whether 0, 1 or >​2 nuclei (that is, cells) are
present (see Supplementary Fig. 2). Output: mean centre-to-terminal displacements of the micropatterns containing a single nucleus (that is, one cell) are
compared with the median of the corresponding measurement of all undisplaced patterns containing zero nuclei (that is, unoccupied patterns) and the
differences are plotted as a horizontal histogram.



biomolecule bearing free amine or thiol groups into a silicone elastomer without using costly linkers, resulting in uniform micropatterns that are unaffected by material stiffness (Supplementary Fig. 1).
This allows us to simulate diverse tissue environments, which, in
turn, can elicit a wide range of measurable force-generating behaviours, from basal smooth muscle tone to phagocytosis. Importantly,
in a multi-well plate format, FLECS achieves a substantial degree
of parallelization without linear increases in fabrication labour. The
96-well plate embodiment (containing >​6,000 70 µ​m 'X' patterns per
well) is natively compatible with existing automation and screening
infrastructures (that is, liquid-handling robotics, plate-handling
robotics and high-content imaging systems) and offers a practical
solution to performing highly parallelized assays and other general
experiments that were previously too costly or cumbersome.


**Results**
**Whole-cell contractility measurements resolve population-wide**
**contractile differences.** FLECS provides whole-cell contractility
measurements. To show that this level of resolution is sufficient for
detecting population-wide contractile differences, we assayed multipotent human mesenchymal stem cells (hMSCs), which are known
to exert large contractile forces and to interrogate mechanical cues
in their environment [20][,][21] and differentiated progeny. hMSCs spread
uniformly to occupy 70 μ​m fibronectin 'X' patterns, forming dense
actin stress fibres (Fig. 2b and Supplementary Fig. 3). Regardless of
the tissue of origin, hMSCs in a multi-potent state produced significantly higher steady-state micropattern displacements than either
set of differentiated hMSCs, suggesting greater force generation
(Fig. 2a). A previous study reported high forces in differentiating
hMSCs that peaked in the first day of culture but declined over the
following seven days [22] . Our results support this earlier conclusion
as they reveal significantly lower forces in MSCs following longer
differentiation times (that is, at 14 days, as in our experiment) and
indicate that sub-cellular resolution is not necessary for populationwide cellular force cytometry. Furthermore, because FLECS assays
all cells present in a sample without pre-selection in one automated



procedure, we obtained data for 180 to >​1,500 cells per condition
(rather than 13–62 cells, as was presented in the previous study)
and identified a smaller sub-population of weakly contractile cells
in each multi-potent stem cell sample.
Additional experiments using FLECS were performed to characterize and compare whole-cell contractility for three types of primary human smooth muscle cells (SMCs)—bronchial SMCs, aortic
SMCs and uterine SMCs. These cells were observed to uniformly
spread over and contract thousands of 70 µ​m 'X' patterns, producing measurable displacements that were on average greater for
aortic SMCs and uterine SMCs than for bronchial SMCs, suggesting higher native force generation by those cells in the absence of
stimuli (Supplementary Fig. 4). A larger sub-population of weakly
contracting cells was also identified in the uterine SMC distribution,
perhaps due to the relative difficulty of isolating pure populations
from this complex tissue. These experiments further support the
suitability of FLECS for studying the force biology of a variety of
adherent tissue cells.
Considering the multitude of disorders arising from abnormal
SMC contractility, including asthma, hypertension and bowel disease [23], technology for rapid force-phenotyping of large SMC populations would be invaluable for research and drug-development
purposes. In support of this idea, we tested whether whole-cell
contractility measurements obtained with FLECS provide sufficient resolution for performing functional phenotypic screens
of modulators of cellular force, and whether accurate quantitative
characterization of drug compounds can be achieved. To do so,
we titrated the myosin II inhibitor blebbistatin using contracting
primary human airway smooth muscle (HASM) cells following a
10-step, twofold dilution scheme and vehicle controls with 4 technical replicates for each (equating to 44 independent measurements)
on a single functionalized 96-well plate (Fig. 2c). As expected, the
addition of this tool compound produced a restorative effect on the
cell-contracted micropatterns (Supplementary Video 3), which was
dose dependent. We observed low variability across replicates and
calculated an IC50 of 2.61 µ​M, which matches previously reported



**Nature Biomedical Engineering** [| VOL 2 | FEBRUARY 2018 | 124–137 | www.nature.com/natbiomedeng](http://www.nature.com/natbiomedeng) **125**


© 2018 Macmillan Publishers Limited, part of Springer Nature. All rights reserved.


#### Articles NATure BIomedIcAl EngIneerIng



**a**


**c**





**b**



12


8


4


0





|n > 25,000 No cells|Adipo Multipotent n = 851|ose-derived hM Adipogenic n = 849|MSCs Osteogenic 16 n = 1,899|Bone mar Multipotent n = 188|rrow-derived h Adipogenic n = 653|hMSCs Osteogenic n = 345|
|---|---|---|---|---|---|---|
|_n_ > 25,000|_n_ = 851|_n_ = 849|0<br>4<br>8<br>12<br>16<br>_n_ = 1,899|_n_ = 188|_n_ = 653|_n_ = 345|
|_n_ > 25,000|||||||
|_n_ > 25,000|||||||
|_n_ > 25,000|||||||
||||||||


Relative frequency

      -      
         -         

**d**


|n = 1,108|n = 1,144|n = 1,243|n = 1,101|n = 1,063|
|---|---|---|---|---|
||||||
||||||
||||||
|<br>977× 10–8 M|<br>91× 10–7 M|156× 10–6 M|625× 10–6 M|250× 10–5 M|


|Half-maximal<br>inhibitory|Col2|
|---|---|
|IC50 = 2.61μM<br>~~concentration~~||



–8 –7 –6 –5 –4

log(blebbistatin concentration, M)



12


8


4


0



Relative frequency


Increasing dose



100


75


50


25


0





**Fig. 2 |** **Whole-cell contractility resolves contractile changes with differentiation and drug treatment.** **a**, Primary human adipose- or bone-marrowderived MSCs exhibited much higher contractile responses than either committed lineage 8 h post-seeding. Non-contractile sub-populations were seen
among the MSCs, indicating heterogeneity and potentially low purity that resulted from standard separation methods. _n_ represents the number of cells.
A typical contracted pattern approximately representing the median case from each distribution is shown below. Scale bars, 35 µ​m. **b**, Overlays of
fluorescent images of contracted patterns (green), phalloidin-stained actin (red) and nuclei (blue) of adipose-derived multi-potent MSCs showing three
instances of cells fully spread over the patterns and actin stress fibres that route stresses to the vertices of the 'X' patterns. Scale bars, 25 μ​m.
**c**, Representative distributions of single-cell responses to increasing doses of blebbistatin. Plots comprise pooled data from four technical replicates
of each condition. **d**, Dose-response curve over 3 decades in which we identify an IC50 of 2.61 µ​M. Error bars represent s.e.m. _n_ represents number of
cells in each distribution. The Kruskal–Wallis test for non-parametric data was used to perform statistical analyses on the contractile distributions with
significance defined as _P_ <​ 0.05.



values [24][,][25] (Fig. 2d). These results show that automating (and scaling)
the FLECS assay is feasible and yields robust readouts. As such, we
expect the FLECS well-plate to facilitate automated screens of large
drug libraries to help identify new candidates for correcting malfunctioning cellular contractility. The single-cell resolution should
also help reveal any non-Gaussian responses to modulators at the
population level.


**Airway SMCs isolated from donors with asthma inherently**
**generate higher forces.** Used together with laboratory automation equipment, the well-plate implementation of FLECS provides
new opportunities to perform highly parallelized and multi-faceted
studies of force generation with high precision and fine temporal
resolution. Here, we harnessed these capabilities to thoroughly
evaluate the functional contractile profiles of primary HASM cells
isolated from patients with fatal asthma and compared them with
cells from patients who were age-, race- and gender-matched without asthma. Researchers in the field have supposed that innate differences in force generation should exist between the two sets, yet
the various aspects of this phenotype have never been compared
directly using a single method or with large quantities of cells.
Although a previous study compared this mechanophenotype
between patient cells using TFM for a number of cells at baseline,
the traction moments were not normalized to the cell-spread area,
which is known to dictate traction forces, and contractility could
not be assessed following dosing with agonists [26] . Moreover, the
comparative responsiveness to asthma treatments has not previously been compared between normal and diseased HASM cells.
Here, we aimed to provide a definitive report on whether force
generation was indeed inherently greater in asthma HASM cells



using a single measurement methodology, evaluating both tone and
responsiveness in thousands of the same cells. For this study, we
evaluated (1) the basal cell tone, (2) contractile responsiveness to
treatment with a bronchoconstrictor and (3) the responsiveness to
attempted rescue from bronchoconstriction using the asthma standard-of-care β​2-adrenoceptor agonist formoterol in the same cells.
These evaluations were performed on 12 total patient-derived cell
lines of which 6 were isolated from asthmatic patients and 6 from
(age-, gender- and race-matched) non-asthmatic patients (Fig. 3).
HASM cells from asthmatic patients contracted patterns with a
higher baseline tone than cells from healthy patients. To first evaluate tone, the 12 HASM cell lines were seeded into 8 wells, each
within 3 FLECS multi-well plates. Each of these was assembled
with independently mixed batches of silicone elastomer. Following
adhesion and serum starvation, all wells were imaged to obtain
basal (tonic) contraction levels for the 12 cells lines. The trends in
tonic contraction between the 12 cell populations were conserved
across the three samples, and the minor inter-well-plate variability
was significantly less than the inter-donor variability we observed,
indicating that the method reliably discerns biological differences
(Supplementary Fig. 5). Here, we observed that the asthma HASM
cells exhibited, on average, higher tone than the non-asthma HASM
cells. When compared as two pooled groups, the median basal tone
of all asthma HASM cells was statistically greater than the median
basal tone of non-asthma HASM cells (Fig. 4a).
Immediately after imaging cells in their tonic contracted state,
we treated them all with the contractile agonist bradykinin at a final
concentration of 10 µ​M. We had previously observed bradykinin
as well as endothelin-1—both of which are molecules that have
been impugned in asthma—to promote significant contraction in



**126** **Nature Biomedical Engineering** [| VOL 2 | FEBRUARY 2018 | 124–137 | www.nature.com/natbiomedeng](http://www.nature.com/natbiomedeng)


© 2018 Macmillan Publishers Limited, part of Springer Nature. All rights reserved.


#### NATure BIomedIcAl EngIneerIng Articles



**a**



Image every Image every Final

10 µM BK 4 min Vehicle control 4 min image









Baseline
image































































Timepoints


**Fig. 3 |** **Parallel study of fatal asthma and non-asthma patient-derived airway SMCs.** **a**, Experimental workflow. Patient-derived HASM cell lines ( _n_ =​ 12)
were seeded into 8 wells each in a FLECS well-plate and a baseline image was taken. All cells were then treated with the contractile agonist bradykinin
(BK; 10 µ​M final concentration) and imaged for 16 min at 4-min intervals. Half of all cells were treated with 50 µ​M formoterol and the other half were
treated with DMSO vehicle. Cells were imaged for an additional 20 min at 4-min intervals and finally 10 min later. **b**, Distributions of responsive cells from
a representative patient. The distribution shifts upwards following BK treatment and is halted by formoterol. **c**, Median values of the evolving contractile
distributions for each of 12 patient cell lines with or without formoterol treatment. Each data point in each trace comprises an average of four separate
well measurements on the well-plate. **d**, Pair-wise comparison of age-, race- and gender-matched patients with and without asthma. The first age listed
is for the normal patient, while the second is for the asthmatic patient. The letters denote race and gender. The full characteristics for all patient donors
are listed in Supplementary Table 1. In general, HASM cells from asthma patients exhibited greater tone and/or contraction following stimulation.
A one-tailed Student’s _t_ -test was performed on the patient pairs in **d** . * _P_ <​ 0.05; ** _P_ <​ 0.01; *** _P_ <​ 0.001. Error bars represent s.e.m. AA, African American;
C, Caucasian; F, female; M, male.



primary HASM (Supplementary Videos 4 and 5). Following treatment, all 96 sites were re-imaged once every 4 min for 16 min, at
which point the plate was removed from the imager and half the
wells received 50 µ​M formoterol, while the other half received vehicle (1% dimethyl sulfoxide (DMSO)). The plate was replaced and
all sites were imaged for another 20 min at 4-min intervals before
a final time point was recorded 10 min later. Contractility for each
of the ~31,000 cells was tracked over time and cells exhibiting
increased contraction at 16 min relative to baseline were selected for
further analysis (~72% of cells on average).
We tracked the evolving contractile distributions for all selected
cells (Fig. 3b) and found that the distributions showed robust



upwards shifts following treatment with bradykinin that were unattenuated following the addition of vehicle, but were halted or
reversed following treatment with formoterol. The median contractility value of each cell population was tracked over the course of
pharmacological treatment (Fig. 3c) and it was observed that for
five of six pairs of age-, race- and gender-matched patients with or
without fatal asthma, the asthmatic patients’ cells exhibited either
greater tone, greater bradykinin-induced contraction or both
(Fig. 3d). In four of these cases, the differences were statistically
significant. One asthma line (asthma patient 6) displayed lower
contraction in all respects than its healthy patient counterpart. We
conclude that, in general, HASM cells isolated from fatal-asthmatic



**Nature Biomedical Engineering** [| VOL 2 | FEBRUARY 2018 | 124–137 | www.nature.com/natbiomedeng](http://www.nature.com/natbiomedeng) **127**


© 2018 Macmillan Publishers Limited, part of Springer Nature. All rights reserved.


#### Articles NATure BIomedIcAl EngIneerIng



**a**



Basal tone **b**



Initial increase after BK



8


6


4





2


0

Normal Asthma


**c** Increase over 40 min **d**


2


1



1.0


0.8


0.6


0.4


0.2


0



1


0


–1





Normal Asthma


Reversal after formoterol







0



Normal Asthma



Normal Asthma



**Fig. 4 |** **Collective comparisons of all asthma versus non-asthma HASM**
**cells.** **a** – **d**, Each data point represents the median value of an individual
well measurement. All wells ( _n_ =​ 96) were compared in **a**, only wells that
received the vehicle ( _n_ =​ 48) were compared in **b** and **c**, and only wells that
received formoterol ( _n_ =​ 48) were compared in **d** . The tone was statistically
greater for asthmatic HASM cells. The initial rate of response to bradykinin
(BK) was also greater for asthmatic cells. However, the long-term time
response over the course of the experiment and rescue via formoterol were
similar for the two groups. A one-tailed Student’s _t_ -test was performed on
pooled groups. NS, not significant.


patients innately generate greater force than cells isolated from their
healthy counterparts.
The acute contractile response to the agonist also appeared significantly accelerated in fatal-asthmatic patient-derived cell lines.
Specifically, the initial rates of contractile response, defined as the
change between the initial tonic reading and first measurement following bradykinin stimulation, were greater in asthmatic lines than
normal ones, and this difference in rate was statistically significant
(Fig. 4b). Interestingly, despite this initial differential response,
which was observed until the third imaging time point, or roughly
12 min (not shown), the total increase over the full course of the
experiment was similar between the groups (Fig. 4c). This indicates
that while there were clearly differences in the absolute force generation between asthma and normal lines, the differences in their relative responsiveness to agonists may have be dominated by kinetics.
Finally, we assessed whether rescue by formoterol was differentially
effective among the two groups. Traces of the population medians
(Fig. 3c) indicated that a number of cell lines from both groups
showed substantial reversal following treatment with formoterol,
but both groups also had cells that responded more asymptotically.
Accordingly, when compared collectively, the asthma and normal
HASM cell lines manifested similar responsiveness to formoterol.
However, a subset of normal-derived cell lines showed substantially
greater reversal than any asthma-derived lines (Fig. 4d).


**Conventional calcium release assays poorly predict functional**
**contractility in HASM.** Using the FLECS workflow, cells may be
imaged live or fixed in their contracted state and subsequently phenotypically profiled. Since the cells were confined to micropatterns
with known positions and boundaries, a simple algorithm could be
used to quantify molecular biomarkers associated with a functional
output (for example, contraction) at the single-cell level over a population of cells. We applied this analysis to address the correlation
in agonist-induced increases in cytosolic calcium with contraction
responses in HASM in a cell-by-cell manner.



Excitation–contraction coupling of HASM requires the highly
coordinated activation of calcium mobilization pathways with
released calcium from intracellular calcium stores and with calcium
influx from the extracellular space. Calcium sensitization activates
rho kinase to inhibit myosin light chain phosphatase activity and
activate actin polymerization and reorganization pathways, as well
as enabling myosin–actin interaction. Some—but not all—of these
pathways are calcium dependent and no techniques have previously been demonstrated to distinguish the relative contribution
of calcium mobilization with simultaneous measurements of force
generation in single cells. Here, by first recording changes in calcium-sensitive dye intensities within HASM arrayed on a FLECS
well-plate (Supplementary Video 6) and then monitoring the
changes in their respective micropatterns (Fig. 5a–b), we show that
the magnitudes of agonist-induced peak calcium and HASM cell
contraction responses are differentially modulated by agonists.
Comparing agonist-induced peak calcium and contraction
responses in hundreds of HASM single cells, on average, bradykinin
and histamine manifested the greatest calcium responses, whereas
the greatest contraction responses were observed with serum and
endothelin-1 stimulation (Fig. 5c). Interestingly, at the single-cell
level, there were no correlations among peak calcium and maximal contraction for any tested agonist, even when the populations
were gated to only include responders (for example, cells exhibiting
either >​1 µ​m contraction increases or a >​1.1-fold change in calcium dye intensity; Fig. 5d and Supplementary Fig. 6). In fact, some
high calcium responders manifested no contraction, while some
very weak calcium responders produced substantial contractile
responses. Some of these effects may be explained by the activation
of receptors differentially coupled to G proteins. For example, histamine activates the histamine 1 receptors coupled to the Gq subunit,
which increases phospholipase β​, which then activates the canonical
inositol 1,4,5-triphosphate pathway. However, it also activates the
histamine 2 receptors coupled to the Gs subunit, which increases
cyclic adenosine monophosphate and activates protein kinase A,
which then antagonizes force generation. The net effect on histamine-induced force generation probably relates to the stoichiometry of the differential receptor activation. Similarly, serum that
contains a variety of agonists likely activates a multitude of HASM
receptors that have differential effects on calcium mobilization and
force generation.
Collectively, our data support the hypothesis that agonistinduced peak calcium responses may not correlate with force generation, and that while calcium release assays may generally indicate
that contractile pathways have been activated, they have limited
usefulness as a quantitative predictor of cellular contractility. These
findings suggest that high-throughput screens of force modulators using calcium-sensitive dyes, such as those proposed in recent
works [27], may have significant limitations in terms of specificity and
predictivity. Overall, we demonstrate that FLECS allows unique
multi-modal studies involving contractility to be performed on single cells in situ, including transient biological events occurring on
sub-minute timescales. As with all previous experiments, we analysed relatively large populations of single cells, and all present cells
were evaluated automatically by the algorithm. By simultaneously
addressing functional and molecular phenotypes in large numbers
of cells using automation, FLECS presents new opportunities for
discriminating between the modes of actions of biological agonists
associated with abnormal contractility diseases.


**Force generation in phagocytosis acts in a digital manner.** In innate
immunity, mechanical forces direct phagocytosis—the process by
which phagocytes internalize and destroy foreign pathogens and
clear cellular debris. Operating at the single-cell level, our microtechnology is uniquely suited to evaluate phagocytic forces in individual
primary human macrophages—a measurement that has not been



**128** **Nature Biomedical Engineering** [| VOL 2 | FEBRUARY 2018 | 124–137 | www.nature.com/natbiomedeng](http://www.nature.com/natbiomedeng)


© 2018 Macmillan Publishers Limited, part of Springer Nature. All rights reserved.


#### NATure BIomedIcAl EngIneerIng Articles



**a**


**b**


**c**



1.2


1.1


1


1.8


1.6


1.4


1.2


1


1.20


1.15


1.10


1.05


1.00



**d**
1. Initial 2. Continuous 3. Continuous µ pattern
μ pattern Ca [2+] -sensitive dye imaging contractility imaging



Frames (10 fps) Time (min)


Population-averaged Ca [2+] release Population-averaged contractility



3. Continuous µ pattern

contractility imaging
(25 min, 1-min intervals)



image



2. Continuous
Ca [2+] -sensitive dye imaging
(30 s, 10 fps)



Histamine
6 _n_ = 324 cells

_R_ = –0.097

_P_ = 0.081


4


2


0

1× 1.2× 1.4×



6


4



Ca [2+] release trace contractility trace



0 50 100 150 200



max _F_ / _F_ 0 3 max Δdisp


2


1



0 100 200 300



0 5 10 15 20 25



Frames (10 fps) Time (min)



Serum


_n_ = 305 cells


_R_ = 0.161


_P_ < 0.01



Pooled Ca [2+] release traces
following treatment with BK


0 100 200 300



0 5 10 15 20 25



Pooled contractility traces
following treatment with BK



Bradykinin

_n_ = 503 cells
_R_ = 0.044

_P_ = 0.321


1× 1.2× 1.4×



5

4

3

2

1

0

–1



0 5 10 15 20 25



2


1


0







2


0


6
Serum-free

medium
(control)

4


_n_ = 322 cells


2


0

1× 1.2× 1.4×


Single-cell Ca [2+] release

(max _F_ / _F_ 0)



Frames (10 fps) Time (min)



**Fig. 5 |** **Simultaneous measurements of calcium release and contractility in patient-derived HASM single cells.** **a**, Experimental workflow. Adhered cells
labelled with Fluo-8 were imaged in their tonic state. Agonists were then added and the calcium-sensitive dye intensity was recorded for 30 s at 100-ms
intervals. The same set of micropatterns was then imaged for 25 min at 1-min intervals. Calcium release and contractility traces were extracted from these
image series. The black triangle on the individual calcium trace denotes the addition of the agonist. _F_ / _F_ 0 is the ratio of the fluorescent intensity ( _F_ ) to the
initial intensity recorded at the first time point ( _F_ 0). fps, frames per second. **b**, All traces obtained from cells treated with bradykinin (BK) ( _n_ =​ 503 cells).
**c**, Population-averaged traces for each agonist. Peak values from the two traces do not correlate, indicating that a high-intensity calcium signal does not
necessarily translate to robust contraction. Error bars represent s.e.m. **d**, Correlations between peak calcium release and peak contraction for the same
single cells. Histograms displayed horizontally and longitudinally correspond to the isolated contractility and calcium measurements, respectively, and
the coloured bar in each distribution identifies the bin containing the median value. While each agonist induced calcium release and contraction to some
extent, there were no strong correlations between these measurements.



previously demonstrated. We achieved this by embedding dansylated bovine serum albumin (BSA) micropatterns into the elastomeric
surface and incubating them with anti-dansyl chimeric immunoglobulin G (hIgG). The resultant micropatterned immune complexes
reliably promoted a phagocytic response: human monocytederived macrophages (hMDMs) rapidly adhered, spread over and
contracted the opsonized patterns and maintained the contraction
for up to 16 h (Fig. 6a–b and Supplementary Video 7).
We first investigated the open question of whether the quantity
of presented stimulus modulates total phagocytic force. This was
done by patterning hIgG into three equi-diametric circular shapes
(to control the cell-spread area), but with different interior geometries to vary the quantities of presented antibody. The MDMs spread
uniformly over micropatterns of each shape and, surprisingly, produced statistically similar micropattern displacements (Fig. 6c).
This result suggests that, as for the triggering of cytokine secretion



in T cells [28], the phagocytic pathway leading to force generation acts
in a digital manner, turning 'on' completely at a certain threshold,
but not scaling with opsonin quantity.
We expected that forces involved in Fc receptor (FcR)-mediated
phagocytosis would exceed less biologically urgent forces initiated by other adhesive opsonins. To evaluate this, we also examined MDM responses to non-opsonized dansylated BSA, as well as
fibrinogen or vitronectin—molecules that support long-term macrophage adhesion but have less understood immunological roles [29][,][30] .
Micropatterns with hIgG presented with the largest displacements,
while micropatterns with fibrinogen, vitronectin and dansylated
BSA generally presented with very minute displacements, supporting our hypothesis. However, for each of these three other conditions, there was a small sub-population of MDMs that applied
substantial contractile forces comparable to hIgG (Fig. 6d). We
suppose this is because a subset of the MDMs, which were initially



**Nature Biomedical Engineering** [| VOL 2 | FEBRUARY 2018 | 124–137 | www.nature.com/natbiomedeng](http://www.nature.com/natbiomedeng) **129**


© 2018 Macmillan Publishers Limited, part of Springer Nature. All rights reserved.


#### Articles NATure BIomedIcAl EngIneerIng



**a**


**b**


**c**



**d**


**e**



16


12


8


4


0


16


12


8


4


0



0

|Vitronectin Fibrinogen BSA hIgG<br>n = 786 n = 1,026 n = 959 n = 2,421<br>***|Col2|Col3|Col4|
|---|---|---|---|
|BSA<br>Vitronectin<br>Fibrinogen<br>hIgG<br>_n_ = 786<br>_n_ = 1,026<br>_n_ = 959<br>***<br>_n_ = 2,421|BSA<br>Vitronectin<br>Fibrinogen<br>hIgG<br>_n_ = 786<br>_n_ = 1,026<br>_n_ = 959<br>***<br>_n_ = 2,421|BSA<br>Vitronectin<br>Fibrinogen<br>hIgG<br>_n_ = 786<br>_n_ = 1,026<br>_n_ = 959<br>***<br>_n_ = 2,421||
|_n_ = 1,312|_n_ = 1,421|_n_ = 1,324|***<br>_n_ = 2,113|
|_n_ = 1,312|_n_ = 1,421|_n_ = 1,324||
|||||



Relative frequency


Solid mechanics three-dimensional model











1,600


1,200


800


400


0


800


600


400


200





Density dependence


8


4


0




|n = 510|n = 955|n = 689|
|---|---|---|
||||
||||











NS


**Fig. 6 |** **Measuring phagocytic forces generated by individual human macrophages.** **a**, Representative images of hMDMs on hIgG cross patterns showing
a range of phagocytic responses. **b**, Representative image of actin-stained hMDMs spread over circular patterns in an array. High rates of single-cell
pattern coverage are achieved. **c**, Phagocytic contraction of (1) ring, (2) cross and (3) filled hIgG circular patterns. The three distributions of single-cell
responses were not significantly different. **d**, Opsonin dependence in phagocytic contraction. Vitronectin, fibrinogen, BSA and hIgG were patterned in
50 μ​m cross shapes on a stiffer, 67:1 base:crosslinker (top) and softer 71:1 (bottom) substrate. HIgG elicited the most contractile response from the largest
fraction of macrophages, consistent with the role and urgency of antibody opsonization in immunity. The left _y_ axis represents displacement, while the
right _y_ axis represents applied forces. A typical pattern representing each distribution in the 67:1 case is shown below. *** _P_ <​0.001. In **c** and **d**, _n_ represents
the number of cells in each distribution. **e**, Finite element method modelling of forces exerted by a phagocytosing macrophage. Forces were modelled as
boundary loads on a linear elastic material and exerted between all pairs of adjacent terminals of the cross pattern. The shape of the non-displaced pattern
is outlined in white and the 5 μ​m ×​ 10 μ​m area over which force was applied is shaded. Left: complete geometry comprising a 150 μ​m ×​ 150 μ​m elastic
material with 90 μ​m thickness. Middle: top view showing the direction of applied tangential forces, indicated by arrows. Right: cross-sectional view of
one-quarter of the geometry at 50% opacity, highlighting the response of the material to the boundary load and indicating the direction of net
displacement. Internal columns of material are depicted only to emphasize the displaced geometry due to applied forces and do not represent real
boundaries in the material. The Kruskal–Wallis test for non-parametric data was used to perform statistical analyses on the contractile distributions for the
opsonin dependence experiment, with significance defined as _P_ <​ 0.05. For the density dependence experiment, a one-way analysis of variance ruled out
any significant differences. Scale bars, 25 µ​m. NS, not significant.



differentiated from a heterogeneous pool of monocytes [31], had
become activated by these molecules through interactions with
other (non-FcR) receptors, ultimately converging in downstream
signalling pathways leading to phagocytosis—further supporting
the notion that phagocytic force generation acts in a digital manner.


**Macrophages generate hundreds of nanonewtons of force during**
**phagocytosis.** Using finite element method solid mechanics modelling based on the micropattern displacements and mechanical properties we measured for the material, we approximated the forces
applied onto the micropatterns. We found that MDMs that were
engaged in FcR-mediated phagocytosis generated median forces
of ~350 nN while a number of outlier cells were capable of forces
as large as 1 µ​N (Fig. 6d–e). Median forces generated by MDMs on
the other opsonins were significantly less, never exceeding 100 nN.
Forces in the 10 [−][7] N range have previously been reported for other
human cells, including MSCs, human umbilical vein endothelial
cells [22] and keratinocytes [32] . Phagocytic forces in this range should



be expected as the adhesive strengths of certain bacteria were also
found to approach the µ​N range [33] . It is also interesting to note that
the macrophages generated similar levels of force on both substrates despite differences in their stiffnesses, since a previous study
reported a correlation between forces in migrating macrophages
and substrate stiffness [34] . The lack of such a relationship here is probably due to the difference in behaviours being analysed. Specifically,
while there may be physiological reasons for more rapid migration
on stiffer surfaces, there does not appear to be a benefit to modulating the phagocytic force if the objective is rapid clearance of a foreign entity. Moreover, it is possible that the response is only linear
on the small range of stiffnesses we tested (4–8 kPa), and that it may
behave differently over a larger range. Overall, this analysis represents the first direct quantification of the contractile forces involved
in the closure of the phagocytic cup.


**Subclasses of IgG stimulate similar phagocytic force generation.**
A recent study reported minor differences in the ability of different



**130** **Nature Biomedical Engineering** [| VOL 2 | FEBRUARY 2018 | 124–137 | www.nature.com/natbiomedeng](http://www.nature.com/natbiomedeng)


© 2018 Macmillan Publishers Limited, part of Springer Nature. All rights reserved.


#### NATure BIomedIcAl EngIneerIng Articles



IgG subclasses to stimulate the phagocytic uptake of _Salmonella_
bacterial cells by a monocytic cell line [35] . We asked whether these
differences were triggered at the force-generation level. Using a
humanized panel of the four subclasses of IgG antibodies, we found
that all subclasses induced significant and comparable increases in
phagocytic force over the non-opsonized controls. We observed
a similar result for another phagocyte—matched immature
monocyte-derived dendritic cells derived from the same patient
(Supplementary Fig. 7). It is not entirely surprising that MDMs
and monocyte-derived dendritic cells produced similar forces since
both are professional phagocytes with the same general targets; for
example, bacteria, parasites and debris. However, these results suggest that if phagocytic uptake efficiency does indeed differ among
the subclasses, it is not a result of differences in force generation.


**Pharmacological inhibition of actin polymerization but not of**
**phagosome acidification reduces the phagocytic force.** Actin
polymerization has long been known to be required for phagocytosis, with target uptake assays showing that actin inhibitors greatly
reduce phagocytic efficiency, particularly with Fc-opsonized targets [36] . Given its role in phagosomal closure, it is logical that inhibition of polymerization would reduce the phagocytic force. Following
closure, the internal phagosomal pH progressively decreases,
enhancing its microbicidal activity [37] . It remains unknown whether



there is feedback between phagosome maturation and the sustained
maintenance of a phagocytic force.
We used FLECS to confirm the direct role of actin polymerization in phagocytic force and also to determine whether disruption
of phagosomal acidification (a late-stage event) feeds back into the
control of the earlier mechanical stages of phagocytosis. We treated
MDMs with cytochalasin D or chloroquine at three doses to block
actin polymerization or phagosomal acidification, respectively.
MDMs were either seeded directly into drug-containing medium
or incubated with the drug after achieving steady-state phagocytic contraction on hIgG 'X' patterns. As expected, incubation
with cytochalasin D at all the tested doses substantially decreased
the measured phagocytic contraction, while pre-treatment completely prevented any measureable contraction, confirming the
requirement of actin polymerization in phagocytic force generation
(Fig. 7a–d). Treatment with chloroquine had no effect on the
mechanical output of the macrophages, indicating that the earlystage mechanical encapsulation and chemical maturation involved in
phagocytic clearance are uncoupled in both the long and short term.


**PI3K inhibition reduces the forces generated during FcR-**
**mediated phagocytosis.** Finally, we investigated the role of a
specific phosphatidylinositide 3-kinase (PI3K) isoform, p110δ​, in
phagocytic force. Among other roles, PI3Ks regulate phagocytosis



**a**


**c**


|Col1|Pre-treatment|Col3|
|---|---|---|
|= 1,629<br>_n_|= 1,624<br>_n_ = 2,206|_n_ = 2,042|
|= 1,585<br>_n_ = 1,735<br>_n_ = 1,983<br>_n_ = 1,861|= 1,585<br>_n_ = 1,735<br>_n_ = 1,983<br>_n_ = 1,861|= 1,585<br>_n_ = 1,735<br>_n_ = 1,983<br>_n_ = 1,861|
|= 2,079<br>_n_|= 2,357<br>_n_ = 2,069|_n_ = 2,036|
||||



**d**



Pre-treatment **b** Delivery post-contraction



16


12


8


4


0











16


12


8


4


0





16


12


8


4


0





16


12


8


4


0


16


12


8


4


0


16


12


8


4


0







Vehicle



0.1 μM



Vehicle 0.1 μM 1 μM 10 μM



1 μM 10 μM



***



6


5


4


3


2


1











Vehicle


Chloroquine



Vehicle


Cytochalasin D



Vehicle



Vehicle


Cytochalasin D



Vehicle



***


CAL-101



CAL-101



Vehicle


Chloroquine



**Fig. 7 |** **Effects of chloroquine, cytochalasin D and CAL-101 on hMDM contractile force.** **a**, Contraction distributions of hMDMs engaging IgG-opsonized
micropatterns pre-treated with DMSO or three doses of each drug. **b**, Contraction distributions of hMDMs engaging IgG-opsonized micropatterns
incubated with DMSO or three doses of each drug for 15 min after reaching steady-state contraction. In **a** and **b**, the data are pooled from four technical
replicates and ' _n_ ' represents the number of cells in each distribution. A bimodal distribution was observed reflecting an 'active' phagocytosing population
(red curve) and a weakly adhered, inactive population (blue curve). A mixed Gaussian distribution is fitted to each plot to obtain information about the
active populations, which is used for quantification. **c**, **d**, Median contraction levels of the active populations in **a** and **b**, respectively. Bars represent the
mean of four measurements (overlayed as dots) and error bars represent the s.e.m. of no treatment and treatment with DMSO control. Measurements
were compared using analyses of variance followed by two-tailed Bonferoni-corrected _t_ -tests. * _P_ <​ 0.05; ** _P_ <​ 0.01; *** _P_ <​ 0.001. NS, not significant.


**Nature Biomedical Engineering** [| VOL 2 | FEBRUARY 2018 | 124–137 | www.nature.com/natbiomedeng](http://www.nature.com/natbiomedeng) **131**


© 2018 Macmillan Publishers Limited, part of Springer Nature. All rights reserved.


#### Articles NATure BIomedIcAl EngIneerIng

































by driving re-arrangement of actin in phagosome formation [38][,][39] .
Class 1A PI3Ks—the p110α​, p110β​ and p110δ​ isoforms—positively regulate the small G protein Rac1 (ref. [40] ), which coordinates
actin organization and is required for FcR-mediated phagocytosis [41][,][42] . Of these, the p110δ​ isoform has also been shown to
selectively reduce phosphorylation of Akt, which is an upstream
effector of FcR-mediated phagocytosis [43] and negatively regulate the PI3K antagonist PTEN in murine macrophages [44] . To test
whether PI3Kδ​ inhibition attenuates the forces generated in FcRmediated phagocytosis, we subjected hMDMs contracting our
hIgG micropatterns to three steps of tenfold dilutions of the selective p110δ​ inhibitor CAL-101.
We found that at the effective dose of 1 µ​M, compared with
the vehicle control, CAL-101 produced statistically significant
relaxations in micropatterns occupied by the active population of
macrophages, and at 10 µ​M the effect was even more pronounced,
indicating a dose-dependent response (Fig. 6a–d). Although pretreatment with CAL-101 produced a more robust relaxation at all
doses, the post-contraction incubation revealed the rapid onset of
this effect (which became noticeable within 15 min of compound
addition) and corroborated the requirement of PI3K activity for
sustained force generation. This observation shows that PI3K plays
a direct role in phagocytic force generation. The partial suppression
of baseline phagocytic force at the effective dose is consistent with
reports that PI3K inhibition blocks phagocytosis of large targets but
not smaller ones [38] . It is also possible that the redundant functions
of the other class 1A PI3Ks helped to mitigate the relaxing effects
of this selective p110δ​ inhibition. This observation is important to
consider in terms of the potential immunosuppresive side effects of
CAL-101, which is currently in phase III clinical trials for the treatment of chronic lymphocytic leukaemia (Clinical Trials Identifier
NCT01539291).



**Discussion**
The FLECS system combines advances in the preparation of biofunctionalization of soft materials with compatibility with automation workflows to enable high-throughput and multi-modal
analysis of large populations of a variety of contractile cells. The
core material allows for independently tunable stiffness, pattern
shape and molecular composition, enabling it to be tailored to a
broad range of cell types and their functions. The seamless integration with well-plate formats enables direct use with screening
robotics and high-content imagers, as well as simple adoption by
end users. As such, this system has the potential to address both
research and industrial applications.
For example, the functionalization of our sensors with immunological molecules enables the study of phagocytosis of large targets.
Traditional phagocytosis assays are endpoint measurements that
look at the total engulfment by phagocytes of exclusively smaller
targets. In contrast, our larger, surface-bound targets are a good
model for phagocytosis of tissue-like structures such as biofilms or
tumour cells embedded in tissue. In addition to quantifying phagocytic force, this method could help determine which factors can
lead to improved immune cell disruption of such pathogenic tissue-like structures. By simply altering the surface functionalization,
evaluations of forces by many other cell types, including SMCs and
cardiomyocytes (Supplementary Fig. 8 and Supplementary Videos
8–10) also become possible.
The compatibility of the FLECS system with automation enables
precise execution of multi-parametric studies of large quantities of
different cells. We were able to simultaneously evaluate tone, responsiveness to an agonist and subsequent responsiveness to a countering antagonist for >​1,000 cells from each of 12 patient-derived cell
lines at once using a single FLECS well-plate. The overall yield of
~31,000 cells on the plate, of which ~24,000 were robust responders



**132** **Nature Biomedical Engineering** [| VOL 2 | FEBRUARY 2018 | 124–137 | www.nature.com/natbiomedeng](http://www.nature.com/natbiomedeng)


© 2018 Macmillan Publishers Limited, part of Springer Nature. All rights reserved.


#### NATure BIomedIcAl EngIneerIng Articles



and used for analysis, exceeds previously reported throughputs for
individual contractility experiments (which we define as comprising a single cell-seeding session and single execution of analysis
software) by 100-fold. By analysing this many cells simultaneously,
we were able to definitively report that asthma HASM innately produces larger forces than non-asthma HASM.
Although we observed clear differences between multi-potent
and differentiated cells, the differences between osteocytes and adipocytes were less apparent, despite past reports showing such differences using micropost arrays [22] . Whether this discrepancy is a result
of the fundamentally different physical environments presented to
the cells (continuous planar versus discretized deflectable pillars),
different culture conditions (in situ versus in vitro) or resolution
limitations is unclear. Therefore, it is important to note that each
of the three major laboratory methods for measuring cellular force
offer unique strengths and limitations, and a given biological problem may be better suited to one method over another. These are
summarized in Table 1 and discussed below.
TFM and micropost array methods offer superior spatial resolution that is able to assign force vectors to specific focal adhesions
and measure very subtle forces in small cells like T cells. Advanced
TFM techniques are now able to map complex sub-cellular forces
in three-dimensional polymer and gel networks. In general, both
methods should remain the standard for addressing specific biological questions relating to sub-cellular force generation by small numbers of cells. However, this resolution comes at the cost of simplicity
and throughput, as these methods typically require high magnification imaging and manual user input during analysis workflows.
Thus, as shown in Table 1, the experimental data throughputs have
generally been limited to 10–50 cells.
In comparison, FLECS yields a larger quantity of single-cell data
per experiment than the older methods. Instead of manually tracing
or fixing and staining cells (which may alter the observable contractile phenotype substantially), FLECS analysis locates live cells
based on nuclear staining co-localized to micropattern sites using
automated template-matching and binary segmentation algorithms.
Thus, no user input is required and all imaged cells are analysed,
thereby removing the potential for selection bias. Furthermore,
by taking whole-cell rather than sub-cellular force measurements,
FLECS is able to extract quantitative data from much larger fields
of view with smaller pixel sizes (for example, data presented in Figs.
3 and 4 were extracted from images taken with 1.61 µ​m px [–1] sizes)
relative to the older methods. Finally, as discussed at length, FLECS
is the only methodology demonstrated to integrate into a highthroughput phenotypic screening configuration that maintains
single-cell resolution. These features enable FLECS to achieve the
described 100-fold improvements in throughput.
All three methods are suitable for performing time-course measurements of cellular force. However, in addition to throughput
limitations, unconstrained cells in the native TFM and micropost
systems migrate and require precise monitoring, adding a layer of
complexity to the measurements. This problem can be overcome by
incorporating micro-contact printing steps to restrict cell motion,
although this may present additional fabrication difficulties. With
FLECS, cells are inherently restricted to micropatterns and do not
migrate. For the same reason, FLECS inherently provides single-cell
resolution, which allowed us to longitudinally track cellular contractility following calcium imaging in the same single cells to discover
that peak measurements in these two modes are not well correlated
despite calcium flux being commonly used as a direct upstream
indicator, as well as to select for responding cells from both HASM
and macrophage populations to cleanly resolve agonist effects.
As a result of these unique advantages, FLECS has the potential
to become the leading technology for phenotypic drug discovery
pertaining to conditions involving aberrant cellular force generation. Compared with target-based screening, phenotypic screening



has produced more first-in-class medicines due to its naturally
unbiased identification of the molecular mechanism of action [45] .


**Methods**
**Preparation of patterned ultra-soft substrates.** The wafer-scale process is shown
in Supplementary Fig. 9 and has been described in detail previously [46] . Briefly, a
20% dextran solution (70 kDa; Sigma–Aldrich) in deionized water was spin-coated
onto plasma-activated silicon wafers and baked until dehydration to yield dextran
substrates. Chrome photomasks containing arrays of micropatterns were designed
using L-Edit software, fabricated off-site and used to pattern SPR 220 photoresist
on separate silicon wafers. Polydimethylsiloxane (PDMS; Sylgard 184) at 10:1 baseto-crosslinker ratio was cast onto the patterned wafer, cross-linked and demoulded
yielding stamps with positive pattern features. Adhesive biomolecule (for example,
extracellular matrix protein) solution was added to the stamp surface, incubated
for 1 h and air-dried immediately before stamping. The stamped adhesive molecule
or a co-stamped molecule was conjugated with a fluorescent moiety. Dextran
substrates were activated with a brief plasma treatment and stamped with the
biomolecule-adsorbed PDMS stamps for 5 min. Ultra-soft PDMS mixture (55:1 to
71:1) was spin-coated (1,200 rpm; 20 s) over the stamped dextran-coated silicon
and cured (24 h at room temperature followed by 7 days at 65 °C). Once cured, the
substrate could be stored stably at room temperature for more than nine months.


**Releasing substrates and seeding with cells.** To begin an experiment, the substrate
was mounted onto cover glass (where the PDMS layer was in contact with the
cover glass) and placed into saline solution to release the soluble dextran layer and
yield a glass-backed elastomeric thin-film with embedded proteins. This substrate
could be fabricated as large as a well-plate footprint. Following fabrication, the
sample was sterilized by washes in strong base followed by washes in sterile
deionized water. Non-patterned regions were blocked in a 0.5% solution of
Pluronics F-127 (45 min at room temperature) and cells of interest were seeded. For
live imaging experiments, Hoechst 33342 nuclear stain was added to the culture
medium (1 μ​g ml [−][1] final concentration). If cells were to be fixed, the nucleus was
stained after fixation. The sample was washed to remove non-adhered cells after
2 h. At the conclusion of the experiment, the sample was either left unfixed or fixed
in 4% paraformaldehyde solution at room temperature for 1 h, mounted using
4',6-diamidino-2-phenylindole-infused mounting medium and imaged.


**Imaging and image analysis.** In our experiments, fluorescent patterns (green
or red channel) and cell nuclei (blue channel) were imaged at 10×​ magnification
with a Nikon fluorescence microscope in fixed-sample experiments, or with the
ImageXpress Micro XL High-Content Imaging System fluorescence microscope
with 10×​ magnification for end-point experiments or 4×​ magnification for timecourse experiments. Image processing was performed using MATLAB.
A separate algorithm was developed for analysing each pattern type. For
experiments using cross (‘X’) patterns, a template was used to locate all patterns
in all frames. The mean distance between the centre and each terminal of each
pattern comprised a data point. For experiments using circular patterns, the native
MATLAB function _imfindcircles()_ was used to identify all circular shapes in each
frame and measure their radii. The presence or absence of a stained nucleus at
the corresponding _xy_ location of the nuclear image determined whether a given
pattern was used for the control or experimental data or was rejected as having
multiple cells (Supplementary Fig. 2a). All experimental data measurements
were zeroed to the median of the measurements of control case patterns yielding
net displacement histogram plots. Raw measurements were also saved in a
.mat format. M-Files containing the algorithms for calculating ‘X’ micropattern
displacements and measuring dye intensity within adhered cells are supplied in the
Supplementary Information.
During processing, a file containing (1) an image of each cross pattern marked
at the computed centre and vertices, or an image of each circular pattern overlaid
with the circle fitted by the _imfindcircles()_ function, alongside (2) an image of the
corresponding nuclear signal labelled with the computed cell count, was created
and saved for each pattern–nuclear-signal pair for later viewing and quality control
(Supplementary Fig. 2b).


**Study on mesenchymal stem cells.** _Cell culture and differentiation._ Human MSCs
derived from bone marrow or adipose tissue (StemPro; Thermo Fisher Scientific)
were maintained in MesenPRO RS Medium. Differentiation was induced by 14-day
culture in adipogenic (StemPro Adipogenesis Differentiation Kit) or osteogenic
(StemPro Osteogenesis Differentiation Kit) inductive medium as described in the
manufacturer’s manual. Trypsin-EDTA (0.05%) was used to re-suspend cells at the
start of the experiment. Seeding and culturing on FLECS substrates was done in
Dulbecco’s modified Eagle's medium (DMEM; Invitrogen) supplemented with 10%
MSC-qualified foetal bovine serum (FBS), 100 units ml [−][1] penicillin and 100 μ​g ml [−][1]
streptomycin. Early passages (<​7) of hMSCs were used in all experiments.


_Substrate parameters._ Cross-shaped patterns (70 μ​m diagonal; 10 μ​m bar thickness)
spaced at 100 μ​m centre-to-centre vertical and horizontal distances were used
for this experiment. Substrates were prepared by adsorbing 0.5 ml of 30 μ​g ml [−][1]



**Nature Biomedical Engineering** [| VOL 2 | FEBRUARY 2018 | 124–137 | www.nature.com/natbiomedeng](http://www.nature.com/natbiomedeng) **133**


© 2018 Macmillan Publishers Limited, part of Springer Nature. All rights reserved.


#### Articles NATure BIomedIcAl EngIneerIng



fibronectin and 30 μ​g ml [−][1] Alexa-Fluor-488-conjugated fibrinogen solution to each
of six 22 mm ×​ 22 mm stamps for 45 min before stamping dextran-coated wafers.
PDMS was mixed at a 55:1 base-to-crosslinker ratio.


_Experimental procedure._ Substrates were housed in six-well plates during the
experiment. Cells were seeded by pipetting cell suspensions directly over the
substrates. After 1 h, non-adhered cells were washed away. Cells were fixed with
warmed 4% paraformaldehyde, and the substrates were mounted onto glass
slides using 4',6-diamidino-2-phenylindole-infused mounting medium (P-36931;
Thermo Fisher Scientific) 8 h after seeding and later imaged.


_Actin staining._ Following fixation but before mounting, a subset of all MSC
samples was permeabilized with 0.25% Triton X-100 (Sigma–Aldrich) for 10 min
and incubated with 1:500 Alexa Fluor 568 Phalloidin (A12380; Thermo Fisher
Scientific) in phosphate buffered saline (PBS) for 20 min at room temperature.


**Study on tonic traction forces supplied by primary human SMCs.** _Cell culture._
Cryopreserved human primary bronchial, uterine and aortic SMCs were purchased
from PromoCell. The cells were maintained in complete Smooth Muscle Cell
Medium (PromoCell) supplemented with 100 units ml [−][1] penicillin and 100 μ​g ml [−][1]
streptomycin. Trypsin-EDTA (0.05%) was used to re-suspend cells at the start
of the experiment. Seeding and culturing on FLECS substrates was also done in
Complete SMC 2 Medium (PromoCell). An end-point measurement was obtained
from one well for each SMC source 8 h after seeding.


**Blebbistatin titration.** Blebbistatin (Sigma–Aldrich) was dissolved in DMSO to
achieve working concentrations using 10 steps of twofold dilutions beginning
with 25 µ​M. HASM cells were seeded 24 h before treatment with blebbistatin. On
the day of the experiment, cells were stained with Hoechst, washed, treated with
blebbistatin (1% DMSO final concentration), incubated for 30 min and imaged live
using the ImageXPress Micro XL High-Content Imaging System.


_Statistical analysis._ Each concentration of blebbistatin was tested in four technical
replicates. The median contraction at each concentration was normalized by
vehicle-treated contraction. GraphPad Prism 6 graphing software was used to
fit a sigmoid curve to the dose-response data and calculate the half-maximal
inhibitory concentration.


**Evaluation of asthma and non-asthma patient-derived HASM.** _Isolation and_
_culture of HASM._ All lines of HASM cells were derived from tracheas obtained
from the National Disease Research Interchange (Philadelphia, PA, USA) and the
International Institute for the Advancement of Medicine (Edison, NJ, USA). HASM
cell culture was performed as described previously [47][–][49] . Briefly, the cells were
cultured in Ham’s F12 medium supplemented with 10% FBS, 100 U ml [–1] penicillin,
0.1 mg ml [–1] streptomycin and 2.5 mg ml [–1] amphotericin B, and this medium was
replaced every 72 h. HASM cell passages 1–6 were used for all experiments because
these cells retain the expression of native contractile protein, as demonstrated by
immunocytochemical staining for smooth muscle actin and myosin [47] . The HASM
cells were derived from donors with fatal asthma or donors who were age and
gender matched without asthma, as shown in Supplementary Table 1.
The 12 distinct patient cell lines were seeded into 8 wells column-by-column,
alternating between non-asthmatic and asthmatic lines, in each of 3 FLECS wellplates at approximately 5,000 cells per well and allowed to adhere for 2 h, at which
point serum was removed for 24 h before pro-contractile agonists were added.


_Basal tone._ The three plates were imaged on an ImageXpress High-Content imager
with environmental controls before any stimulation to get a basal measurement
for contraction.


_Responsiveness to bradykinin and formoterol._ Immediately after acquiring baseline
images, one of the three well-plates (selected at random) was used to perform
pharmacological studies, and a multi-drop instrument (BioTek) was used to deliver
bradykinin (Sigma–Aldrich) to all 96 wells at a final concentration of 10 µ​M. The
plate was replaced on the imager and each well was imaged for 16 min at 4-min
intervals. Following the last imaging time point, the plate was removed and the
multi-drop was used to deliver 50 µ​M formoterol (Sigma–Aldrich) to every odd
row or 1% DMSO in serum-free medium to every even row. The plate was again
replaced and imaged an addition six time points. Analysis software was used to
track the contractile behaviour of each of the 250–450 cells adhered within each
well (>​31,000 cells in total) over the course of the experiment, and those cells
exhibiting a positive contraction between the initial and fourth time point (after
16 min of bradykinin stimulation but before formoterol or vehicle) were selected
for further analysis—approximately 24,000 cells.


**Simultaneous measurements of calcium release and contractility in HASM**
**single cells.** _Experimental._ HASM cells derived from a single healthy patient were
seeded into a FLECS well-plate as described above and serum-starved for 24 h.
Before imaging, cells were incubated with 4 µ​M Fluo-8 (Abcam) and 1 μ​g ml [−][1]
Hoechst 33342 for 1 h and then washed with fresh serum-free medium. To start



the experiment, 20 wells were imaged using 4×​ magnification on the ImageXpress
to get a baseline reading. The plate was immediately transported to a table-top
manual fluorescence microscope (Nikon) where serum-free medium, 20% FBS
(Thermo Fisher Scientific), 10 µ​M bradykinin, 100 nM endothelin-1 (Sigma–
Aldrich) or 10 µ​M histamine (Sigma–Aldrich) was added to four wells each,
one-by-one, and the calcium dye intensity was imaged for 30 s at 100-ms intervals
(see Supplementary Video 6). After the imaging was complete for the final well,
the plate was transported back to the high-content imager to acquire images of the
micropatterns for 25 min at 1-min intervals.


_Analysis._ Image series of the micropatterns and image series of the calcium signal,
which were acquired on separate microscopes, were registered using corresponding
images of stained cell nuclei taken through both microscopes, which produced
a unique intensity signature at each site allowing simple registration in ImageJ.
Single-cell contraction was assessed as usual. Micropatterns in the images taken
at the initial time point were used to define regions of interest for each cell within
which calcium dye intensity was calculated for every frame and normalized to
initial intensity. In the case of 20% serum, addition generated significant sustained
auto-fluorescence so the authors manually adjusted the reference intensity for
those wells as it was clear from the traces when the calcium peaked relative to
the addition of serum. The other agonists did not produce a sustained autofluorescence. Both the calcium release and contractility traces were pooled and
averaged to generate the mean traces shown in Fig. 4c. The initial calcium peaks
were used to register all calcium traces before averaging. The peak values obtained
from each single-cell contractility and calcium trace were also displayed in a scatter
plot to generate Fig. 4d.


**Phagocyte experiments.** _Macrophage differentiation._ Human peripheral blood
monocytes were isolated from blood taken from consenting healthy adult donors
using density gradient centrifugation with Histopaque-1077 solution (Sigma–
Aldrich) according to University of California, Los Angeles Institutional Review
Board protocol 14-000522. Collected mononuclear cells were washed in saline,
re-suspended in unsupplemented RPMI 1640 Medium (Life Technologies) and
allowed to adhere to the well surfaces within polystyrene 6-well plates for 2 h.
The wells were then washed to remove contaminating lymphocytes and refilled
with warm RPMI 1640 Medium supplemented with 20% heat-inactivated foetal
calf serum (FCS), 20 ng ml [−][1] M-CSF (Life Technologies), 100 units ml [−][1] penicillin
and 100 μ​g ml [−][1] streptomycin. Monocytes were allowed to differentiate into
macrophages (hMDM) for seven days. All macrophages were used within this
period as the phagocytic force was significantly reduced in macrophages aged
>​14 days and completely suppressed in macrophages aged 21 days (Supplementary
Fig. 10). To begin an experiment, macrophages were dissociated from the
well-plates by incubation in StemPro Accutase (Life Technologies) for 30 min
at 37 °C, followed by vigorous pipetting up and down to complete dissociation.
Macrophages were re-suspended in RPMI 1640 Medium supplemented with 10%
heat-inactivated FCS, 100 units ml [−][1] penicillin and 100 μ​g ml [−][1] streptomycin before
seeding onto the FLECS chips. Macrophages were imaged live without fixing in all
experiments and Hoechst 33342 (1 μ​g ml [−][1] ) was used to stain the cell nuclei.


_Dendritic cell differentiation._ Dendritic cells were prepared in the same manner
as macrophages, but using differentiation medium containing 100 ng ml [−][1]
granulocyte-macrophage colony-stimulating factor and 50 ng ml [−][1] interleukin 4
instead of M-CSF.


_Patterning antibodies._ To pattern the IgG antibodies, a 45 μ​g ml [−][1] dansyl-conjugated
BSA and 45 μ​g ml [−][1] Alexa-Fluor-488-conjugated BSA solution were adsorbed to a
stamp and stamped onto a dextran-coated wafer. After the substrates were coated
with PDMS, cured, released and blocked with Pluronic F-127, but before the
macrophages were seeded, approximately 50 μ​l per 400 mm [2] of 25 μ​g ml [−][1] solution
of human–mouse chimeric anti-dansyl IgG antibodies was spread over each
patterned substrate and incubated for 3 h at room temperature. Excess antibody
was then washed with saline. The human–mouse chimeric antibodies were
developed by ref. [50] .


_Density dependence experiment._ Circular patterns with 54 μ​m diameters
but with various degrees of filling were patterned with IgG as described above.
Specifically, the following were patterned: (1) a ring pattern with 10 μ​m thickness
(inner diameter subtracted from the outer diameter), (2) the same ring pattern
encircling a symmetric cross shape with a 10 μ​m bar thickness and (3) a solid circle.
PDMS was mixed at a 65:1 base-to-crosslinker ratio. Macrophages were imaged 6 h
after seeding.


_Opsonin dependence experiment._ Human recombinant vitronectin (Advanced
BioMatrix), fibrinogen (Life Technologies) and BSA (Life Technologies) conjugated
with Alexa Fluor 488 and hIgG (as described above) were patterned in cross shapes
(50 μ​m diagonal and 20 μ​m bar thickness). The total quantities of each ligand were
set to be approximately uniform by modulating the concentrations of the adsorbing
ligands and confirmed by measuring the fluorescence intensities of the resulting
transferred patterns (Supplementary Table 2). Macrophages were dissociated as



**134** **Nature Biomedical Engineering** [| VOL 2 | FEBRUARY 2018 | 124–137 | www.nature.com/natbiomedeng](http://www.nature.com/natbiomedeng)


© 2018 Macmillan Publishers Limited, part of Springer Nature. All rights reserved.


#### NATure BIomedIcAl EngIneerIng Articles



described, seeded and imaged live 6 h later. PDMS was mixed at both 67:1 and 71:1
base-to-crosslinker ratios.


_Patterning equal quantities of different opsonins._ Testing the phagocytic force
response of hMDMs as a function of the opsonin type required patterning of
three different ligands: vitronectin, fibrinogen and dansyl-BSA (hIgG was
not patterned, but rather used to bind the dansyl-BSA in which the conjugated
dansyl group served as the binding site for the IgG antibodies). To decouple
the potential effects of differential opsonin quantities from the opsonin type,
we set out to equalize the molar quantities of each opsonin on our substrates.
To accomplish this, each opsonin was labelled with the same fluorophore
(Alexa Fluor 488), and the respective degree of labelling (DOL) along with the
fluorescent intensities of the patterns as a function of the solution concentration
(used in the adsorption step) were used to achieve the same final surface densities.
For each fluorescence intensity measurement, 10×​ magnification and 2 s exposure
times were used.


_Fibrinogen._ Alexa-Fluor-488-conjugated fibrinogen was purchased from Life
Technologies (catalogue number F13191; lot number: 1636855) with a DOL
of 6. This was the same ligand as was used for the hMSC and dose-response
experiments and was adsorbed to the PDMS stamps for 45 min before being
stamped onto the dextran-coated wafers for 5 min. Three concentrations
(30, 20 and 10 μ​g ml [–1] ) were tested to create a concentration-versus-fluorescenceintensity curve.


_BSA._ Alexa-Fluor-488-conjugated BSA was purchased from Life Technologies
(catalogue number A13100; lot number 1348652) with a DOL of 7. Alexa-Fluor488-conjugated BSA was co-patterned with dansyl-BSA since Alexa-Fluor-488conjugated BSA was used for fluorescently visualizing the pattern while dansylBSA contained the epitope (dansyl) targeted by our human–mouse chimeric
antibody. Thus, the two BSA molecules were patterned in equal quantities at three
concentrations (60, 30 and 20 μ​g ml [–1] each) to create a concentration-versusfluorescence-intensity curve. In addition to the general procedure, the PDMS
stamps were plasma treated before adsorption to promote wetting and, during
stamping, the stamps were kept in contact with the dextran-coated wafers under
weight for 20 min rather than 5 min.


_HIgG._ BSA patterns were prepared as described with the addition of hIgG (50 μ​l of
25 μ​g ml [−][1] solution per 400 mm [2] ) after the release, sterilization and blocking steps.


_Vitronectin._ Human recombinant vitronectin was purchased from Advanced
BioMatrix (catalogue number 5052) and conjugated with Alexa Fluor 488 in house
using Alexa Fluor 488 carboxylic acid and succinimidyl ester (Life Technologies) at
a 8:1 fluorophore-to-protein molar ratio in PBS (4 h at 4 C). Following the reaction,
the vitronectin solution was dialysed against PBS for 48 h with PBS changes every
12 h to remove unreacted dye. The DOL for the vitronectin–Alexa Fluor 568
conjugate was calculated to be 6.25 using absorbance readings taken at 494 and
280 nm, as prescribed in the manufacturer’s manual provided with the conjugation
kit (Life Technologies), and using 1.02 ml mg [−][1] cm [−][1] as the extinction coefficient for
vitronectin [51] . Three concentrations (40, 30 and 20 μ​g ml [−][1] ) were tested to create a
concentration-versus-fluorescence-intensity curve. As with BSA, the stamps were
plasma treated before adsorption and were kept in contact with the dextran-coated
wafers under weight for 20 min.


_BSA._ BSA was found to saturate in fluorescence intensity when 30 μ​g ml [−][1] and
higher concentrations were used for each BSA conjugate. However, concentrations
of 60 μ​g ml [−][1] produced the most consistent transfers so this concentration was
chosen for BSA. This maximum BSA intensity was normalized by the DOL for BSA
and adjusted by a factor of two to account for the equal part of non-fluorescent
BSA (dansyl-BSA). Referencing this ‘target’ normalized intensity (termed the
‘relative surface molarity coefficient’), along with the concentration-versusfluorescence-intensity curves constructed for vitronectin and fibrinogen and their
DOLs, we predicted the adequate concentrations to be 30 μ​g ml [−][1] and 10 μ​g ml [−][1] for
vitronectin and fibrinogen, respectively.


**Approximation of phagocytic forces.** _Substrate stiffness measurement._ Cylindrical
PDMS samples (67:1 and 71:1) were placed onto an Instron tensile tester (model
5564) with a 2.5 N load cell, and compressive testing of the sample was performed
at a strain rate of 1 mm min [–1] for a total indentation of 1.5 mm. The data were
used to generate load-displacement curves. The slope of the linear portion of the
curve, cross-sectional area of the indentation tip and PDMS sample heights were
used to calculate stiffness. Three samples of each stiffness were test after one and
three weeks of curing (Supplementary Fig. 11). The results showed no significant
stiffening after one week, indicating that the polymer was fully cured at one week
and these unchanging stiffness values could be used for modelling cellular traction
forces. The mean calculated stiffnesses were used in force approximations.


_Finite element method modelling._ To approximate the forces applied by
phagocytosing macrophages on the ultra-soft substrates, the FLECS ‘X’ pattern was



simulated using the finite element model software COMSOL. Specifically, a single
cross-shaped pattern corresponding to the experimental patterns (50 μ​m diagonal
and 10 μ​m bar thickness) was simulated. We modelled the ultra-soft substrates as
linear elastic materials with Young’s moduli of 4,000 and 7,900 Pa (corresponding
to 71:1 and 67:1 PDMS ratios, respectively), a density of 970 kg m [–3], a Poisson’s
ratio of 0.49999 and the forces exerted by macrophages as boundary loads directed
tangentially between all pairs of adjacent terminals of the ‘X’ pattern. The substrate
was modelled as a 150 μ​m by 150 μ​m film with a thickness of 90 μ​m and was
discretized into tetrahedral mesh elements. A 90 μ​m thickness was selected to
minimize the computational intensity associated with higher degrees of freedom,
as thicknesses greater than 70 μ​m did not yield significant changes in the pattern
deflection for a given applied force (empirically, substrates were determined to be
approximately 110 μ​m thick using an automated fluorescence microscope to find
the two focal planes containing either the embedded patterns or the glass substrate
and calculating the distance between them). The bottom of the modelled substrate
was assigned a fixed boundary condition (displacement =​ 0) and tangential forces
ranging from 1 to 250 nN were applied to 5 μ​m ×​ 10 μ​m regions on the top surface
of the modelled substrate at the vertices of the pattern. To compute the pattern
displacement due to an applied force, maximum values of the in-plane deformation
were calculated on the four edges of the pattern region. Due to symmetry,
the points of maximum displacement were located at the centre points of each
terminal boundary—the same locations as where the imaging analysis algorithm
measures displacement.
For this model, the key assumptions of elasticity and linearity hold. Relaxation
of contracted cells with the myosin inhibitor blebbistatin results in patterns
returning to their unperturbed size and shape, suggesting elastic behaviour and
a lack of plastic deformation (Supplementary Video 3). Additionally, previous
work has demonstrated that PDMS behaves as a linearly elastic material under
quasi-static loading conditions [52] . Finally, the observed deflections of the substrate
are small compared with the size of the substrate so we do not expect significant
departures from linearity. This model is similar to that employed by ref. [14],
although our system allows for direct measurement of substrate deflection,
removing the need for including the cell in the simulation.


**Macrophage drug panel.** _Experimental._ Methods for cell culture and substrate
preparation were identical to our earlier macrophage experiments, but using
exclusively hIgG patterns. Chloroquine, CAL-101 and cytochalasin D were
dissolved in medium or DMSO and delivered to FLECS plate wells at final
concentrations of 0.1, 1 and 10 µ​M either before the macrophages were seeded or
after they had maintained adhesion to the patterns for 24 h. When delivery was
before macrophage seeding, imaging was performed 24 h later. When it was after,
imaging was performed 15 min after addition of the drug.


_Analysis._ Since an inactive sub-population of macrophages was prevalent in the
overall population, we fitted a mixed Gaussian curve to each distribution using the
open-source MATLAB function _peakfit.m_ developed by T. O’Haver (University
of Maryland). To obtain the best fit, the two Gaussian widths were restricted
to a minimum of 1, but were otherwise unconstrained. In each case (except for
pre-treatment with cytochalasin D), two Gaussians were clearly identified in the
best fit, representing the inactive (near-zero contraction) and active populations.
Overall curve-fit error rates were low at <​7% and _R_ _[2]_ values were all >​0.93. The
central positions of the Gaussians, representing the active populations, were used
for quantifying the contractile capability of the macrophages following treatment
with vehicle or drug.


**Cardiac myocyte experiments.** _Cell culture and imaging._ Freshly isolated
neonatal rat ventricular myocytes were a generous gift from J. Z. Lee and Y. Wang.
Immediately after isolation, the cells were brought in suspension in DMEM media
supplemented with 1% insulin-transferrin-sodium selenite, and seeded onto
samples patterned either with fibronectin/fibrinogen cross-shaped patterns
(50 μ​m diagonal and 10 μ​m thickness) or 200 µ​m [2] rod-shaped patterns with a 7:1
length ratio. Approximately 6 h after seeding, spontaneous beating was observed in
a fraction of cells. Patterns contracted by beating cells were imaged using fast timelapsed imaging with short exposure times (for example, 100 ms) enabling real-time
observations of the contractions.


_Electrical stimulation._ To pace the cells, an assembly was created based on previous
work [53] . Briefly, carbon rods were placed parallel to each other spaced 5 cm apart in
a petri dish and held in place using cured Sylgard 184. Platinum wire was wrapped
around each carbon rod and connected to either electrode on a Grass Instrument
SD9 pulse generator. Pulse widths of 10 µ​s and 80 V were applied at 1 or 2 Hz to
pace cardiac cells adhered to patterns placed inside the petri dish.


**Life Sciences Reporting Summary.** Further information on experimental design is
available in the Life Sciences Reporting Summary.


**Code availability.** The MATLAB computer code used to evaluate micropattern
displacements and calcium dye intensity is provided as Supplementary
Information.



**Nature Biomedical Engineering** [| VOL 2 | FEBRUARY 2018 | 124–137 | www.nature.com/natbiomedeng](http://www.nature.com/natbiomedeng) **135**


© 2018 Macmillan Publishers Limited, part of Springer Nature. All rights reserved.


#### Articles NATure BIomedIcAl EngIneerIng



**Data availability.** All data supporting the findings of this study are available
within the paper and its Supplementary Information. Source data for most plots
[are available on Figshare through the following DOIs: https://doi.org/10.6084/](https://doi.org/10.6084/m9.figshare.5717842.v1)
[m9.figshare.5717842.v1, https://doi.org/10.6084/m9.figshare.5717845.v1 and](https://doi.org/10.6084/m9.figshare.5717842.v1)
[https://doi.org/10.6084/m9.figshare.5717839.v1.](https://doi.org/10.6084/m9.figshare.5717839.v1)
Source data of large single-cell-contraction distributions are stored in .mat files
and are available from the corresponding author upon reasonable request.


Received: 7 April 2017; Accepted: 9 January 2018;
Published online: 6 February 2018


**References**
1. Discher, D. E., Janmey, P. & Wang, Y.-L. Tissue cells feel and respond to the
stiffness of their substrate. _Science_ **310**, 1139–1143 (2005).
2. Fournier, M. F., Sauser, R., Ambrosi, D., Meister, J.-J. & Verkhovsky, A. B.
Force transmission in migrating cells. _J. Cell Biol._ **188**, 287–297 (2010).
3. Burton, K. & Taylor, D. L. Traction forces of cytokinesis measured with
optically modified elastic substrata. _Nature_ **385**, 450–454 (1997).
4. Evans, E., Leung, A. & Zhelev, D. Synchrony of cell spreading and
contraction force as phagocytes engulf large pathogens. _J. Cell Biol._ **122**,
1295–1300 (1993).
5. Hall, C. N. et al. Capillary pericytes regulate cerebral blood flow in health
and disease. _Nature_ **508**, 55–60 (2014).
6. Pelaia, G. et al. Molecular mechanisms underlying airway smooth muscle
contraction and proliferation: implications for asthma. _Respir. Med._ **102**,
1173–1181 (2008).
7. Yemisci, M. et al. Pericyte contraction induced by oxidative-nitrative stress
impairs capillary reflow despite successful opening of an occluded cerebral
artery. _Nat. Med._ **15**, 1031–1037 (2009).
8. Huang, X. et al. Relaxin regulates myofibroblast contractility and protects
against lung fibrosis. _Am. J. Pathol._ **179**, 2751–2765 (2011).
9. Valencia, A. M. J. et al. Collective cancer cell invasion induced by coordinated
contractile stresses. _Oncotarget_ **6**, 43438–43451 (2015).
10. Gupta, S., Nahas, S. J. & Peterlin, B. L. Chemical mediators of migraine:
preclinical and clinical observations. _Headache_ **51**, 1029–1045 (2011).
11. Munevar, S., Wang, Y. & Dembo, M. Traction force microscopy
of migrating normal and H-ras transformed 3T3 fibroblasts. _Biophys. J._ **80**,
1744–1757 (2001).
12. Park, C. Y. et al. High-throughput screening for modulators of cellular
contractile force. _Integr. Biol. (Camb.)_ **7**, 1318–1324 (2015).
13. Tan, J. L. et al. Cells lying on a bed of microneedles: an approach to isolate
mechanical force. _Proc. Natl Acad. Sci. USA_ **100**, 1484–1489 (2003).
14. Oakes, P. W., Banerjee, S., Marchetti, M. C. & Gardel, M. L. Geometry
regulates traction stresses in adherent cells. _Biophys. J._ **107**,
825–833 (2014).
15. Ricart, B. G., Yang, M. T., Hunter, C. A., Chen, C. S. & Hammer, D. A.
Measuring traction forces of motile dendritic cells on micropost arrays.
_Biophys. J._ **101**, 2620–2628 (2011).
16. Legant, W. R. et al. Multidimensional traction force microscopy reveals
out-of-plane rotational moments about focal adhesions. _Proc. Natl Acad. Sci._
_USA_ **110**, 881–886 (2013).
17. Polacheck, W. J. & Chen, C. S. Measuring cell-generated forces: a guide to the
available tools. _Nat. Methods_ **13**, 415–423 (2016).
18. Myers, D. R. et al. Single-platelet nanomechanics measured by highthroughput cytometry. _Nat. Mater._ **16**, 230–235 (2017).
19. Tseng, Q. et al. A new micropatterning method of soft substrates reveals that
different tumorigenic signals can promote or reduce cell contraction levels.
_Lab Chip_ **11**, 2231–2240 (2011).
20. Rape, A., Guo, W. & Wang, Y. The regulation of traction force in relation to
cell shape and focal adhesions. _Biomaterials_ **32**, 2043–2051 (2011).
21. Wang, N., Ostuni, E., Whitesides, G. M. & Ingber, D. E. Micropatterning
tractional forces in living cells. _Cell Motil. Cytoskeleton_ **52**, 97–106 (2002).
22. Fu, J. et al. Mechanical regulation of cell function with geometrically
modulated elastomeric substrates. _Nat. Methods_ **7**, 733–736 (2010).
23. Kim, H. R., Appel, S., Vetterkind, S., Gangopadhyay, S. S. & Morgan, K. G.
Smooth muscle signalling pathways in health and disease. _J. Cell. Mol. Med._
**12**, 2165–2180 (2008).
24. Limouze, J., Straight, A. F., Mitchison, T. & Sellers, J. R.Specificity of
blebbistatin, an inhibitor of myosin II. _J. Muscle Res. Cell Motil._ **25**,
337–341 (2004).
25. Straight, A. F. et al. Dissecting temporal and spatial control of cytokinesis
with a myosin II inhibitor. _Science_ **299**, 1743–1747 (2003).
26. An, S. S. et al. An inflammation-independent contraction mechanophenotype
of airway smooth muscle in asthma. _J. Allergy Clin. Immunol._ **138**,
294–297.e4 (2016).
27. Herington, J. L. et al. High-throughput screening of myometrial calciummobilization to identify modulators of uterine contractility. _PLoS ONE_ **10**,
e0143243 (2015).



28. Wertek, F. & Xu, C. Digital response in T cells: to be or not to be. _Cell Res._
**24**, 265–266 (2014).
29. McNally, A. K., Jones, J. A., Macewan, S. R., Colton, E. & Anderson, J. M.
Vitronectin is a critical protein adhesion substrate for IL-4-induced foreign
body giant cell formation. _J. Biomed. Mater. Res. A_ **86**, 535–543 (2008).
30. Labernadie, A., Thibault, C., Vieu, C., Maridonneau-Parini, I. &
Charrière, G. M. Dynamics of podosome stiffness revealed by atomic force
microscopy. _Proc. Natl Acad. Sci. USA_ **107**, 21016–21021 (2010).
31. Gordon, S. & Taylor, P. R. Monocyte and macrophage heterogeneity. _Nat. Rev._
_Immunol._ **5**, 953–964 (2005).
32. Soon, C. F., Tee, K. S., Youseffi, M. & Denyer, M. C. T. Tracking traction force
changes of single cells on the liquid crystal surface. _Biosensors (Basel)_ **5**,
13–24 (2015).
33. Tsang, P. H., Li, G., Brun, Y. V., Freund, L. B. & Tang, J. X. Adhesion of single
bacterial cells in the micronewton range. _Proc. Natl Acad. Sci. USA_ **103**,
5764–5768 (2006).
34. Hind, L. E., Dembo, M. & Hammer, D. A. Macrophage motility is driven by
frontal-towing with a force magnitude dependent on substrate stiffness.
_Integr. Biol. (Camb.)_ **7**, 447–453 (2015).
35. Goh, Y. S. et al. Human IgG isotypes and activating Fcγ​ receptors in the
interaction of _Salmonella enterica_ serovar Typhimurium with phagocytic cells.
_Immunology_ **133**, 74–83 (2011).
36. Kaplan, G. Differences in the mode of phagocytosis with Fc and C3 receptors
in macrophages. _Scand. J. Immunol._ **6**, 797–807 (1977).
37. Hackam, D. J., Rotstein, O. D. & Grinstein, S.Phagosomal acidification
mechanisms and functional significance. _Adv. Cell. Mol. Biol. Membr._
_Organelles_ **5**, 299–319 (1999).
38. Schlam, D. et al. Phosphoinositide 3-kinase enables phagocytosis of large
particles by terminating actin assembly through Rac/Cdc42 GTPaseactivating proteins. _Nat. Commun._ **6**, 8623 (2015).
39. Beemiller, P. et al. A Cdc42 activation cycle coordinated by PI 3-kinase
during Fc receptor-mediated phagocytosis. _Mol. Biol. Cell_ **21**,
470–480 (2010).
40. Papakonstanti, E. A. et al. Distinct roles of class IA PI3K isoforms in primary
and immortalised macrophages. _J. Cell Sci._ **121**, 4124–4133 (2008).
41. Castellano, F., Montcourrier, P. & Chavrier, P. Membrane recruitment of Rac1
triggers phagocytosis. _J. Cell Sci._ **113**, 2955–2961 (2000).
42. Massol, P., Montcourrier, P., Guillemot, J.-C. & Chavrier, P. Fc receptorâ€
mediated phagocytosis requires CDC42 and Rac1. _EMBO J._ **17**,
6219–6229 (1998).
43. Ganesan, L. P. et al. The serine/threonine kinase Akt promotes Fcγ
receptor-mediated phagocytosis in murine macrophages through the
activation of p70S6 kinase. _J. Biol. Chem._ **279**, 54416–54425 (2004).
44. Papakonstanti, E. A., Ridley, A. J. & Vanhaesebroeck, B. The p110δ
isoform of PI 3-kinase negatively controls RhoA and PTEN. _EMBO J._ **26**,
3050–3061 (2007).
45. Swinney, D. C. Phenotypic vs. target-based drug discovery for first-in-class
medicines. _Clin. Pharmacol. Ther._ **93**, 299–301 (2013).
46. Tseng, P., Pushkarsky, I. & Carlo, D. D. Metallization and biopatterning
on ultra-flexible substrates via dextran sacrificial layers. _PLoS ONE_ **9**,
e106091 (2014).
47. Panettieri, R. A., Murray, R. K., DePalo, L. R., Yadvish, P. A. & Kotlikoff, M. I.
A human airway smooth muscle cell line that retains physiological
responsiveness. _Am. J. Physiol._ **256**, C329–C335 (1989).
48. Koziol-White, C. J. et al. Inhibition of PI3K promotes dilation of human
small airways in a rho kinase-dependent manner. _Br. J. Pharmacol._ **173**,
2726–2738 (2016).
49. Yoo, E. J. et al. Gα​12 facilitates carbachol-induced shortening in human airway
smooth muscle by modulating phosphoinositide 3-kinase-mediated activation
in a RhoA-dependent manner. _Br. J. Pharmacol._ **174**, 4383–4395 (2017).
50. Morrison, S. L., Johnson, M. J., Herzenberg, L. A. & Oi, V. T. Chimeric
human antibody molecules: mouse antigen-binding domains with human
constant region domains. _Proc. Natl Acad. Sci. USA_ **81**, 6851–6855 (1984).
51. Zhuang, P. et al. Characterization of the denaturation and renaturation of
human plasma vitronectin II. Investigation into the mechanism of formation
of multimers. _J. Biol. Chem._ **271**, 14333–14343 (1996).
52. Vanlandingham, M. R., Chang, N.-K., Drzal, P. L., White, C. C. & Chang, S.-H.
Viscoelastic characterization of polymers using instrumented indentation.
I. Quasi-static testing. _J. Polym. Sci. B Polym. Phys._ **43**, 1794–1811 (2005).
53. Tandon, N. et al. Electrical stimulation systems for cardiac tissue engineering.
_Nat. Protoc._ **4**, 155–173 (2009).
54. Beussman, K. M. et al. Micropost arrays for measuring stem cell-derived
cardiomyocyte contractility. _Methods_ **94**, 43–50 (2016).
55. Cheng, Q., Sun, Z., Meininger, G. & Almasri, M. PDMS elastic micropost
arrays for studying vascular smooth muscle cells. _Sens. Actuators B Chem._
**188**, 1055–1063 (2013).
56. Munevar, S., Wang, Y. & Dembo, M. Traction force microscopy of
migrating normal and H-ras transformed 3T3 fibroblasts. _Biophys. J._ **80**,
1744–1757 (2001).



**136** **Nature Biomedical Engineering** [| VOL 2 | FEBRUARY 2018 | 124–137 | www.nature.com/natbiomedeng](http://www.nature.com/natbiomedeng)


© 2018 Macmillan Publishers Limited, part of Springer Nature. All rights reserved.


#### NATure BIomedIcAl EngIneerIng Articles



57. Wu, H. et al. Epigenetic regulation of phosphodiesterases 2A and 3A
underlies compromised β​-adrenergic signaling in an iPSC model of dilated
cardiomyopathy. _Cell Stem Cell_ **17**, 89–100 (2015).
58. Del Álamo, J. C. et al. Three-dimensional quantification of cellular traction
forces and mechanosensing of thin substrata by Fourier traction force
microscopy. _PLoS ONE_ **8**, e69850 (2013).
59. Plotnikov, S. V., Pasapera, A. M., Sabass, B. & Waterman, C. M. Force
fluctuations within focal adhesions mediate ECM-rigidity sensing to guide
directed cell migration. _Cell_ **151**, 1513–1527 (2012).
60. Goedecke, N., Bollhalder, M., Bernet, R., Silvan, U. & Snedeker, J.Easy
and accurate mechano-profiling on micropost arrays. _J. Vis. Exp._ **2015**,
e53350 (2015).
61. ToliÄ‡-Nørrelykke, I. M. & Wang, N. Traction in smooth muscle cells varies
with cell spreading. _J. Biomech._ **38**, 1405–1412 (2005).
62. Liu, K. et al. Improved-throughput traction microscopy based on fluorescence
micropattern for manual microscopy. _PLoS ONE_ **8**, e70122 (2013).
63. Colin-York, H. et al. Super-resolved traction force microscopy (STFM). _Nano_
_Lett._ **16**, 2633–2638 (2016).
64. Murrell, M., Oakes, P. W., Lenz, M. & Gardel, M. L. Forcing cells into shape:
the mechanics of actomyosin contractility. _Nat. Rev. Mol. Cell Biol._ **16**,
486–498 (2015).
65. Basu, R. et al. Cytotoxic T cells use mechanical force to potentiate target cell
killing. _Cell_ **165**, 100–110 (2016).


**Acknowledgements**
The work was supported by the National Institutes of Health Director’s New Innovator
Award 1DP2OD007113, the David and Lucile Packard Fellowship and the National
Institutes of Health/National Institute of Biomedical Imaging and Bioengineering R21
Award 1R21EB024081-01. The authors thank C. Walthers for providing the primary
mouse intestinal SMCs used in the Supplementary Videos, Y. Wang and J. Z. Lee for
providing the neonatal rat ventricular myocytes, and O. Adeyiga for performing bloods
draws over the course of six months to facilitate primary macrophage culture. All
microfabrication steps were completed using equipment provided by the Integrated



Systems Nanofabrication Cleanroom at the California NanoSystems Institute at the
University of California, Los Angeles.


**Author contributions**

P.T., D.D.C. and I.P. conceived the methods. I.P., R.D., P.O.S., S.L.M., R.A.P., C.J.K.-W.
and D.D.C. designed the experiments. I.P. performed all the experiments, developed the
multi-well embodiment, optimized the protocols and wrote the image analysis software.
D.B. assisted with the substrate preparation and macrophage differentiation procedures.
L.W. assisted with the substrate preparation. R.K.T. maintained the chimeric antibody
stocks. S.L.M. supplied all the chimeric antibodies. J.L. constructed the finite element
method model. R.D. supplied the high-throughput screening (HTS) equipment for
dose-response experiments and provided extensive guidance and technical advice on
HTS procedures and developing the multi-well plate embodiment. B.F. assisted with
the HTS equipment and drug administration. W.F.J. maintained the donor HASM
cells. P.O.S. performed the macrophage and dendritic cells differentiation and advised
the experimental procedures. I.P., R.D., P.O.S., S.L.M., R.A.P., C.J.K.-W. and D.D.C.
interpreted the results. I.P. and D.D.C. wrote the manuscript. R.D., P.O.S., S.L.M., R.A.P.
and C.J.K.-W. helped revise the manuscript.


**Competing interests**
I.P., P.T. and D.D.C. are named inventors on a patent application by the University of
California, Los Angeles that covers the technology described in this study. I.P., R.D. and
D.D.C. have a financial interest in Forcyte Biotechnologies, which aims to commercialize
FLECS technology.


**Additional information**

**Supplementary information** [is available for this paper at https://doi.org/10.1038/](https://doi.org/10.1038/s41551-018-0193-2)

[s41551-018-0193-2.](https://doi.org/10.1038/s41551-018-0193-2)


**Reprints and permissions information** [is available at www.nature.com/reprints.](http://www.nature.com/reprints)


**Correspondence and requests for materials** should be addressed to D.D.


**Publisher's note:** Springer Nature remains neutral with regard to jurisdictional claims in
published maps and institutional affiliations.



**Nature Biomedical Engineering** [| VOL 2 | FEBRUARY 2018 | 124–137 | www.nature.com/natbiomedeng](http://www.nature.com/natbiomedeng) **137**


© 2018 Macmillan Publishers Limited, part of Springer Nature. All rights reserved.


Corresponding author(s): Dino Di Carlo


Initial submission Revised version Final submission
### Life Sciences Reporting Summary


Nature Research wishes to improve the reproducibility of the work that we publish. This form is intended for publication with all accepted life
science papers and provides structure for consistency and transparency in reporting. Every life science submission will use this form; some list
items might not apply to an individual manuscript, but all fields must be completed for clarity.


For further information on the points included in this form, see Reporting Life Sciences Research. For further information on Nature Research
policies, including our data availability policy, see Authors & Referees and the Editorial Policy Checklist.

##### � Experimental design


1.  Sample size


Describe how sample size was determined. In most experiments, a standard substrate size was used, and the cell count was
chosen on the basis of the number of micropatterns on those substrates.


2.  Data exclusions


Describe any data exclusions. In Fig. 3, cells not exhibiting any positive contractile response after 16 minutes
following agonist treatment were not assessed in their responsiveness to the
bronchodilator.


3.  Replication


Describe whether the experimental findings were We were able to repeatably observe the same differences between the 12 patientreliably reproduced. derived cell lines (see Supplementary Fig. 5).


4.  Randomization


Describe how samples/organisms/participants were Cells were allocated by donor where appropriate, or by tissue of origin.
allocated into experimental groups.


5.  Blinding


Describe whether the investigators were blinded to No blinding was used.
group allocation during data collection and/or analysis.


Note: all studies involving animals and/or human research participants must disclose whether blinding and randomization were used.


6.  Statistical parameters


For all figures and tables that use statistical methods, confirm that the following items are present in relevant figure legends (or in the
Methods section if additional space is needed).


n/a Confirmed


The exact sample size ( _n_ ) for each experimental group/condition, given as a discrete number and unit of measurement (animals, litters, cultures, etc.)


A description of how samples were collected, noting whether measurements were taken from distinct samples or whether the same
sample was measured repeatedly


A statement indicating how many times each experiment was replicated


The statistical test(s) used and whether they are one- or two-sided (note: only common tests should be described solely by name; more
complex techniques should be described in the Methods section)


A description of any assumptions or corrections, such as an adjustment for multiple comparisons


The test results (e.g. _P_ values) given as exact values whenever possible and with confidence intervals noted


A clear description of statistics including central tendency (e.g. median, mean) and variation (e.g. standard deviation, interquartile range)


Clearly defined error bars


_See the web collection on statistics for biologists for further resources and guidance._


|/a|Co|
|---|---|
|||
|||
|||
|||
|||
|||
|||
|||
|||
|||
|||
|||
|||
|||
|||
|||



1


##### � Software

Policy information about availability of computer code

7. Software


Describe the software used to analyze the data in this Custom-written MATLAB software (available as Supplementary Information) was
study. used to analyze the images.


For manuscripts utilizing custom algorithms or software that are central to the paper but not yet described in the published literature, software must be made
available to editors and reviewers upon request. We strongly encourage code deposition in a community repository (e.g. GitHub). _Nature Methods_ guidance for
providing algorithms and software for publication provides further information on this topic.

##### � Materials and reagents


Policy information about availability of materials

8.  Materials availability



Indicate whether there are restrictions on availability of
unique materials or if these materials are only available
for distribution by a for-profit company.



The materials are distributed by a for-profit company (Forcyte Biotechnologies).
There will be no restrictions or qualifications placed on researchers seeking to
obtain these materials.



9.  Antibodies


Describe the antibodies used and how they were validated Only humanized anti-dansyl IgG molecules were used for promoting macrophage
for use in the system under study (i.e. assay and species). phagocytosis.


10. Eukaryotic cell lines


a. State the source of each eukaryotic cell line used. HASM cells were provided by the Panettieri Lab, which specialies in isolating SMCs
from human airways.
MSCs were purchased from StemPro.
Macrophages were differentiated directly from monocytes taken from donor
blood.

Other SMCs were purchased from PromoCell.


b. Describe the method of cell line authentication used. Certificates of authentication were provided by appropriate vendors.

Markers used to identify HASM cells (obtained from the Panettieri Lab) are
described in the Methods Section.


c. Report whether the cell lines were tested for All cells were routinely tested for mycoplasma via PCR
mycoplasma contamination.



d. If any of the cell lines used are listed in the database
of commonly misidentified cell lines maintained by
ICLAC, provide a scientific rationale for their use.



No commonly misidentified cell lines were used.


##### � Animals and human research participants

Policy information about studies involving animals; when reporting animal research, follow the ARRIVE guidelines


11. Description of research animals


Provide details on animals and/or animal-derived No animals were used.
materials used in the study.


Policy information about studies involving human research participants


12. Description of human research participants


Describe the covariate-relevant population The study did not involve human research participants.
characteristics of the human research participants.



2


