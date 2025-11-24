# **-­** **Defining T cell receptor repertoires using nanovial based binding** **and functional screening**


### **Introduction**

Doyeon Koo [a,1], Zhiyuan Mao [b,1], Robert Dimatteo [c], Miyako Noguchi [d], Natalie Tsubamoto [a], Jami McLaughlin [d], Wendy Tran [d], Sohyung Lee [c], Donghui Cheng [e], Joseph de Rutte [a,f], Giselle Burton Sojo [d], Owen N. Witte [[b,d,e,g,h,i,2]](mailto:), and Dino Di Carlo [[a,f,h,j,k,2]](mailto:)


Contributed by Owen N. Witte; received November 20, 2023; accepted February 27, 2024; reviewed by Polly M. Fordyce and Ellen V. Rothenberg


**The ability to selectively bind to antigenic peptides and secrete effector molecules can**
**complex (pMHC) monomers to isolate antigen** -­ **reactive T cells. T cells are captured**
**and activated by pMHCs inducing the secretion of effector molecules including IFN** -­γ
**and granzyme B that are accumulated on nanovials, allowing sorting based on both**
**binding and function. The TCRs of sorted cells on nanovials are sequenced, recovering**
**paired** αβ-­ **chains using microfluidic emulsion** -­ **based single** -­ **cell sequencing. By labeling**
**specific targets and rank each TCR based on the corresponding cell’s secretion level.**
**Using the technique, we identified an expanded repertoire of functional TCRs tar-**
In the future, engineered cell therapies will be a pillar of medicine along with molecular and genetic interventions. There have been encouraging successes in the use of engineered T cell-­based therapies, including T cell receptor (TCR) immunotherapy in treating cancer.
These approaches use endogenous signaling activity in T cells and rely on the recognition of cancer-­associated antigens that are presented as peptides associated with major histo­ compatibility complex (MHC) on the surface of tumor cells (1). Engineered TCRs have demonstrated efficacy in treating multiple types of tumors including melanoma, sarcoma, and leukemia (2, 3).
One technical hurdle for developing effective TCR immunotherapy is to identify reac­ tive TCRs that can recognize targets with sufficient affinity and potency. T cells have one of the most diverse sequence repertoires (10 [8] to 10 [20] ) to respond to a wide variety of pathogens (4, 5). Current tools for enriching and screening cognate T cell populations rely mostly on TCR affinity or function, as defined by surface or intracellular markers of lymphocyte activation. Peptide-­MHC (pMHC) multimer (e.g., tetramer) staining is the conventional method to specifically label T cells with cognate TCRs benefiting from the avidity effect when four pMHC monomers are linked through a tetrameric streptavidin backbone (6). However, pMHC multimer staining does not take into account the func­ tional stages of the T cells, and binding of multimers to T cells is not always correlated with activation or cytotoxicity (6).
An alternative way to isolate reactive T cells is through both extracellular and intracel­ lular activation markers (7–9). The stimulation of T cells based on activation biomarkers can be achieved without the knowledge of specific epitopes and the readouts of these markers are based largely on functional activation of the T cell (7, 8). Despite improvement in these activation-­based selection techniques and better choices of markers, some of the T cells isolated by surface markers have been reported to be “bystander T cells,” meaning that they were not able to respond to antigens in a reconstructed experiment (8). Techniques based on intracellular markers, on the other hand, require cell fixation and permeabiliza­ tion leading to less RNA recovery at lower quality and may still recover TCRs that are noncytolytic, as noncytotoxic cells can secrete interferons (IFNs) and tumor necrosis factors (TNFs) (10, 11). For example, our previous attempts to recover TCRs targeting

cancer-­ enhanced splicing variants identified 8 functional TCRs from 389 candidate TCR sequences in total recovered by either surface (CD137) or intracellular (IFNγ and TNFα) markers (12). Secreted granzyme B is thought to be a specific marker for epitope-­induced
cytotoxic cells, but traditional methods like FACS and ELISPOT are not compatible with


**Significance**


T cells possess a vast diversity of surface receptors that bind to antigens presented on target cells, resulting in the

activation of functions such as

secretion of cytokines or cytotoxic molecules. T cell receptor (TCR) immunotherapies leverage this system to target tumor cells for elimination, yet
methods of identifying rare TCRs
remain nonspecific, resulting in many nonfunctional TCRs. We apply microcavity -­ containing hydrogel microparticles, known as nanovials, to selectively bind to and activate target T cells and capture secreted cytokines. This method enabled the linkage of TCR binding and functional secretion of cytokines directly with TCR sequences at the single -­ cell level, leading to expanded repertoires of TCRs and reduced false positives, ultimately enhancing the prospects of T cell cancer immunotherapy.


Reviewers: P.M.F., Stanford University; and E.V.R., California Institute of Technology


Competing interest statement: J.d.R. is an employee of Partillion Bioscience which is commercializing nanovial technology. J.d.R., D.D.C. and the University of California have financial interests in Partillion Bioscience.
O.N.W. currently has consulting, equity, and/or board relationships with Trethera Corporation, Kronos Biosciences, Sofie Biosciences, Breakthrough Properties, Vida Ventures, Nammi Therapeutics, Two River, Iconovir, Appia BioSciences, Neogene Therapeutics, 76Bio, and Allogene Therapeutics. Some of authors are inventors on patent application owned by the University of California.


Copyright © 2024 the Author(s). Published by PNAS.


1D.K. and Z.M. contributed equally to this work.


Published March 27, 2024.


