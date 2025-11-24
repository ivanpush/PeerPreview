[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 **Building an atlas of mechanobiology: high-throughput contractility screen of**

2 **2418 kinase inhibitors in five primary human cell types reveals selective divergent**

3 **responses among related cell types**


4


5 **Authors & Affiliations**


6 Anton Shpak [a], Jeremy Wan [a], Ricky Huang [a], Enrico Cortes [a], Yao Wang [a], Robert


7 Damoiseaux [a,b,c], Ivan Pushkarsky [a] 

8


9 *Corresponding author.


10 Authors 2–5 are listed in inverse order of the day of their birthday.


11


12 aForcyte Biotechnologies, Inc


13 bUniversity of California Los Angeles, Los Angeles, CA 90095, United States


14 cCalifornia NanoSystems Institute at UCLA, Los Angeles, CA 90095, United States


15


16 **Abstract**


17 Cellular mechanical forces play crucial roles in both normal physiology and disease, yet drug


18 discovery efforts targeting mechanobiology have been limited in part by assumptions about the


19 conservation of contractile pathways across cell types. Here, we present the first high-throughput


20 contractility screen of an annotated kinase inhibitor library, evaluating 2,418 compounds across


21 five primary human cell types using the FLECS (Fluorescent Elastomer Contractility Sensors)


22 platform. Quantification of contractile responses revealed selective divergent responses among


23 related cell types. Clustering analysis identified distinct mechanobiological profiles and novel


24 pathway associations that challenge the assumption that contractile pathways are too highly


25 conserved for selective targeting. This systematic approach supports wider adoption of


26 mechanical phenotypic screening as a viable strategy for discovering cell-type specific contractile


27 pathway modulators for a broad range of mechanically-driven disease indications.


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 **1. Introduction**


2 Working alongside the well-established importance of chemistry and biology in health, the physics


3 of cellular behavior—known as mechanobiology—also plays a crucial role. All cells, as well as the


4 tissues and organs they constitute, possess the intrinsic ability to generate mechanical force. This


5 capability is housed within the molecular machinery of each individual cell and is governed by a


6 wide variety of pathways, many of which remain poorly understood. At the single-cell level,


7 mechanical forces are utilized in processes such as cell division [1], anchoring, and motility [2], while


8 in more complex scenarios, these forces contribute to functions such as wound repair [3] . At the


9 tissue level, mechanical forces facilitate essential physiological processes, such as the


10 contractions seen in cardiac, smooth, and skeletal muscle systems, which impact organs such as


11 the bladder, intestine, and others. Mechanobiology is, therefore, a fundamental and ubiquitous


12 feature of biological systems throughout the body [4,5] **(Fig 1)** .


13 Dysregulation of these mechanical processes within cells can contribute, either partially or


14 entirely, to the development of various complex diseases. These conditions can be grouped into


15 several broad categories, including diseases related to connective tissue such as asthma [6–8] and


16 bladder dysfunction [9–11], fibrotic conditions such as lung and liver fibrosis [12–14], as well as


17 oncological and rarer disorders. The development of therapies to target these diseases has been


18 constrained by our limited understanding of the underlying biological mechanisms. There exist


19 some therapeutic strategies that directly modulate contractile forces to treat disease. For instance,


20 beta-2 adrenergic receptor agonists such as albuterol treat asthma by relaxing smooth muscle.


21 However, overall, we lack comprehensive insight into the full spectrum of druggable pathways


22 that regulate cellular and tissue mechanics.


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1


**Figure 1: Body map of mechanobiological disease caused in part or in whole by contractile**


**dysfunction in cells.** Three main classes of disease are represented here: connective tissue


such as asthma and spastic or underactive bladder, fibrotic disease such as lung fibrosis, and


oncology where tumor microenvironments, metastasis and tumor tension all play key pathological


roles. There is a major need to develop therapeutics that modulate the mechanobiological


function in cells to treat these classes of diseases.


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 Historically, a lack of technological means to quantitatively profile contractile cell force at sufficient


2 scale, and the long-held conservative assumption that contractile pathways are highly conserved


3 across cell types (making them challenging to target with precision and safety), has prevented a


4 deeper pursuit of mechanobiological readouts as a means for phenotypic drug discovery.


5 To address this, we conducted the first ever high-throughput cell contractility screen of an


6 annotated library of kinase inhibitors across two distinct disease categories within


7 mechanobiology and utilizing five primary human cell types representative of these conditions.


8 Our results reveal that, while some responses are conserved, there are also highly specific and


9 selective activities observed across different cell types in response to the same treatment. These


10 findings provide empirical evidence that selective pathways can indeed be exploited to safely


11 target mechanical processes in the treatment of disease.


12


13 **2. Results**


14 **2.1 FLECS technology is a general purpose platform to scalably screen contractile cell**


15 **force**


16 Previously, we introduced the FLECS Technology platform as an automated, high-throughput


17 system for assaying contractile force at the single-cell level across large populations of various


18 types of primary human cells [6,8,13,15–19] . Briefly, this platform enables precise measurement of both


19 acute and longer-term contractile responses in distinct cell types. Specifically, we have


20 demonstrated its ability to classify the acute contractile responses of smooth muscle cells as well


21 as the longer-term response of fibroblasts to TGF-β activation.


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1


**Figure 2:** _**(a)**_ Schematic representation of the FLECS technology: Single cells adhered to


adhesive micropatterns embedded within an elastomeric film exert mechanical force onto the


micropatterns resulting in their displacements. Top view demonstrates various pattern shapes,


while a magnified image illustrates a contracting cell inwardly displacing its terminals. Overlay of


fluorescent patterns and phase contrast images captures contracting cells, with time-lapsed


images showcasing the cell's contraction over the underlying micropattern. Scale bars represent


25 μm. _**(b)**_ Implementation of FLECS Technology in a 384 well-plate format. _**(c)**_ Workflow for


image analysis: Input includes aligned image sets of the micropatterns (set 1) and stained cell


nuclei (set 2). Analysis involves (i) identification and measurement of all micropatterns in image


set 1, (ii) cross-referencing the positions of each micropattern in image set 2, and (iii) determining


the presence of 0, 1, or >2 nuclei (cells). Output consists of mean center-to-terminal


displacements of micropatterns containing a single nucleus (one cell), compared to the median


measurement of non-displaced patterns with zero nuclei. The resulting differences are presented


as a horizontal histogram. MATLAB code enabling describing original versions of these


[algorithms are described in a previous work[16]. Figure adapted with permission from](https://www.slas-discovery.org/article/S2472-5552(23)00109-0/fulltext)


Pushkarsky et al. [13,15,16]


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 To explore how different human cell types and classes respond to the same pharmacological


2 treatments, we screened a library of kinase inhibitors in two types of smooth muscle cells relevant


3 to connective tissue disorders and two progenitor myofibroblast cell types involved in organ


4 fibrosis. The smooth muscle cells, derived from bladder and airway tissues, were screened for


5 their acute responses (45 minutes and 2 hours post-drug exposure) since conditions like asthma


6 and spastic bladder require rapid intervention during flare-ups. The fibroblast progenitor cells,


7 specifically lung fibroblasts and hepatic stellate cells, were screened for their responses over a


8 24-hour period in the presence of TGF-β, as this more closely models the activation of


9 myofibroblasts—a key process in the progression of fibrosis.


10


11 **2.2 Primary screen results**


12 Following protocols developed in our prior works, we conducted acute response screens in


13 primary human bladder (HBSM) and airway (HASM) smooth muscle cells (collectively, “SMC”),


14 and 24-hour screens in primary human lung fibroblasts (HLF), hepatic stellate cells (HHSteC),


15 and IPF patient derived lung fibroblasts (IPF-HLF) – collectively referred to as myofibroblast


16 progenitors (“MYO”), each while exposed to TGF-β over this 24-hour period. Our experimental


17 parameters are summarized in **Table 1.**


18 All experiments were performed on 384-well FLECS plates at two doses (356 nM and 35 nM). In


19 addition, to evaluate possible differential responses between the two categories of cell types,


20 smooth muscle cells were also screened in a 24-hour format but without exposure to TGF-β at a


21 single dose (356 nM). Collectively, over 38,000 drug-dosed wells were imaged each with >100


22 single cells, not including controls.


23 Acute SMC screens were performed by allowing seeded SMCs to adhere overnight on FLECS


24 assay plates, imaging their contracted states at baseline, administering drug compounds, and


25 reading their response at 45 minutes following drug addition. Final timepoints were taken 2 hours


26 after drug administration. In this format, DMSO-only wells served as negative controls. No


27 pharmacological positive control was administered since micropatterns lacking adhered cells


28 serve as inherent positive controls.


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


























|Cell Type|Abbrev<br>.|Tissue /<br>Origin|Screen<br>Format|TGF β?<br>-|Time<br>Points|Dose(s)|
|---|---|---|---|---|---|---|
|**Human Bladder**<br>**Smooth Muscle**<br>(“SMC”)|HBSM|Primary bladder<br>smooth muscle|**Acute**|No|Pre-drug,<br>45min & 2hr<br>Post-drug|35 nM,<br>356 nM|
||||**Extended**<br>(secondary)|No|24hr|356 nM|
|**Human Airway**<br>**Smooth Muscle**<br>(“SMC”)|HASM|Primary airway<br>smooth muscle|**Acute**|No|Pre-drug,<br>45 min & 2hr<br>post-drug|35 nM,<br>356 nM|
||||**Extended**<br>(secondary)|No|24hr|356 nM|
|**Lung**<br>**Fibroblasts**<br>(“MYO”)|HLF|Primary human<br>lung fibroblasts|**24-hour**<br>(activation)|Yes|24hr|35 nM,<br>356 nM|
|**IPF Lung**<br>**Fibroblasts**<br>(“MYO”)|IPF-HLF|Patient-derived<br>lung fibroblasts|**24-hour**<br>(activation)|Yes|24hr|35 nM,<br>356 nM|
|**Hepatic Stellate**<br>**Cells**<br>(“MYO”)|HHSteC|Liver-resident<br>stellate cells|**24-hour**<br>(activation)|Yes|24hr|35 nM,<br>356 nM|



1



**Table 1.** Summary of the five primary human cell types and their screening conditions. SMC


cells (blue rows) and MYO cells (orange rows) differ in assay format (acute vs. 24-hour), TGF-β


activation, time points, and dosing. This table highlights how each cell type was tested under


distinct protocols to capture disease-relevant contractile responses. The secondary 24hr screens


in SMC were performed at the primary single-point level for cursory comparison to MYO


responses, but these hits were not advanced into confirmation and subsequent stages.


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 All 24-hour SMC screens were conducted identically but were only imaged at 24 hours after drug


2 addition. All 24-hour TGF-β MYO screens were performed by allowing MYO cells to adhere in


3 FLECS assay plates pre-loaded with drug compounds for 4 hours. Then, TGF-β was added to the


4 cells. After 24 hours, the plates were imaged at one terminal timepoint. In this format, DMSO-only


5 wells served as negative controls while wells without TGF-β provided positive controls


6 representing non-activated myofibroblast progenitor cells.


7 **Figure 3** shows the normalized screen results across all primary screens. Normalized contraction


8 values for 24-hour screens are shown in Supplemental Information **(Fig S1)** . The tightest


9 distributions are observed in acute SMC screens (hit upper bound >8 MADs below median of


10 treated wells) while the most variation is seen in HLF at the 356 nM dose (hit upper bound 1.5


11 MADs below median). Robust Z’ factors for all TGF-β MYO screens are displayed in Supplemental


12 Information **(Fig S2)** . For MYO screens, hits were defined as compounds that achieved both Z

13 score <-3 and normalized activity inhibition of at least 15% to ensure both statistical significance


14 and biological relevance. For SMC screens, hits were defined as compounds that achieved a


15 decrease in normalized activity inhibition of at least 20% from the baseline timepoint.


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1


**Figure 3: Results from primary contraction screens across multiple cell types** . The data


demonstrates the platform's scalability and robustness, with clear separation between


controls and hits. Expectedly, most compounds did not elicit significant responses, yet a


notable subset of inhibitors was identified across cell types and doses. This underscores the


non-random distribution of responses. A “Hit upper bound” threshold is marked by the green


line, with non-hits below this threshold shaded in dark grey. These non-hits fail to meet


normalized contraction constraints (<0.85) despite achieving robust Z-score criteria. _**(a)**_


Scatter plots of acute SMC screen results. Robust Z-scores of contraction are shown,


stratified by dose and cell type. Compounds are ordered by the average Z-score of


contraction across all cell types and doses, with the same order maintained across all


subplots. _**(b)**_ Scatter plots of MYO screen results. Normalized percent change in contraction


is shown, stratified by dose, timepoint, and cell type. Compounds are ordered by the average


normalized percent change in contraction across all cell types, timepoints, and doses, with


the same order maintained across all subplots.


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 **2.3 Clustering of primary screening data identifies clear activity clusters described by**


2 **specific pathway representation.**


3 To analyze broad patterns in compound responses, we applied agglomerative hierarchical


4 clustering to the vectorized dataset **(Fig 4a)**, capturing compound activity across cell types and


5 doses at the 24 hour timepoint.


6 Agglomerative hierarchical clustering begins by treating each observation as its own cluster.


7 Then, similar pairs of clusters are iteratively merged based on a linkage criterion that represents


8 the dissimilarity between sets of observations. This criterion is computed as a function of the


9 pairwise distances between the single observations within these sets.


10 Given the low dimensionality of our data, and given that magnitude of response is of primary


11 concern, we used Euclidean distance as the pairwise distance metric. We performed the


12 clustering using Ward’s linkage, which minimizes the increase in total within-cluster variance when


13 merging two clusters. To visualize this process, we created a hierarchical dendrogram that


14 represents relationships at various levels of similarity.


15 For this analysis, we focused on the penultimate branch point, where the dendrogram resolves


16 into four clusters **(Fig 4a)** . We chose this number of clusters based on visual inspection. At the


17 four-cluster level, the clusters appear sparse and well-separated, suggesting that they represent


18 distinct and meaningful groupings. Moreover, the clusters remain large enough to yield statistically


19 significant comparisons between them.


20 By examining the four primary clusters at this level, we identified fundamental groupings of


21 compounds with similar mechanobiological effects, capturing both shared mechanisms and


22 distinct response profiles across the dataset. Based on this analysis, we designated these clusters


23 with the following labels:


24 1. _HHSteC-specific compounds_ – compounds primarily active in human hepatic stellate cells


25 (HHSteCs)


26 2. _Inhibitors_ – compounds with broad inhibition across all cell types tested


27 3. _Inactives_ – compounds that did not affect contraction in any cell type


28 4. _Inducers_ – compounds that increased contraction of cells


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


**Figure 4: Clustering of 24-hour primary screen compounds reveals distinct contractile**


**response types and pathway associations.** _**(a)**_ Dendrogram and pairwise distance matrix


showing hierarchical clustering of compounds based on Z-score vectors across five cell types.


Clusters highlight compounds with distinct response profiles, with pairwise distances >50


indicating highly divergent responses. _**(b)**_ Bar graph comparing mean robust Z-scores of


contraction (±95% CI) for each cell type within clusters, with the dotted line marking the Z = -3


upper bound for hits. _**(c)**_ Distribution of compounds by affected pathways within each cluster,


emphasizing pathway overrepresentation.


1


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 Following from this, we used the hypergeometric distribution to evaluate which pathways were


2 overrepresented within each cluster (under the null hypothesis that pathways were identically


3 distributed across clusters). We identified several expected associations as well as novel ones.


4 Specifically, the _Inhibitors_ cluster contained overrepresentations of the cell-cycle/DNA damage,


5 ROCK, and TGF-β/Smad pathways, all of which are known to affect cytoskeletal function,


6 contraction, or TGF-β activation (which was induced in all MYO cell types). This result validated


7 the FLECS platform’s ability to reflect known mechanobiological responses in cells.


8 Novel results from this analysis include the overrepresentation of PI3K/Akt/mTOR in the _HHSteC-_


9 _specific_ cluster but not in the _Inhibitors_ cluster, and the overrepresentation of MAP/ERK in the


10 _Inducers_ cluster, suggesting possible targets for disease indications where enhancement or


11 restoration of higher contractile tone would benefit patients, such as underactive bladder.


12


13 **2.4 Subcluster dissection reveals distinct mechanobiological response profiles and**


14 **pathway biases**


15 To further refine our understanding of pathway groupings within the identified primary clusters, we


16 performed a secondary clustering analysis. Each of the four main clusters— _HHSteC-specific_


17 _compounds, Inhibitors, Inactives, and Inducers_ —was further subdivided. The number of sub

18 clusters was chosen based on visual inspection of the dendrogram. This was done separately for


19 each cluster, to ensure that sub-clusters were well-separated and were not singletons or


20 otherwise too small to observe statistically significant differences. Overall, the subclusters


21 maintained the general activity themes of the parent clusters. However, at this finer level of


22 resolution, by similarly evaluating pathway overrepresentation using the hypergeometric


23 distribution, additional mechanistic themes and pathway contributions that were not apparent at


24 the primary cluster level were revealed.


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1


**Figure 5: Sub-clustering of 24-hour primary screen compounds reveals distinct**


**contractile response types and pathway associations.** _**(a)**_ Dendrogram and pairwise


distance matrix showing hierarchical clustering of compounds based on Z-score. _**(b)**_ Bar graph


comparing mean robust Z-scores of contraction (±95% CI) for each cell type within sub

clusters, with the dotted line marking the Z = -3 upper bound for hits. _**(c)**_ Distribution of


compounds by affected pathways within each sub-cluster, emphasizing pathway


overrepresentation within general cluster.


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 In particular, the _HHSteC-specific_ cluster was sub-divided into strong HHSteC inhibitors (HHS2),


2 moderated HHSteC inhibitors (HHS3), and TGF-β pathway inhibitors which only affected MYO


3 cells (HHS1 - where HLF, IPF-HLF, and HHSteC but not SMC cells were affected). Statistically


4 significant overrepresentation of TGF-β pathway in HHS1 confirms this association.


5 The _Inhibitors_ cluster broke out into strong general inhibitors (INH1), weak general inhibitors


6 (INH2), and a third grouping which appears to represent strong inhibitors in non-diseased MYO


7 cells but not in IPF-HLF nor the SMCs. Interestingly, INH1 (strong general inhibitors) are


8 associated with metabolic enzyme pathway overrepresentation while INH2 (weak general


9 inhibitors) are associated with ROCK pathway overrepresentation – a known broadly active


10 regulator of cellular contractility.


11 The _Inactives_ cluster—the largest by compound count—further resolved into three distinct groups:


12 a wholly inactive group that accounted for over 75% of the parent cluster (INA1), as expected,


13 and two smaller subclusters with unexpected low, non-zero activity one of which showed selective


14 effects in HHSteCs (INA2), and one which displayed low non-zero activity across all cell types


15 (INA3). This result suggests that on a relative basis, the modest activities of sub-clusters INA2,


16 INA3 were more numerically similar to entirely inactive compounds indicating their activities would


17 be masked without this secondary subcluster analysis.


18 Finally, the _Inducers_ parent cluster was subdivided into two subclusters representing inducer


19 activity in all cell types (IND1) and selective inducer activity only in SMCs (IND2). Pathway


20 overrepresentations within these sub-clusters suggest that the MAP/ERK pathway might regulate


21 contractility in various different cell types while Protein Tyrosine Kinase/RTKs pathway might be


22 selective towards SMCs.


23


24 **2.5 Hit selection and confirmation**


25 Next, we cherry-picked molecules that registered as hits per our original definitions (see **4.4** ).


26 Some compounds that met the hit definition were excluded due to evidence of toxicity (observed


27 through dead staining and from morphology). Other compounds were excluded due to inactivity


28 in one cell type when picked together (e.g., compounds active in HLF at the 35 nM dose but only


29 active in IPF-HLF at the 365 nM dose were picked at 35 nM and excluded from the analysis for


30 IPF-HLF). A few borderline hits were excluded due suspected inactivity in combination with plate


31 limitations (e.g., for HHSteC, there were slightly too many hits to fit on one cherry-pick drug plate).


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


**Figure 6: Screening flow-chart from primary screening to confirmation and dose response.**


Flowchart illustrating the screening process and the number of hits identified at each stage. A total


of 2,418 compounds were screened at multiple doses in both MYO and SMC cell types, with


imaging performed at biologically relevant time points. MYO cells were imaged at a single 24-hour


time point to capture their response to TGF-β, which aligns with the biological timescale of


myofibroblast activation. In contrast, SMCs were imaged pre-drug exposure, and at 45 minutes


and 2 hours post-drug exposure to capture their acute responses. Hit definitions were established


based on these time points. For comparison, SMCs were also screened at 24 hours; however, hits


from this time point were not selected for further analysis as the focus remained on acute


responses. Confirmation screens were subsequently conducted in triplicate using the same


formats as the primary screen. Confirmed hits were defined as compounds which maintained their


initial activity levels in all three of the triplicate tests.


1


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 Compounds were cherry-picked for confirmation screening only their lowest active doses. **Figure**


2 **6** summarizes our effort in taking primary screen data, identifying and retesting suspected hits,


3 and advancing certain interesting confirmed hits into dose-response testing. As part of this


4 process, certain molecules that were initially found to be more active in one cell type over another


5 were re-tested across a dose-range in multiple cell types to better understand their selective


6 activity.


7 As discussed previously, the SMCs, derived from bladder and airway tissues, were screened for


8 their acute responses at 45 minutes and 2 hours post-drug exposure, as conditions like asthma


9 and spastic bladder require rapid intervention during flare-ups. In contrast, the MYO cells—


10 specifically lung fibroblasts and hepatic stellate cells—were screened for their responses over a


11 24-hour period in the presence of TGF-β. This longer time frame was chosen to model the


12 activation of myofibroblasts, a key process in the progression of fibrosis. All subsequent


13 confirmation screen analyses were conducted using these time-point-specific activity definitions.


14 Based on the strictest criteria of having all three replicates of the confirmation screen meet our


15 definition for a hit, we observed a confirmation rate of >40% in all cell types with the exception of


16 IPF-HLF which are primary IPF patient-derived and appear much more heterogenous in


17 morphology, size, and contractile activity.


18 Data from the triplicate confirmation screen experiments demonstrated strong consistency, with


19 mean pairwise R² correlation values exceeding 0.75 and approaching 0.9 for certain cell types


20 **(Fig 7b)**, underscoring the robustness of the results. A heatmap of the number of hits (out of three


21 replicates) across cell type and compound combinations **(Fig 7c)** reinforced our primary screening


22 findings, revealing both highly cell-type-specific responses and shared effects across multiple cell


23 types induced by certain compounds.


24 To further classify these diverse activities and elucidate the underlying biological pathways driving


25 them, we performed agglomerative hierarchical clustering on the confirmation dataset and


26 evaluated the pathways associated with the compounds comprising each cluster.


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1


**Figure 7: Confirmation screen results show strong correlation and cell-specific**


**responses.** _**(a)**_ Scatter plot showing comparing robust Z-score of contraction between two


replicates in HLF confirmation screen, colored by density. _**(b)**_ Bar graphs showing correlation in


response variables by cell type. Note that the SMC graphs show only the 45-min results. _**(c)**_


Heatmap showing confirmation index by cell type for each compound. Note that some


compounds were picked at different doses in different cell types. For SMC cells, the maximum


number of hits across both timepoints is shown.


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 **2.6 Pathway analysis of confirmation data**


2 As with the earlier analysis of the 24-hour primary screen dataset, the number of clusters was


3 chosen based on visual inspection of the clustering dendrogram **(Fig 8a)** . At the four-cluster level,


4 the branches of the dendrogram appear well-separated, suggesting that these clusters represent


5 meaningful groupings.


6 Within these four clusters, we identified fundamental groupings of compounds with similar


7 mechanobiological effects, encompassing both shared mechanisms and distinct response


8 profiles across the dataset. Two clusters characterized response types similar to those observed


9 in the primary screen data – the _HHSteC-specific_ cluster (typified by a greater response in


10 HHSteC cells), and the _General_ cluster (typified by a broad inhibitory response across all cell


11 types), resemble the _HHSteC-specific_ and _Inhibitors_ primary screen clusters respectively. This


12 suggests that these groupings reflect similarities in the constituent compounds across the two


13 screens. Furthermore, cell-type-specific activities were observed in the remaining two clusters,


14 which we designated as _Long-term/MYO-specific_ and _Acute/SMC-specific_, reflecting the earlier


15 observation time points used for SMCs.


16 To elucidate the pathways underpinning these activity profiles, we again applied the


17 hypergeometric distribution to evaluate which pathways were overrepresented within each cluster


18 (under the null hypothesis that pathways were identically distributed across clusters). Several


19 expected associations were identified, along with novel ones **(Fig 8c)** . In particular, statistical


20 overrepresentation of the ROCK pathway was observed in the _General_ cluster, characterized by


21 inhibition across all cell types. Meanwhile, the _Long-term/MYO-specific_ cluster exhibited a


22 statistical overrepresentation of immunology/inflammation pathways.


23 The PI3K/Akt/mTOR and Cell Cycle/DNA Damage pathways were again statistically


24 overrepresented in the _HHSteC-specific_ cluster, consistent with the analysis performed on the


25 entire primary screen dataset. Interestingly, the Protein Tyrosine Kinase/RTK and Neuronal


26 Signaling pathways were overrepresented in the _Acute/SMC-specific_ cluster, suggesting a unique


27 influence of these pathways on SMC contractile function or acute response times.


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


**Figure 8: Clustering of confirmation screen results reveals distinct response types with**


**differences in associated pathways.** _**(a)**_ Dendrogram and pairwise distance matrix showing


hierarchical clustering of compounds based on Z-score vectors across five cell types. Selected


compound targets are highlighted. _**(b)**_ Bar graph comparing mean robust Z-scores of contraction


(±95% CI) for each cell type within clusters, with the dotted line marking the Z = -3 upper bound


for hits. _**(c)**_ Distribution of compounds by affected pathways within each cluster, emphasizing


pathway overrepresentation. Note: only 45-min data was included in activity vectors for SMC


cells.


1


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 **2.7 Comparison of HLF to HHSteC**


2 Following our comparison of activities and profiles across different clusters, we next focused on


3 analyzing potential differences in responses between related cell types, beginning with HLF and


4 HHSteC, both classified as MYO cell types.


5 To do this, we first plotted the mean robust Z-scores (using confirmation screen data) for each


6 compound tested in both cell types at the same dose against each other to directly compare their


7 responses **(Fig 9a)** . Although the distribution of pathways represented among the confirmed hits


8 was largely similar between the two cell types **(Fig 9b)**, the Z-score scatter plot suggests certain


9 compounds were active in HHSteC but not HLF. This finding aligns with the presence of similar


10 _HHSteC-specific_ clusters observed in both the primary and confirmation screens.


11 This analysis suggested the possibility of significant differential responses to the same


12 treatments between these two related cell types. To test this hypothesis, we conducted


13 concentration-response experiments on selected hits that appeared to exhibit such differences


14 **(Fig 9c)** . Using the 24-hour MYO screening protocol, we evaluated a 10-step, 3-fold dose range


15 spanning low nM to double-digit µM concentrations in both HLF and HHSteC.


16 Our findings revealed distinct responses in both potency and efficacy for certain compounds.


17 For instance, compound 9A produced highly similar responses in the two cell types, with slightly


18 better potency in HLF. In contrast, compounds 9C-9F exhibited marginally to significantly


19 greater potency in HHSteC. Moreover, compounds 9E and 9F demonstrated over 100% greater


20 percent inhibition in HHSteC compared to HLF at the response plateau level. Collectively, these


21 dose-response curves demonstrate that highly related human cell types can exhibit substantially


22 different responses to the same treatments under identical conditions.


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


**Figure 9: Comparing responses in HLF and HHSteC shows both general and selective**


**responses.** _**(a)**_ Scatter plot of average Z-scores for contraction for compounds tested in both


cell types at the same dose at the confirmation screen level. Note: not all hits were tested in


both cell types, as in this case molecules were only re-tested in the cell type where they were


originally identified as hits. _**(b)**_ Distribution of compounds by affected pathways for confirmed


hits in each cell type, highlighting pathway overrepresentation. _**(c)**_ Dose response curves for


selected compounds demonstrating cell-type selectivity among the MYO cells. Compounds


labelled with an asterisk (*) were over 10 times more potent (by IC50) in HHSteC.


1


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 **2.8 Comparison of HASM to HBSM**


2 Finally, we repeated this analysis on SMC cells (derived from bladder or airway tissue) used in


3 the screens. As before, we plotted the mean robust Z-scores (from the confirmation screen) for


4 each compound tested in both cell types at the same dose against each other to directly compare


5 their responses **(Fig 10a)** .


6 **Fig 10b** shows that the majority of confirmed hits were active in both cell types. However, some


7 hits were not uniformly confirmed across all triplicates (e.g., not all three replicates met the criteria


8 for a hit). This reflects the data presented in the Z-score scatter plot in which some hits are active


9 but narrowly miss the hit criteria on an averaged basis. This suggests potential overall weaker


10 activity in cases where only partial confirmation was achieved. Once again, the distribution of


11 pathways represented among the confirmed hits were similar between the two cell types **(Fig**


12 **10c)**,


13 From this dataset, we selected six compounds for re-testing in both cell types under the same


14 assay conditions as the original screen (i.e., 45-minute acute response to drug exposure)


15 across a 10-step, 3-fold dose range spanning low nM to double-digit µM concentrations.


16 Although the differences were less pronounced than those observed in the MYO comparison


17 **(Fig 9)**, we still identified distinct responses between the two cell types. Specifically, compounds


18 10A–10D exhibited better potency in HBSM with similar efficacy in both cell types. Conversely,


19 compound 10F, and to a lesser extent 10E, demonstrated greater percent inhibition in HASM


20 compared to HBSM.


21 Importantly, all experiments were conducted simultaneously on the same plates, ruling out


22 batch effects or inter-experimental variability as potential causes for these differences.


23 Collectively, these findings further demonstrate that highly related cell types, such as primary


24 human bladder smooth muscle cells (HBSM) and primary human airway smooth muscle cells


25 (HASM), can exhibit distinct responses to the same compound treatments.


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


**Figure 10: Comparing responses in HASM and HBSM shows both general and selective**


**responses.** _**(a)**_ Scatter plot of average Z-score of contraction for compounds tested in both cell


types at the same dose at the confirmation screen level. _**(b)**_ Venn diagram showing overlap in


confirmed hits. _**(c)**_ Distribution of compounds by affected pathways for confirmed hits in each cell


type, emphasizing pathway overrepresentation. _**(d)**_ Dose response curves for selected


compounds.


1


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 **3. Discussion**


2 The purpose of this study was twofold.


3 First, to demonstrate that contractility and mechanical cell function, though governed by the


4 same family of contractile proteins, can exhibit distinct regulatory mechanisms across cell types.


5 Our findings, derived from the first-ever high-throughput kinase inhibitor screen targeting cell


6 contraction, provide compelling evidence that mechanobiological pathways are diverse and


7 selectively targetable. This suggests that direct screening for contraction modulators could


8 unveil novel, first-in-class therapeutics with potential for high therapeutic indices, even among


9 related cell or tissue types.


10 Second, this work highlights the unprecedented capability and scalability of the FLECS platform.


11 For the first time, we were able to scalably quantify the effects of >2,400 annotated kinase


12 inhibitors across five cell-types at multiple doses, as well as perform confirmation and dose

13 response studies. This was accomplished all using the same assay and readout, in under 8


14 weeks of run time, including plate manufacturing (in house) and data analysis. This dataset


15 comprises over 38,000 unique drug-loaded wells each with 100s of single-cell datapoints in a


16 single study. This scale and quantitative resolution enables a network level of insight into


17 mechanobiology laying the groundwork for building a mechanobiology atlas, a resource with the


18 potential to transform how we approach drug discovery and deepen our understanding of


19 cellular mechanics.


20 Our systematic analysis of kinase inhibitors revealed that cellular contractility can be selectively


21 modulated by small molecules, with even related cell types exhibiting divergent responses to the


22 same compounds. While many compounds showed similar effects across cell types, we


23 identified specific cases where responses clearly diverged. This divergence was particularly


24 well-demonstrated in MYO cells, where the distinct response patterns were confirmed in dose

25 response experiments. SMCs also exhibited divergent responses, though less consistently


26 when examined in targeted dose-response studies compared to the initial screens. Collectively,


27 these results underscore the complexity of mechanobiological pathways and demonstrate that


28 contractility regulation can differ even among related cell types, suggesting the possibility of


29 selectively regulating contractile phenotypes with good therapeutic indices.


30 Our clustering analyses of the dataset revealed both expected and novel mechanobiological


31 signatures. We identified known pathway associations like ROCK [20,21] and TGF-β, validating our


32 approach, while also discovering unexpected pathway overrepresentations such as MAP/ERK


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 in SMCs and PI3K/Akt/mTOR in HHSteCs, suggesting new therapeutic opportunities like


2 enhancing contractility in underactive bladder through MAP/ERK modulation. Interestingly,


3 despite using TGF-β for myofibroblast activation, the MYO-specific cluster did not show


4 statistical overrepresentation of the TGF-β/SMAD pathway, likely because these compounds


5 generated activity profiles that clustered with other mechanobiological response patterns rather


6 than forming a distinct signature. This distribution of responses across multiple clusters


7 suggests that mechanical responses to kinase inhibitors may not cleanly segregate by canonical


8 pathway annotations. Moreover, these clustering patterns reveal the complex evolutionary


9 landscape of contractile regulation, suggesting that while core contractile machinery is


10 conserved, its regulation has diversified to meet tissue-specific functional demands.


11 The robustness of our findings is supported by high confirmation rates exceeding 40% across


12 triplicates in most cell types, though we noted some important technical considerations. Lower


13 confirmation rates in patient-derived IPF-HLF cells reflect the inherent variability of such


14 samples, highlighting the importance of multiple cell models in translational research.


15 Additionally, compound storage conditions may have affected the reproducibility of weakly


16 active compounds, though this limitation did not impact our major hits, which showed consistent


17 activity across experiments. Future studies will benefit from standardized compound preparation


18 protocols across all screening stages.


19 The creation of this first mechanobiological response atlas represents a significant advance in


20 our understanding of cellular mechanics. By systematically mapping how diverse cell types


21 respond to pharmaceutical perturbations, we establish a framework for predicting tissue-specific


22 drug effects on mechanical properties. This approach could revolutionize drug development by


23 enabling early identification of both desired tissue-specific effects and potential mechanical side


24 effects. The atlas concept could be further expanded by incorporating additional cell types, drug


25 classes beyond kinase inhibitors, and complementary readouts such as transcriptional profiles.


26 Such a comprehensive resource would provide unprecedented insight into the relationship


27 between chemical structure, pathway activation, and mechanical outcomes across tissues.


28 In conclusion, this work advances our understanding of mechanobiology, demonstrating that


29 contractility pathways are not universally conserved and that selective targeting is feasible. Our


30 findings suggest new strategies for drug development, where mechanical phenotypes could be


31 modulated with tissue specificity despite shared molecular machinery. It also showcases the


32 transformative potential of the FLECS platform to uncover novel therapeutic targets and create


33 a comprehensive mechanobiology atlas. These findings lay the groundwork for future studies


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 and provide a strong foundation for translating these insights into meaningful therapeutic


2 advances.


3


4 **4. Methods**


5 **4.1 Cell culture**


6 Cryopreserved human primary lung fibroblasts (HLF), human primary hepatic stellate cells


7 (HHSteC), human airway smooth muscle (HASM) cells, and human bladder smooth muscle


8 (HBSM) cells were obtained from ScienCell. IPF-HLF were a gift from Prof. Brigette Gomperts


9 (UCLA). HLF and IPF-HLF were cultured in Lung Fibroblast Growth Medium (Cell Applications,


10 catalog #516–500),). HHSteC were cultured in Stellate Cell Medium (SteCM, Cat. #5301).


11 HASM and HBSM cells were maintained in Ham's F-12 medium supplemented with 10% fetal


12 bovine serum (FBS) and 1% penicillin/streptomycin. All cell types were grown in T75 flasks


13 under standard conditions (37 °C, 5% CO₂) until ready for experiments. Cells were detached


14 using 0.05% Trypsin-EDTA and prepared for experiments at passage 3. For experiments, HLF,


15 HHSteC and IPF-HLF were tested in Dulbecco's Modified Eagle Medium (DMEM) containing


16 10% FBS and 1% penicillin-streptomycin, while HASM and HBSM cells were tested in their


17 respective Ham's F-12 growth medium.


18


19 **4.2 FLECS contractility assay protocol**


20 The FLECS contractility assay followed protocols previously published [16] . Plates pre-coated with


21 70 µm “X”-shaped collagen type IV micropatterns on an 8 kPa substrate (Forcyte


22 Biotechnologies, product #384-HC4R-QC10) were used throughout the study. Wells were


23 initially filled with 25 µL of either serum-free DMEM (MYO cells) or Ham’s F12 media (SMC)


24 supplemented with 1% penicillin-streptomycin. The appropriate cells were resuspended at


25 50,000 cells/mL in their proper culture medium. Cells were seeded in 25 µL volumes per well


26 and allowed to settle for 1.5 hours at room temperature before being transferred to a 37 °C


27 incubator. For MYO cells, compounds were added via Biomek automation 1.5 hours after


28 incubation, followed by 10 minutes of plate shaking. TGF-β1 (PeproTech, 2.5 ng/mL) was added


29 30 minutes after compound addition. Plates were then returned to the incubator. At 24 hours


30 post-TGF-β1 addition, Hoechst 33342 live nuclear stain (1 µg/mL) was added, and plates were


31 imaged after 30 minutes using a Molecular Devices ImageXpress automated microscope. For


32 SMC cells, plates were incubated for 24 hours post-seeding. Baseline images were acquired


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 before compound addition via Biomek, followed by 10 minutes of plate shaking. Wells were then


2 imaged at 45 minutes and 2 hours post-compound addition. Prior to the 2-hour imaging


3 timepoint, Hoechst 33342 live nuclear stain was added for 30 minutes to enable nuclear


4 imaging. Analysis of cell contraction and adhesion was performed using proprietary computer


5 vision algorithms developed by Forcyte [16] .


6


7 **4.3 Compound libraries**


8 The screen was conducted using the Kinase Inhibitor Library (MedChemExpress), which


9 consists of 18 unique 384-well source plates. Each source plate is laid out according to one of


10 nine unique plate maps, and each map is repeated at two different stock concentrations.


11


12 **4.4 Hit criteria**


13 For MYO cells, compounds were selected as ‘hits’ for retesting if the robust Z-score of


14 contraction was more than -3 (>3 MADs below the median of the negative controls) and the


15 normalized inhibition was at least 15%. Primary screen hits were also filtered for toxicity based


16 on morphology. For SMC cells, compounds were selected as ‘hits’ for retesting for a given


17 timepoint if the normalized percent decrease in contraction (compared to the baseline timepoint)


18 was greater than 20%. Primary screen hits were also filtered for toxicity based on dead stain


19 imaging, with a cutoff of 3 times the median dead percent of the negative controls. Compounds


20 were defined to be “confirmed hits” in a given cell type if after being chosen for retesting, they


21 met the above conditions for 3/3 replicates. In addition, all preliminary hits were also filtered for


22 toxicity based on dead stain imaging, with a cutoff of three times the median dead percent of the


23 negative controls. If any of the three replicates were beyond this cutoff, compounds were


24 excluded from the confirmed hits.


25


26 **4.5 Data analysis**


27 Hierarchical agglomerative clustering was performed using the AgglomerativeClustering()


28 function from the scikit-learn Python library. Compounds were characterized by vectors with five


29 components, with each component corresponding to the robust Z-score of contraction (for MYO


30 cells) or the robust Z-score of the normalized percent inhibition (for SMC cells) in a given cell


31 type. Clustering was done using Ward’s linkage, computed from the Euclidean distance metric.


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 The number of clusters for comparison and the corresponding distance threshold in each case


2 was chosen based on visual inspection of the clustering dendrogram. Clusters were chosen at


3 the point where branches of the dendrogram appeared most sparse and well-separated,


4 deviating where necessary to ensure that (a) there were no singletons/clusters too small to yield


5 statistically significant differences and (b) meaningful differences in response were not


6 obscured. Pathway overrepresentation was analyzed using the hypergeometric distribution.


7 This was performed using the hypergeom.cdf() function from the SciPy Python library. The p

8 value that a pathway is overrepresented was computed as the probability that a given cluster (or


9 group of confirmed hits for a given cell type) contains at least the observed number compounds


10 affecting that pathway when drawing groups of the observed size randomly without replacement


11 under the null hypothesis that pathways are evenly distributed throughout the population.


12


13 **Author Contribution**


14 I.P. conceived of the project. E.C., Y.W., R.H., J.W., and A.S. performed the experiments. A.S.,


15 E.C., J.W., Y.W., and I.P. analyzed the data. R.D. developed the automation strategy and


16 oversaw the robotic laboratory and lead compound management. A.S. developed data analysis


17 and interpretation scripts and prepared the figures. A.S., I.P., Y.W., and R.D interpreted the data.


18 I.P., A.S., and R.D. wrote the manuscript.


19


20 **Declaration of Competing Interest**


21 The authors declare the following financial interests/personal relationships which may be


22 considered as potential competing interests:


23 Ivan Pushkarsky reports a relationship with Forcyte Biotechnologies, Inc that includes: board


24 membership, employment, and equity or stocks. Robert Damoiseaux reports a relationship with


25 Forcyte Biotechnologies, Inc that includes: consulting or advisory and equity or stocks. Yao


26 Wang reports a relationship with Forcyte Biotechnologies, Inc that includes: employment and


27 equity or stocks. Enrico Cortes reports a relationship with Forcyte Biotechnologies, Inc that


28 includes: employment and equity or stocks. Ricky Huang reports a relationship with Forcyte


29 Biotechnologies, Inc that includes: employment and equity or stocks. Jeremy Wan reports a


30 relationship with Forcyte Biotechnologies, Inc that includes: employment and equity or stocks.


31 Anton Shpak reports a relationship with Forcyte Biotechnologies, Inc that includes: employment


32 and equity or stocks. Ivan Pushkarsky has patent #US11592438B2 issued to UCLA. Robert


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 Damoiseaux is an employee at UCLA which holds the patent licensed by Forcyte which pertains


2 to research presented in this work.


3


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 **Acknowledgements**


2 The authors thank the Magnify Incubator at CNSI and the Nanolab at UCLA, and the Molecular


3 Screening Shared Resource at CNSI for providing critical infrastructure to support the work. The


4 authors also thank Mason Victors for his invaluable guidance regarding robust assay


5 development and execution practices to ensure data quality and on relevant data analysis


6 approaches.


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 **References**


2 1. Lesman, A., Notbohm, J., Tirrell, D. A. & Ravichandran, G. Contractile forces regulate cell


3 division in three-dimensional environments. _J. Cell Biol._ **205**, 155–162 (2014).


4 2. Jin, J.-P., Bloch, R. J., Huang, X. & Larsson, L. Muscle Contractility and Cell Motility. _J._


5 _Biomed. Biotechnol._ **2012**, 257812 (2012).


6 3. Li, B. & Wang, J. H.-C. Fibroblasts and Myofibroblasts in Wound Healing: Force Generation


7 and Measurement. _J. Tissue Viability_ **20**, 108–120 (2011).


8 4. Dunn, A. R. Mechanobiology: ubiquitous and useful. _Mol. Biol. Cell_ **29**, 1917–1918 (2018).


9 5. Eyckmans, J., Boudou, T., Yu, X. & Chen, C. S. A Hitchhiker’s Guide to Mechanobiology.


10 _Dev. Cell_ **21**, 35–47 (2011).


11 6. Yoo, E. J. _et al._ Gα12 facilitates shortening in human airway smooth muscle by modulating


12 phosphoinositide 3-kinase-mediated activation in a RhoA-dependent manner. _Br. J._


13 _Pharmacol._ **174**, 4383–4395 (2017).


14 7. Doeing, D. C. & Solway, J. Airway smooth muscle in the pathophysiology and treatment of


15 asthma. _J. Appl. Physiol._ **114**, 834–843 (2013).


16 8. Koziol-White, C. J. _et al._ Inhibition of PI3K promotes dilation of human small airways in a rho


17 kinase-dependent manner. _Br. J. Pharmacol._ **173**, 2726–2738 (2016).


18 9. Steers, W. D. Pathophysiology of Overactive Bladder and Urge Urinary Incontinence. _Rev._


19 _Urol._ **4**, S7–S18 (2002).


20 10. Aizawa, N. & Igawa, Y. Pathophysiology of the underactive bladder. _Investig. Clin. Urol._ **58**,


21 S82–S89 (2017).


22 11. Miyazato, M., Yoshimura, N. & Chancellor, M. B. The Other Bladder Syndrome: Underactive


23 Bladder. _Rev. Urol._ **15**, 11–22 (2013).


24 12. Younesi, F. S., Miller, A. E., Barker, T. H., Rossi, F. M. V. & Hinz, B. Fibroblast and


25 myofibroblast activation in normal tissue repair and fibrosis. _Nat. Rev. Mol. Cell Biol._ **25**,


26 617–638 (2024).


27 13. Wang, Y. _et al._ FLECS technology for high-throughput screening of hypercontractile cellular


28 phenotypes in fibrosis: A function-first approach to anti-fibrotic drug discovery. _SLAS Discov._


29 _Adv. Life Sci. R D_ **29**, 100138 (2024).


[bioRxiv preprint doi: https://doi.org/10.1101/2025.01.11.632556; this version posted September 27, 2025. The copyright holder for this preprint](https://doi.org/10.1101/2025.01.11.632556)
(which was not certified by peer review) is the author/funder, who has granted bioRxiv a license to display the preprint in perpetuity. It is made
[available under aCC-BY-ND 4.0 International license.](http://creativecommons.org/licenses/by-nd/4.0/)


1 14. Wipff, P.-J., Rifkin, D. B., Meister, J.-J. & Hinz, B. Myofibroblast contraction activates latent


2 TGF-β1 from the extracellular matrix. _J. Cell Biol._ **179**, 1311–1323 (2007).


3 15. Pushkarsky, I. _et al._ Elastomeric sensor surfaces for high-throughput single-cell force


4 cytometry. _Nat. Biomed. Eng._ **2**, 124–137 (2018).


5 16. Pushkarsky, I. FLECS Technology for High-Throughput Single-Cell Force Biology and


6 Screening. _ASSAY Drug Dev. Technol._ **16**, 7–11 (2018).


7 17. Hairapetian, L. _et al._ Simplified, High-throughput Analysis of Single-cell Contractility using


8 Micropatterned Elastomers. _JoVE J. Vis. Exp._ e63211 (2022) doi:10.3791/63211.


9 18. Ezzo, M. _et al._ Acute contact with profibrotic macrophages mechanically activates fibroblasts


10 via αvβ3 integrin–mediated engagement of Piezo1. _Sci. Adv._ **10**, eadp4726 (2024).


11 19. Tseng, P., Pushkarsky, I. & Carlo, D. D. Metallization and Biopatterning on Ultra-Flexible


12 Substrates via Dextran Sacrificial Layers. _PLOS ONE_ **9**, e106091 (2014).


13 20. Kawada, N., Seki, S., Kuroki, T. & Kaneda, K. ROCK Inhibitor Y-27632 Attenuates Stellate


14 Cell Contraction and Portal Pressure Increase Induced by Endothelin-1. _Biochem. Biophys._


15 _Res. Commun._ **266**, 296–300 (1999).


16 21. Roda, V. M. de P. _et al._ Inhibition of Rho kinase (ROCK) impairs cytoskeletal contractility in


17 human Müller glial cells without effects on cell viability, migration, and extracellular matrix


18 production. _Exp. Eye Res._ **238**, 109745 (2024).


19