**Fig. 1.** Overview of high -­ throughput analysis and isolation of antigen -­ specific T cells followed by recovery of a single -­ cell TCR library. ( _A_ ) Optional pre -­ expansion of PBMCs with target peptides for 7 d. ( _B_ ) Functionalization of nanovials with secretion capture antibodies, pMHC monomers, and oligonucleotide barcodes via streptavidin -­ biotin chemistry. ( _C_ ) Loading of cognate T cells into the cavities of nanovials in a well plate and removal of unbound cells using a cell strainer. ( _D_ ) Activation of T cells for 3 h and secretion capture in the cavity of nanovials. ( _E_ ) Labeling of captured cytokines and cell surface markers with fluorescent detection antibodies, followed by oligonucleotide barcoded antibodies against secreted markers. ( _F_ ) Sorting of cells on nanovials based on viability, CD3/CD8 expression, and secretion signal. ( _G_ ) Compartmentalization of sorted population into droplets with a cell barcode bead in the 10X Chromium system for the construction of matched V(D)J and feature barcode libraries (nanovial -­ epitope and secretion barcodes). ( _H_ ) Annotation of TCR clonotypes with corresponding secretion levels and epitopes by matching feature barcodes. (Scale bars represent 50 μ m.)


sorting of live single cells (13, 14). An ideal technology would combine antigen-­specific enrichment and secretion-­based screen­ ing to achieve both highly specific identification of functional TCR sequences along with the knowledge of their cognate target epitopes.
We recently reported an approach to confine cells in small nanoliter-­volume cavities within hydrogel microparticles, which we call “nanovials,” and capture secreted molecules on the nanovial surfaces (15, 16). Here, we adapted the nanovial technology to achieve combined antigen-­specific capture and functional activation-­based high-­throughput analysis and sorting of live


single T cells based on secreted cytokines (Fig. 1). Each nanovial acts as both an artificial antigen-­presenting cell that presents pMHC molecules at high valency within the cavity to capture with high avidity and activate cells with cognate TCRs, and as a capture site for secreted molecules, allowing accurate measurement of secreted effector molecules, such as granzyme B.
To recover TCR sequences in an epitope-­specific manner, live cells on nanovials are sorted based on CD3 and CD8 expression and secretion (i.e., IFN-­γ, granzyme B), followed by single-­cell sequencing to construct a single-­cell TCR library with matching αβ-­chains. Corresponding antigen-­specific information and


cules on the nanovial and an antibody targeting the secretion detection antibody (Fig. 1 _B_ and _E_ ). Using this platform, we were able to find an expanded number of viral-­epitope-­specific cognate TCRs compared to tetramers and recover rare prostate

cancer-­ specific functional TCRs that emerged as promising can­ didates when linking single-­cell secretion to each TCR sequence.
### **Results**


**Capture of Antigen** **-­** **reactive T Cells with pMHC** **-­** **labeled Nanovials.**
We hypothesized that nanovials coated with pMHC and cytokine capture antibodies could be used for antigen-­specific capture, TCR-­specific activation, and detection of secreting cytokines.
Transitioning from using anti-­CD45, pMHC-­functionalized nanovials were applied for the selection of antigen-­reactive T cells.
We first analyzed the specificity of nanovials in selectively binding antigen-­specific T cells using human peripheral blood mononuclear cells (PBMCs) transduced with 1G4 TCR targeting NY-­ESO-­1, a clinically studied cancer-­specific antigen (3, 17). Truncated nerve growth factor receptor (NGFR) was used as the cotransduction marker for the presence of 1G4 TCR. PBMCs transduced with and expressing 1G4 bound specifically to nanovials labeled with pMHC monomer containing HLA-­A*02:01 restricted NY-­ESO-­1 C9V peptide (SLLMWITQV) (20 µg/mL) (Fig. 2 _A_ ). Live cells

~ occupied 17% of nanovials, and 93.9% had NGFR expression. To further clarify whether the interaction was specific, we increased the NY-­ESO-­1 pMHC concentration used to functionalize nanovials.


**T Cells with Low** **-­** **affinity TCRs Are Isolated Effectively by pMHC** **-­**
**coated Nanovials.** -­ Since the 1G4 TCR has high affinity to NY ESO-­1 pMHC, we questioned whether increased avidity of pMHCs coating the nanovial cavity would prove advantageous in recovering TCRs with various affinities. Human PBMCs were transduced with five previously identified TCRs (3A1, 1G4, 4A2, 5G6, 9D2) targeting the same HLA-­A*02:01 restricted NY-­ESO-­1


**Fig. 2.** Detection of antigen -­ specific T cells on HLA -­ A*02:01 restricted NY -­ ESO -­ 1 pMHC labeled nanovials. ( _A_ ) PBMCs transduced with 1G4 TCRs are captured onto NY -­ ESO -­ 1 pMHC labeled nanovials with ~ 94% of bound cells staining positive for anti -­ NGFR. (Scale bar represents 50 μ m.) ( _B_ ) The fraction of nanovials containing live cells plotted as a function of pMHC concentration for 1G4 -­ transduced (black dots) or untransduced PBMCs (magenta dots). ( _C_ ) Flow cytometry plots of IFN -­γ secretion induced by nanovials at 3 h for 1G4 -­ transduced PBMCs loaded onto anti -­ CD45 labeled nanovials (red dots) or NY -­ ESO -­ 1 pMHC labeled nanovials (cyan dots). Secreting cells on pMHC -­ labeled nanovials sorted from the gated area are shown. (Scale bar represents 50 μ m.) ( _D_ ) The purity of recovered cognate T cells with various affinities to HLA -­ A*02:01 restricted NY -­ ESO -­ 1 pMHC are shown. Measurements are based on binding to nanovials (black circles), nanovials with IFN -­γ secretion (grey squares), or labeling with dual -­ color tetramers (red diamonds) as a function of TCR.


**Recovery of Functional Viral** **-­** **epitope** **-­** **specific TCRs using**
**Nanovials.** Following successful isolation of rare antigen-­specific T cells with TCRs of varying affinities in model systems we hypothesized that sorting based on a combination of binding and cytokine secretion using nanovials would increase the functional hit rate of a diverse repertoire of TCRs specific to common viral epitopes. Healthy donor PBMCs preactivated with a pool of previously reported HLA-­A*02:01 restricted peptides from cytomegalovirus (CMV) and Epstein Barr virus (EBV) targeting CMV pp65 (CMV1, NLVPMVATV), CMV IE-­1 (CMV2, VLEETSVML), and EBV BMLF1 (EBV, GLCTLVAML) were
isolated using three different methods: secretion based sorting
using nanovials, sorting using a CMV pp65-­specific tetramer, or activation-­based sorting using CD137 as the surface marker


sorted based on gating for above background levels of the CD137
TCRs were recovered from sorted cells using the 10X Genomics Chromium platform (Fig. 3 _B_ ). Notably, the cells on nanovials were introduced directly into the system to maintain the connec­ tion between a nanovial with a feature barcode oligonucleotide tag and the attached T cell. Nanovials did not interfere with the gene sequence recovery resulting in the highest fraction of cells with a productive V–J spanning pair (90.9%) compared to tetramer (87.8%) and CD137 samples (88%) (Fig. 3 _B_ ). We com­ piled a list of high-­frequency TCR clonotypes (frequency ≥ 5)
detected by the three methods. Since a few clonotypes contained
multiple alpha or beta chains, we recombined them into separate TCR sequences with each permutation of alpha and beta chains.
In total, we retrieved 32 unique TCR pairs with frequency ≥5: 6
TCRs overlapped among the three methods, 28 overlapped
between the nanovial and CD137 approaches, and one unique TCR was detected with nanovials (Fig. 3 _C_ ). A larger number of unique TCR sequences were detected with a less stringent cutoff


gesting additional rarer TCRs were also found.


Unlike workflows using CD137, which require laborious deconvolution to uncover the target epitopes from a peptide pool that match specific TCR sequences, pMHC-­barcoded and multiplexed nanovials reveal epitope information during cognate T cell isolation.
Using the 10X Chromium system, TCR sequence information of each cell was linked to the nanovial pMHC feature barcode, resulting in the recovery of each TCR with matching target epitope information.
To understand the antigen-­specific reactivity of 32 unique TCR sequences from 26 clonotypes (one clonotype may contain mul­
tiple alpha and beta chains) retrieved by the three methods (nano­
vial, tetramer, CD137) with a frequency ≥5, candidates were re-­expressed via electroporation into Jurkat-­NFAT-­GFP cells, in which GFP expression can be induced upon TCR recognition.
Murine constant regions were used for both TCR alpha and beta chains to prevent mispairing with endogenous TCRs. Engineered Jurkat cells were then cocultured with K562 cells expressing HLA-­A*02:01 (K562-­A2) as antigen-­presenting cells along with exogenously added peptides. Activation of the Jurkat cells was determined by flow cytometry, gating on % of the CD8 [+] /murin­
eTCRβ [+] population with GFP signal above background. K562
To investigate how functional IFN-­γ secretion-­based selection on nanovials correlated to secretory function elicited by the recovered TCR sequences in T cells, 19 reactive TCRs identified in the Jurkat-­NFAT-­GFP assay were transduced into human PBMCs and IFN-­γ secretion was measured following exposure to antigen-­presenting cells (APCs) with exogenously added cog­ nate peptides. We found that T cells transduced with all 19 reactive TCRs tested were able to specifically produce secreted IFN-­γ (>5,000 pg/mL) when stimulated by APCs presenting exogenous peptides (Fig. 3 _E_ ). Levels of secreted IFN-­γ in PBMCs were not directly correlated to GFP activation signals when tested in Jurkat-­NFAT-­GFP (R [2] = 0.10). Nanovial and CD137 approaches were both able to recover TCRs with a range of different potencies, but only nanovials provided matched epitope information.


of PBMCs was used to enrich reactive T cells (Fig. 3 _F_ ), requiring an additional 7 d of culture, we asked whether nanovials could directly enrich and activate T cells from freshly thawed PBMCs.
We loaded PBMCs directly onto nanovials or performed tetramer staining, both using pMHC CMV1 (CMV pp65, NLVPMVATV). Then, 10 [7] PBMCs were used in each method without pre-­expansion, which reduces a week-­long experiment to a single day (Fig. 3 _F_ ). Antigen-­specific T cells that bound to CMV1 on nanovials and secreted IFN-­γ or bound to CMV1
on tetramers were gated and recovered by the two methods
(Fig. 3 _G_ and _H_ ). pMHC-­labeled nanovials were able to recover ~13,000 CD3 [+] CD8 [+] cells with a clear fraction of bound cells (398) secreting IFN-­γ (Fig. 3 _I_ ). For the same sample of PBMCs, using duo-­color tetramers yielded 163 CD3+CD8+ cells (Fig. 3 _I_ ).


**Detection of Antigen** **-­** **specific T Cells based on Granzyme B**
**Secretion using Nanovials.** IFN-­γ signaling is primarily associated with activated T cells and cell-­mediated immune responses (18). As more direct evidence for cytotoxicity of antigen-­specific T cells, we further expanded the nanovial assay for the isolation of T cells based on granzyme B secretion, which remains challenging by currently available techniques (11, 13, 14). A previously identified TCR (TCR156) targeting a defined epitope (PAP22) of prostatic acid phosphatase (PAP), a prostate tissue antigen, was used to validate

-­ -­ this approach (19). This low affinity TCR shows antigen specific recognition but weak tetramer signals in reconstruction experiments (19). In the context of HLA-­A*02:01, TCR156-­transduced PBMCs were loaded onto anti-­CD45-­labeled or PAP22 pMHC-­labeled nanovials, and granzyme B secretion was analyzed after 3 h of activation. Strong granzyme B secretion was only observed from the cells that bound to pMHC-­labeled nanovials, showing antigen-­ specific activation (Fig. 4 _A_ ). By sorting the top 10% of granzyme B secreting cells, we confirmed viability and intense secretion signal on the nanovial cavity by fluorescence microscopy (Fig. 4 _A_ ).


**Finding Rare Functional TCRs Targeting Prostate Cancer**
**Epitopes.** We then wanted to challenge our nanovial platform for the recovery of rare functional TCRs targeting PAP and cancer-­ enhanced splicing peptides from human donor PBMCs. Previous studies indicate the frequency of finding cognate TCRs against those epitopes is extremely low (12, 19). In this experiment, we expanded the number of nanovial types to 10 different HLA-­A*02:01 restricted pMHC-­labeled barcoded sets: PAP14 (ILLWQPIPV), PAP21 (LLLARAASLSL), PAP22 (TLMSAMTNL), PAP23 (LLFFWLDRSVLA), CTNND1 (MQDEGQESL), CLASP1 (SLDGTTTKA), MEAF6 (SGMFDYDFEYV), PXDN (HLFDSV­ FRFL), SCAMP3 (STMYYLWML), and TCF12 (SLHSLKNRV), all of which have been previously used for TCR finding (12, 19).
In order to increase the confidence in re-­expressing potential rare TCRs with low frequency of recovery, we also introduced a unique capability into the nanovial assay where we link cell secretion of granzyme B to the TCR sequence information by adding an oligo-­nucleotide barcoded antibody that reports out the level of granzyme B secretion. In this case, an oligo-­anti-­APC antibody targeting anti-­granzyme B-­APC was added. We aimed to be able to rank TCR sequences by the amount of granzyme B associated with T cells expressing that TCR. Starting with 20 million donor PBMCs from one healthy donor, live+CD3+CD8+ cells that bound to nanovials and had granzyme B signal above the gate (granzyme B+, 698 cells) were sorted (Fig. 4 _B_ ). A subset


of live+CD3+CD8+ cells on nanovials below the granzyme B secretion threshold (granzyme B−, 4764 cells) were also sorted as a negative control (Fig. 4 _B_ ). Using the 10X Genomics platform, we constructed libraries for V(D)J sequences, the 1st feature barcode encoding the specific pMHC molecule (of 10 types) on nanovial, the 2nd feature barcode encoding granzyme B secretion level, and gene expression. In total, we sequenced and recovered 87 cells with a productive V–J spanning pair from the Granzyme B+ population and 570 cells from the Granzyme B− population (Fig. 4 _C_ ).
Using the oligo-­barcoded detection antibodies targeting the gran­ zyme B signal, we were able to identify the secretion level for each cell (Fig. 4 _D_ ). As expected, the average secretion barcode level of the Granzyme B+ population (Mean = 1,022, SD = 1,286) was significantly higher ( _P_ < 0.0001) than the Granzyme B-­ population (Mean = 288, SD = 149), representing that the oligo-­barcoding process accurately reflects the fluorescence gates (Fig. 4 _D_ ). Notably, the three most differentially expressed up-­regulated genes among the Granzyme B+ population as compared to the Granzyme


B− population were IFN-­γ, granzyme H, and granzyme B, which supports the idea that granzyme B and IFN-­γ act as crucial effectors for inducing cytotoxic activity (Fig. 4 _E_ ) (20–22).
Based on the distribution of granzyme B secretion barcode levels, we categorized each T cell subset into three different classes:
Granzyme B [High] (barcode level ≥ 2,000), Granzyme B [Medium] (2,000

- barcode level ≥ 500), Granzyme B [Low] (barcode level < 500) (Fig. 4 _D_ ). Among the 68 TCR candidates that belong to the Granzyme B+ class, 40 fell under Granzyme B [Medium] (58.8%), 9 under Graznyme B [High] (13.3%) and 19 under Granzyme B [Low] (27.9%) (Fig. 4 _F_ ).


**Functional Validation of TCRs Recovered based on Secretion**
**Barcode Levels.** We hypothesized that T cells with the highest levels of granzyme B would yield the most potent TCRs with the highest reactivity. We ranked and selected the top six clonotypes from the Granzyme B+ population expressing granzyme B secretion barcode levels above 2,000 with productive TCR alpha and beta chains


From PBMCs of one healthy donor, we found two functional TCRs from the Granzyme B [High] and one from Granzyme B [Medium] TCRs that secreted IFN-­γ upon exposure to APCs (Fig. 4 _G_ ). For those 3 functional TCRs, nanovials also provided accurate epitope infor­ mation (Fig. 4 _H_ ). The recovery rate of functional TCRs from Granzyme B [High] was highest (33%) as compared to Granzyme B [Medium] (6.7%) and Granzyme B [Low] (0%) TCRs, suggesting that functional (secretion) information captured by nanovials improves the detection rate of rare and potent TCRs (Fig. 4 _I_ ).


About 24% of CD8+ cells were polyfunctional, secreting both IFN-­γ and TNF-­α simultaneously. On the other hand, CD4+ cells had a larger polyfunctional population (47.5%) and this pattern was consistent when we analyzed for IFN-­γ and IL-­2 secretion (Fig. 5 _D_ ).
The multiplexed secretion profiling capability of nanovials could further improve the true identification rate of novel TCRs based on unique secretion phenotypes, as well as provide links to gene expres­ sion responsible for such polyfunctionality of each secreting cell.


Nanovials provide a tool to sort live antigen-­specific T cells based on a combination of TCR binding and functional response (cytokine or granzyme B secretion) followed by recovery of reactive TCRs and epitope-­specific annotation. This approach brings a number of advantages over conventional single-­cell cognate T cell isolation platforms. First, nanovials can present pMHC at high density, providing an initial high avidity enrichment step from a


-­ 24). This broader range does not come with the trade off of low purity. High-­purity screening is supported by the 78% functional hit rate of CMV and EBV-­specific TCR clonotypes following

re-­ expression where each target epitope was accurately identified.
Other large-­scaled pooled barcoded multimer approaches demon­ strated a functional hit rate of ~50% or only assessed functionality of a few TCRs recovered instead of the entire set with 80% accu­ racy for calling matching epitopes (25, 26). Another study showed the ability to link TCR sequences with specific pMHC molecules using barcoded tetramers using single-­cell sequencing in a multi­ well plate format, although no data were presented on the fraction of the recovered TCR sequences that were reactive when re-­ expressed (27).
Using oligo-­barcoded antibodies to label secreted cytokines allowed encoding of this cellular function into the single-­cell sequencing dataset and ranking of TCR sequences based on the amount of cytokine(s) secreted. The ability to link TCR sequence information directly to secretion levels of cytokines also appears to improve the yield of functional TCRs following re-­expression.
We identified three functional TCRs that are prostate cancer spe­ cific, from a pool of 25 that were re-­expressed. None of the highest frequency clonotypes (>3 of a clonotype) were functional upon re-­expression. Notably, TCRs associated with the highest gran­ zyme B secretion barcode signals (2 of 6, 33%) had the highest validation rate. As a comparison, in our previous study, we re-­expressed 389 TCRs from more than 14 distinct healthy donors to retrieve 8 functional TCRs (2.05%) (12). Although the sample
size is low, our results suggest secretion-­based screening can dra­
matically improve the recovery rate for rare functional TCRs.
The accessibility and compatibility of nanovials with standard FACS and single-­cell sequencing instrumentation can accelerate the development of personalized TCR immunotherapies. Epitopes for each recovered TCR are annotated through barcoding, while still being able to recover TCRs over a range of reactivity. Although we demonstrated only 10 different nanovial types, the number of pMHCs that can be multiplexed with nanovials is extensible to >40 based on commercial oligonucleotide-­barcoding reagents, or ~1,000 using specialized manufacturing approaches (28). Since the TCR-­pMHC interaction is heavily dependent on HLA-­subtype restriction, the ability of nanovials to provide TCRs along with matching HLA-­restricted epitopes leverages current technology

-­ limitations to simultaneously profile a large library of antigen specific T cells, especially in disease models identified with diverse HLA genotypes like type 1 diabetes or COVID-­19 (26, 29, 30).


**Fig. 5.** Multiplexed secretion -­ based profiling of prostate tissue antigen -­ specific T cells. ( _A_ ) FACS analysis and sorting gates for identifying functional antigen -­ specific T cells transduced with TCR128 loaded on HLA -­ A*02:01 restricted PAP21 pMHC labeled nanovials. IFN -­γ and TNF -­α secretion signals were analyzed from the CD3+/CD8+/NGFR+ cells. Images of T cells on nanovials that were sorted reflecting each of the four quadrant gates including an IFN -­γ and TNF -­α polyfunctional population (Q2). (Scale bars represent 50 μ m.) ( _B_ ) The population distribution based on secretion phenotype is shown as a pie chart for TCR 128, 218, and 156 transduced cells. CD3+CD8+ cells with secretion signal below the background threshold were considered as nonsecretors. ( _C_ ) Overview of multiplexed profiling of untransduced human primary T cells based on cytokine secretion and cell phenotype. T cells loaded on nanovials labeled with two cytokine capture antibodies (anti -­ IFN -­γ and anti -­ TNF -­α, or anti -­ IFN -­γ and anti -­ IL -­ 2) and anti -­ CD45 were activated under PMA/ionomycin stimulation. Secreted cytokines and cell surface markers (CD4, CD8) were stained with fluorescent detection antibodies, followed by analysis and sorting with a cell sorter. ( _D_ ) The distribution of secretion phenotype for CD4+ and CD8+ human primary T cells based on IFN -­γ and TNF -­α secretion.


By screening for TCRs based on the ability of cells to secrete a panel of cytokines, we can further explore links between TCR struc­ ture and cellular function and discover therapeutically important TCRs that, for example, are used by different cell subsets, such as regulatory T cells to prevent autoimmune conditions. The nanovial platform allows linking function, TCR sequence, and transcriptome at the single-­cell level with high clarity, which can also further


elucidate the role of TCRs across cytolytic and noncytolytic T cells.
It is noteworthy that the MHC-­nanovials employed in this study are, in theory, capable of providing only signal 1 in T cell activation (via pMHC-­TCR interaction). Given the high-­avidity effects provided by the ligand-­coated nanovials, our current research is focused on incorporating costimulatory domains into the nanovials. This approach aims to develop an artificial antigen-­presenting platform


­ terization of TCRs, such as through assaying Ca [2+] flux upon mechan ical engagement of TCRs with pMHC-­coated hydrogel beads, a platform that could be synergistic with nanovials to more fully func­ tionally screen TCRs (31). We have shown that oligonucleotide-­ barcoded antibodies can be used as labels in the nanovial assay format

[see also secretion-­encoded single cell (SEC)-­seq workflows] (32).
These types of multiomic studies can ultimately uncover relationships between TCR structure and function for improved efficacy in T cell therapies. Beyond TCRs, the nanovial assay format should be appli­ cable to other screening processes, e.g., for CAR-­T cells, CAR-­NK cells, TCR-­mimics, or bispecific T cell engagers (BiTEs), with minor adjustments, opening up a new frontier in functional screening for cell therapy development.
### **Materials and Methods**


**Nanovial Fabrication.** Polyethylene glycol biotinylated nanovials with 35 μm diameters were fabricated using a three-­inlet flow-­focusing microfluidic droplet generator, sterilized and stored at 4 °C in Washing Buffer consisting of Dulbecco’s Phosphate Buffered Saline (Thermo Fisher) with 0.05% Pluronic F-­127 (Sigma), 1% 1X antibiotic-­antimycotic (Thermo Fisher), and 0.5% bovine serum albumin (Sigma) as previously reported (33).


**Nanovial Functionalization.**

_**Streptavidin conjugation to the biotinylated cavity of nanovials.**_ Sterile nanovials were diluted in Washing Buffer five times the volume of the nanovials (i.e., 100 µL of nanovial volume was resuspended in 400 µL of Washing Buffer). A diluted nanovial suspension was incubated with equal volume of 200 μg/mL of streptavidin (Thermo Fisher) for 30 min at room temperature on a tube rotator.
Excess streptavidin was washed out three times by pelleting nanovials at 2,000 × g for 30 s on a Galaxy MiniStar centrifuge (VWR), removing supernatant and adding 1 mL of fresh Washing Buffer. _**Anti**_ **-­** _**CD45 and cytokine capture antibody labeled nanovials.**_ Streptavidin-­coated nanovials were reconstituted at a five times dilution in Washing Buffer containing 140 nM (20 μg/mL) of each biotinylated antibody or cocktail of antibodies: anti-­CD45 (Biolegend, 368534) and anti-­IFN-­γ (R&D Systems, BAF285), anti-­TNF-­α (R&D Systems, BAF210), anti-­IL-­2 (BD Sciences, 555040). Nanovials were incubated with antibodies for 30 min at room temperature on a rotator and washed three times as described above. Nanovials were resuspended at a five times dilution in Washing Buffer or culture medium prior to each experiment.

_**pMHC labeled nanovials.**_ MHC monomers with peptides of interest were synthesized and prepared according to a published protocol (34). Streptavidin-­coated nanovials were reconstituted at a five times dilution in Washing Buffer containing 20 μg/mL biotinylated pMHC and 140 nM of anti-­IFN-­γ antibody or 140 nM of anti-­granzyme B antibody (R&D systems, BAF2906) unless stated otherwise. For oligonucleotide barcoded nanovials, 1 µL of 0.5 mg/mL totalseq-­C streptavidin (Biolegend, 405271, 405273, 405275) per 6 µL nanovial volume was additionally added during the streptavidin conjugation step.


**Cell Culture.**

_**Human primary T cells.**_ Human primary T cells were cultured as previously reported (33). _**Human donor PBMCs.**_ To prime naive T cells with peptides of interest, PBMCs from commercial vendors (AllCells) were cultured and processed as previously described with chemically synthesized peptides (>80% purity, Elim Biopharm) (19).

_**K562 and Jurkat**_ **-­** _**NFAT**_ **-­** _**ZsGreen.**_ K562 (ATCC) and Jurkat-­NFAT-­ZsGreen (gift from D. Baltimore at Caltech) were cultured in RPMI 1640 (Thermo Fisher) with 10% FBS (Omega Scientific) and Glutamine (Fisher Scientific). 293T (ATCC) was cultured in DMEM (Thermo Fisher) with 10% FBS and Glutamine.


**Isolation of Viral Epitope** **-­** **specific T Cells using Nanovials, Tetramers, and**
**CD137 Staining.** Nanovials were functionalized with HLA-­A*02:01 restricted pMHCs targeting cytomegalovirus pp65, cytomegalovirus IE1 or Eptsein-­Barr virus BMLF1 with corresponding totalseq-­C streptavidin barcodes C0971, C0972, C0973


nanovials). PBMCs were activated for 7 d with peptides associated with each antigen (CMV1: pp65/NLVPMVATV, CMV2: IE1/VLEETSVML, EBV: BMLF1/GLCTLVAML) as reported previously (19). Five million activated PBMCs were loaded onto the pooled nanovial suspension. Following recovery and activation on nanovials for 3 h, samples were stained with viability dye and a cocktail of detection antibodies (calcein AM, anti-­CD3 APC Cy7, anti-­CD8 PE, anti-­IFN-­γ). Using a cell sorter, viable CD3 and CD8 cells on nanovials with IFN-­γ secretion signal were sorted. In parallel, five million activated PBMCs were each stained with a surface activation marker (CD137) or CMV1 pMHC tetramers and sorted as previously reported (9). All sorted samples were reconstituted in 18 µL of 1× PBS containing 0.04% BSA.


**Direct Enrichment of Antigen** **-­** **specific T Cells without Preactivation**
In parallel, 10 [7] of the same PBMCs were stained with anti-­CD3 PerCp Cy5.5, anti-­CD8 PE, and CMV pp65 tetramer as previously reported (9). Samples were analyzed using a cell sorter by gating to CD3+CD8+ cells on nanovials with IFN-­γ signal or to CD3+CD8+ cells with tetramer signal.


**Nanovial** **-­** **based Isolation of Prostate Cancer Epitope** **-­** **specific T Cells from**
**One Donor.** Nanovials were functionalized with anti-­granzyme B antibody and HLA-­A*02:01 restricted pMHCs each targeting 10 different prostate acid phosphatase (PAP) and cancer-­enhanced splicing epitopes discovered in previous study (19). Oligonucleotide streptavidin barcode was also added to encode each pMHC molecule on nanovials. PBMCs from one healthy donor were preactivated for 7 days with peptides associated with each antigen: PAP14 (ILLWQPIPV), PAP21 (LLLARAASLSL), PAP22 (TLMSAMTNL), PAP23 (LLFFWLDRSVLA), CTNND1 (MQDEGQESL), CLASP1 (SLDGTTTKA), MEAF6 (SGMFDYDFEYV), PXDN (HLFDSVFRFL), SCAMP3 (STMYYLWML), and TCF12 (SLHSLKNRV). Twenty million activated PBMCs were loaded onto the pooled nanovial suspension. Following recovery and activation on nanovials for 3 h, samples were stained with viability dye and a cocktail of detection antibodies (calcein AM, anti-­CD3 APC Cy7, anti-­CD8 PE, anti-­granzyme B APC). After washing, samples were also incubated with oligonucleotide anti-­APC antibody. Using a cell sorter, viable CD3+CD8+ cells on nanovials with granzyme B signal were sorted (35).


**Functional Validation of Recovered TCR Sequences.** To measure antigen-­ specific reactivity of recovered CMV-­,EBV-­, or cancer epitope-­specific TCR sequences, TCRs were expressed and screened in Jurkat-­NFAT-­GFP cells as described previously (36). Jurkat-­NFAT-­GFP cells containing multiple NFAT-­ binding motifs followed by GFP genes were used as the reporter cell line. Paired TCRs with murine constant regions were introduced into Jurkat-­NFAT-­GFP cells via electroporation. Upon TCR-­MHC recognition, NFAT will drive the transcription of GFP and can then be quantified and analyzed by FACS. Murine TCR constant regions were also analyzed by FACS to ensure TCR surface presentation.
Paired TCR alpha and beta chains of interest were cloned into a retroviral pMSGV construct as previously described (17). PBMCs for retroviral transduction were processed and cultured according to our recent publication (19, 36). Briefly, healthy donor PBMCs were activated by CD3/CD28 dynabeads followed by retroviral infection with TCRs of interest. Truncated NGFR was used as a cotransduction marker. Constant regions of TCR alpha and beta chains were replaced with mouse counterparts to minimize mispairing in human T cells. Total T cell population (both CD8 [+] and CD4 [+] ) was analyzed 7 days postinfection by FACS to ensure high-­quality infection (50 to 70% NGFR [+] ). Similar to the Jurkat-­NFAT-­GFP assay, murine TCR constant regions were also tested to ensure correct membrane allocation in human PBMCs. No significant transduction and membrane allocation differences were found among the candidate TCRs tested in this study.
To assess the function of the transduced TCRs in human PBMCs, TCR-­expressing cells were mixed with K562-­A2 cells at a ratio of 1:2 (Effector:Target) in the RPMI media and supplemented with 1 µg/mL of anti-­CD28/CD49d antibodies (BD Biosciences, 347690) and 1 µg/mL of cognate peptides or mixed peptide library.
For PBMCs, supernatants were collected after 48 h and analyzed by ELISA (BD


**Multiplexed Secretion–based Profiling to Identify Polyfunctional T Cells.**

_**Linking cell surface markers to secretion phenotype.**_ Streptavidin-­coated nanovials were decorated with biotinylated antibodies (140 nM of anti-­CD45, anti-­IFN-­γ and anti-­TNF-­α or anti-­CD45, anti-­IFN-­γ and 140 nM anti-­IL-­2).
Negative control nanovials were prepared by labeling nanovials only with anti-­CD45 antibody without any cytokine capture antibodies. Then, 0.5 million human primary T cells were loaded onto nanovials and recovered in T cell expansion medium containing 10 ng/mL PMA and 500 ng/mL ionomycin. Following 3 h of activation, secreted cytokines were stained with fluorescent detection antibodies (anti-­IFN-­γ BV421, anti-­TNF-­α APC, and anti-­IL-­2 APC) and cells were stained with 0.3 μM calcein AM, 5 µL of 25 μg/mL anti-­CD4 PE (Biolegend, 344606) and 5 µL of 100 μg/mL anti-­CD8 Alexa Fluor 488 (Biolegend, 344716) per 6 µL nanovial volume. Using a cell sorter, CD4 or CD8 cells on nanovials with secretion signal were evaluated by first creating quadrant gates based on the negative control sample (nanovials only labeled with anti-­CD45 antibody). Q1 was defined as nanovials with only IFN-­γ secreting cells. Q2 was nanovials with polyfunctional T cells that secreted both cytokines (IFN-­γ and TNF-­α or IL-­2). Q3 was nanovials with either TNF-­α or IL-­2 secreting cells while Q4 was nanovials with nonsecretors. Nanovials in each quadrant were sorted and imaged with a fluorescence microscope to quantify enrichment of each cell type and their associated secretion characteristics. _**Multiplexed secretion**_ **-­** _**based profiling of cancer**_ **-­** _**specific cognate T cells.**_ PBMCs were transduced with prostate acid phosphatase-­specific TCRs (TCR128, 156, 218) as previously described (19). Streptavidin-­coated nanovials were functionalized with biotinylated anti-­IFN-­γ, anti-­TNF-­α, and pMHC targeting each TCR: PAP21 for both TCR128 and TCR218, and PAP22 for TCR156. As a negative control, noncognate pMHC (PAP14 for TCR156) labeled nanovials were also prepared. PBMCs transduced with each TCR were separately loaded onto nanovials and activated for 3 h, followed by secondary staining with anti-­CD3 PerCp Cy5.5, anti-­CD8 PE, anti-­IFN-­γ ΒV421, anti-­TNF-­α APC, anti-­NGFR PE Cy7, and calcein AM. Using a cell sorter, CD3, CD8, and NGFR positive cells on nanovials with each


1. L. A. Johnson, C. H. June, Driving gene-­engineered T cell immunotherapy of cancer. _Cell Res._ 27, 38 (2017). 2. R. A. Morgan _et al._, Cancer regression in patients after transfer of genetically engineered lymphocytes. _Science_ 314, 126 (2006). 3. P. F. Robbins _et al._, Single and dual amino acid substitutions in TCR CDRs can enhance antigen-­ specific T cell functions. _J. Immunol._ 180, 6116–6131 (2008). 4. V. I. Zarnitsyna, B. D. Evavold, L. N. Schoettle, J. N. Blattman, R. Antia, Estimating the diversity, completeness, and cross-­reactivity of the T cell repertoire. _Front. Immunol._ 4, 485 (2013). 5. Q. Qi _et al._, Diversity and clonal selection in the human T-­cell repertoire. _Proc. Natl. Acad. Sci. U.S.A._ 111, 13139–13144 (2014). 6. M. M. Davis, J. D. Altman, E. W. Newell, Interrogating the repertoire: Broadening the scope of peptide–MHC multimer analysis. _Nat. Rev. Immunol._ 11, 551–558 (2011). 7. T. C. Wehler _et al._, Rapid identification and sorting of viable virus-­reactive CD4(+) and CD8(+) T cells
based on antigen-­triggered CD137 expression. _J. Immunol. Methods_ 339, 23–37 (2008).
8. M. Wölfl, J. Kuball, M. Eyrich, P. G. Schlegel, P. D. Greenberg, Use of CD137 to study the full repertoire of CD8+ T cells without the need to know epitope specificities _Cytometry A_ 73, 1043 (2008). 9. P. A. Nesterenko _et al._, Droplet-­based mRNA sequencing of fixed and permeabilized cells by CLInt-­ seq allows for antigen-­specific TCR cloning. _Proc. Natl. Acad. Sci. U.S.A._ 118, e2021190118 (2021). 10. M. K. Silfka, F. Rodriguez, J. L. Whitton, Rapid on/off cycling of cytokine production by virus-­specific CD8+ T cells _Nature_ 401, 76–79 (1999). 11. K. Shafer-­Weaver _et al._, The Granzyme B ELISPOT assay: An alternative to the 51Cr-­release assay for monitoring cell-­mediated cytotoxicity. _J. Transl. Med._ 1, 14 (2003). 12. Y. Pan _et al._, IRIS: Discovery of cancer immunotherapy targets arising from pre-­mRNA alternative splicing. _Proc. Natl. Acad. Sci. U.S.A._ 120, e2221116120 (2023). 13. I. Voskoboinik, J. C. Whisstock, J. A. Trapani, Perforin and granzymes: Function, dysfunction and human pathology. _Nat. Rev. Immunol._ 15, 388–400 (2015). 14. J. C. Briones _et al._, A microfluidic platform for single cell fluorometric granzyme B profiling. _Theranostics_ 10, 123–132 (2020). 15. J. de Rutte _et al._, Suspendable hydrogel nanovials for massively parallel single-­cell functional analysis and sorting. _ACS Nano_ 16, 7242–7257 (2022). 16. S. Lee, J. De Rutte, R. Dimatteo, D. Koo, D. Di Carlo, Scalable fabrication and use of 3D structured microparticles spatially functionalized with biomolecules. _ACS Nano_ 16, 38–49 (2021). 17. M. T. Bethune _et al._, Isolation and characterization of NY-­ESO-­1-­specific T cell receptors restricted on various MHC molecules. _Proc. Natl. Acad. Sci. U.S.A._ 115, E10702–E10711 (2018). 18. D. Jorgovanovic, M. Song, L. Wang, Y. Zhang, Roles of IFN-­γ in tumor progression and regression: A review. _Biomark Res._ 8, 49 (2020). 19. Z. Mao _et al._, Physical and in silico immunopeptidomic profiling of a cancer antigen prostatic acid phosphatase reveals targets enabling TCR isolation. _Proc. Natl. Acad. Sci. U.S.A._ 119, e2203410119 (2022).


**ACKNOWLEDGMENTS.** We would like to thank other members of Di Carlo
lab and Witte lab for helpful comments and discussion in preparation of this
manuscript. We thank UCLA Jonsson Comprehensive Cancer Center (JCCC) and Center for AIDS Research Flow Cytometry Core Facility. We thank UCLA Technology Center for Genomics & Bioinformatics for performing sequencing services. We
thank Jamie Spangler and Monika Kizerwetter for helpful discussions. NIH
(5R21CA256084-­02). National Cancer Institute, UCLA SPORE in Prostate Cancer (P50 CA092131). Parker Institute for Cancer Immunotherapy (20163828).
California NanoSystems Institute (CNSI) Noble Family Innovation Fund. CNSI Mann Family Foundation Technology Development Fund.


Author affiliations: [a] Department of Bioengineering, University of California, Los Angeles, CA 90095; [b] Department of Molecular and Medical Pharmacology, David Geffen School of Medicine, University of California, Los Angeles, CA 90095; [c] Department of Chemical and Biomolecular Engineering, University of California, Los Angeles, CA 90095; [d] Department of Microbiology, Immunology and Molecular Genetics, University of California, Los Angeles, CA 90095; [e] Eli and Edythe Broad Center of Regenerative Medicine and Stem Cell Research, University of California, Los Angeles, CA 90095; [f] Partillion Bioscience, Pasadena, CA 91107; gMolecular Biology Institute, University of California, Los Angeles, CA 90095; hJonsson Comprehensive Cancer Center, University of California, Los Angeles, CA 90095; [i] Parker Institute for Cancer Immunotherapy, David Geffen School of Medicine, University of California, Los Angeles, CA 90095; [j] Department of Mechanical and Aerospace Engineering, University of California, Los Angeles, CA 90095; and [k] California NanoSystems Institute, Los Angeles, CA 90095


Author contributions: D.K., Z.M., O.N.W., and D.D.C. designed research; D.K., Z.M., R.D., M.N., N.T., J.M., W.T., S.L., D.C., J.d.R., and G.B.S. performed research; D.K. contributed new reagents/analytic tools; D.K., Z.M., M.N., N.T., J.M., W.T., S.L., D.C., and G.B.S. analyzed data; and D.K., Z.M., O.N.W., and D.D.C. wrote the paper.


20. G. Z. Tau, S. N. Cowan, J. Weisburg, N. S. Braunstein, P. B. Rothman, Regulation of IFN-­γ signaling is essential for the cytotoxic activity of CD8+ T cells. _J. Immunol._ 167, 5574–5582 (2001). 21. N. Otani _et al._, Changes in cell-­mediated immunity (IFN-­γ and Granzyme B) following influenza vaccination. _Viruses_ 13, 1137 (2021). 22. C. Galassi, G. Manic, M. Musella, A. Sistigu, I. Vitale, Assessment of IFN-­γ and granzyme-­B
production by in “sitro” technology. _Methods Enzymol._ 631, 391–414 (2020).
mapping of the sequence-­ and force-­dependence of T cell activation. _Nat. Methods_ 19, 1295–1305