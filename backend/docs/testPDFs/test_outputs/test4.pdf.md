ACS Nano. Author manuscript; available in PMC 2023 May 24.


Published in final edited form as:

ACS Nano. 2022 May 24; 16(5): 7242–7257. doi:10.1021/acsnano.1c11420.

# **Suspendable hydrogel nanovials for massively parallel single-** **cell functional analysis and sorting**


**Joseph de Rutte** [†,][⁑][,+], **Robert Dimatteo** [‡,+], **Maani M. Archang** [†], **Mark van Zee** [†], **Doyeon** **Koo** [†], **Sohyung Lee** [‡], **Allison C. Sharrow** [#], **Patrick J. Krohl** [††], **Michael Mellody** [†,#], **Sheldon** **Zhu** [⁑], **James V. Eichenbaum** [†], **Monika Kizerwetter** [‡‡], **Shreya Udani** [†], **Kyung Ha** [⊥], **Richard** **C. Willson** [°], **Andrea L. Bertozzi** [§,#,][⊥], **Jamie Spangler** [††,‡‡,¬], **Robert Damoiseaux** [#,][α][,][∥], **Dino Di** **Carlo** [*,†,§,#,][α]


Author Contributions:
J.D., R.Di, and D.D. conceptualized the overall nanovial platform and designed experiments throughout the entire work. R.Da. contributed to designing and interpreting flow cytometry experiments and single-cell RT PCR experiments and B cell secretion experiments. J.D. designed the initial fabrication workflow and performed characterization experiments. J.D., R.Di, S.Z., S.L., S.U., and D.K. contributed to production and optimization of nanovials for the experiments. J.D, R.Di., M.M.A, J.V.E. M.Z., D.K. S.U., and P.K. performed cell loading and cell binding experiments. J.D., R.Di., and S.Z. performed and analyzed nanovial emulsification experiments. J.D., R.Di., and M.V. developed the CHO cell secretion protocols and performed characterization experiments. P.J.K. and M.K. performed HEK293 transfection studies which J.S. supervised. R.Di., M.A., S.L., J.V.E, and S.Z., performed hybridoma and B cell secretion assay experiments. M.A. and J.V.E. performed mouse immunizations and harvested cells for B cell studies. M.M. and A.C.S. performed single-cell RT-PCR experiments. K.H. and A.L.B. developed the framework for calculating the volume energy curves and volume splitting curves. R.C.H. provided hybridoma lines and consultation. J.D., R.Di, and D.D. wrote the manuscript with input from all authors. J.D. prepared final figures with input from all authors. +These authors contributed equally


Competing Interests:
The Regents of the University of California have filed patents related to the work described in the manuscript that D.D., J.D., R.Di., M.M.A., R.Da, S.L. and D.K. are inventors on. J.D. and D.D. are co-founders and have a financial interest in Partillion Bioscience which is commercializing the nanovial technology. S.Z. was employed by and has financial interests in Partillion Bioscience.


**Supplemental Information.** Document includes figures S1–S12 and Table S1 that support the findings in the main text including: table of reagents and resources used for the studies; additional details on nanovial fabrication and characterization; compatibility of different nanovial sizes with different cell types, flow cytometers, and other instruments; timelapse images of nanovials settling in a well plate; theoretical analysis of monodisperse dropicle formation; cell viability characterization and growth after dropicle formation and release; recovery of cells from nanovials; overviews for high IgG producer enrichment workflows and hybridoma and B cell secretion assays; analysis of single-cell IgG secretion for transiently transfected cells on nanovials; single-cell RT-PCR gel for free hybridomas compared with hybridomas loaded on nanovials; assessment of the dynamic range of nanovials for capture and antigen-specific detection of antibodies.


#California NanoSystems Institute, University of California, Los Angeles, CA 90095, USA


have the potential to transform our understanding of cellular biology, as well as accelerate the

nanovials, and demonstrate their use for sorting single viable cells based on their secreted products

types, partition uniform aqueous compartments, and capture secreted proteins. Solutions can be

exchanged around nanovials to perform fluorescence immunoassays on secreted proteins. Using

this platform and commercial flow sorters, we demonstrate high-throughput screening of stably and transiently-transfected producer cells based on relative IgG production. Chinese Hamster

cells secreting an anti-hen egg lysozyme (HEL) antibody were recovered from background cells,

enriching a population of ~4% prevalence to >90% following sorting. Leveraging the high-speed

sorting capabilities of standard sorters, we sorted >1,000,000 events in less than an hour.

IgG secreting mouse B cells were also sorted and enriched based on antigen-specific binding.

Successful sorting of antibody-secreting B cells combined with the ability to perform single-cell

RT-PCR to recover sequence information suggests the potential to perform antibody discovery

workflows. The reported nanovials can be easily stored and distributed amongst researchers,

democratizing access to high-throughput functional cell screening.


The microwell plate is a foundational component of biological assays because of its ability

between samples. The bottom surface of each well can be functionalized to adhere cells,

promote cell growth, and perform biomolecular reactions that allow for colorimetric and

fluorescent readouts. Biological samples of interest can then be isolated by pipetting fluid

from a well. Despite its simplicity and utility, even the highest throughput, 1536-well plate

formats, hold volumes that are hundreds of thousands of times larger than individual cells,

The ability to perform functional biological assays at single-cell resolution promises to

deepen our understanding of biology and accelerate the development of biotechnology

products. Among the ~20,000 protein-coding genes in the human genome more than 15%

of the encoded proteins are predicted to be secreted, a similar percentage to that for cell membrane-bound proteins. [1] Approaches to analyze and sort cells based on these secreted

factors can shine light on this ubiquitous but significantly understudied cellular function.

In biotechnology, sorting of rare B cells or plasma cells directly based on the secretion of

antigen-specific antibodies allows for the acquisition of gene sequences that can be used to make monoclonal antibody (mAb) drugs or diagnostic affinity reagents. [2–7] Additionally,

selection of stable production-grade cells such as Chinese hamster ovary (CHO) cells based

on humanized IgG secretion rates enables development of highly productive cell lines for industrial scale monoclonal antibody manufacturing. [8]


Although technologies have emerged that enable the interrogation of single cells, there

are significant tradeoffs that either limit their functionality or inhibit widespread adoption.

Fluorescence activated cell sorting (FACS) was one of the first single-cell technologies

events per second. Screening of viable cells is typically limited to cell surface markers

(i.e. the clusters of differentiation markers, or CDs) as analysis of intracellular markers requires membrane permeabilization and fixation. [9,10] Approaches have been developed to


sequester secreted products directly onto the cell surface, but these techniques suffer from significant crosstalk between cells. [11–13] Microfluidic technologies have emerged that can

create volumes approaching the size of cells, enabling high-throughput analysis of single cells based on additional properties such as secreted molecules. [14] Devices with microscale

chambers as well as water-in-oil droplets generated using microfluidic devices have been employed to isolate cells, accumulate secreted molecules, and even sort. [15–20] Despite

the utility of these existing platforms, the ability to add reagents and wash is limited,

and microfluidically-generated droplets lack the solid surface of a microwell plate which

is critical for standard assay formats like sandwich immunoassays or ELISA. Strategies

to address these shortcomings have been developed, but each requires specialized assay

formats, and often extremely expensive equipment to perform the assays, which hinders widespread adoption. [21–24]


microwells (Figure 1). These microparticles, or “nanovials”, hold single cells in sub nanoliter volumes of fluid, 100,000 times less volume than a single well of a 1536-well

microwell plate, yet require no specialized instrumentation. Fluids are easily exchanged

by centrifugation and pipetting, and each compartment can be sealed and unsealed using

biocompatible oils to prevent cross-talk between samples. The surfaces can be modified

to bind cells or capture biomolecules for various molecular readouts. Nanovials can be

analyzed and isolated using commonly available FACS instruments enabling screening at

rates >1000 events per second. While other particle systems have been utilized to hold subnanoliter volumes, [25–29] our approach allows attachment and protection of cells in cavities

within particles, unlocking capabilities to expand the scale of analysis by integration with

within one day. After sorting, cells remain intact and viable, enabling regrowth and single cell RT-PCR. A similar experiment would require >2600 384-well plates and several weeks

of additional culture to grow up a sufficiently large clonal population of cells required to

detect secretions in the larger volumes. Nanovial-enabled workflows promise to democratize

antibody discovery and cell line development, and also empower researchers to investigate

single-cell secretions, as a key cellular function, with high precision and scale.


are engineered to directly load and protect cells. Each particle is decorated with functional

groups to attach cells and perform chemical reactions, is precisely shaped to prevent cross talk, and is designed to be compatible with commercial flow cytometers. Utilizing an

aqueous two-phase system combined with droplet microfluidics, and hydrogel chemistry

developed for tissue engineering, we fabricate these hydrogel microparticles (nanovials) at high throughputs (~1000 s [−1] ) (Figure S1–3). [30,31] By tuning the fabrication parameters, we


achieve highly monodisperse polyethylene glycol (PEG)-based nanovials with accessible

internal cavities (outer diameter CV of 1.5 – 3.2%, cavity opening diameter CV of 2.1

– 5.8%, interbatch variation <5%, depending on size Figure S1F–G). Particles are easily

modified with various cell adhesion moieties (e.g. argine-glycine-aspartate (RGD), poly-L lysine (PLL), fibronectin). Biotin covalently coupled to the nanovial matrix allows for facile

interactions can also be used to link cell capture antibodies specific to cell surface proteins

(e.g. CD45 and CD19) to selectively adhere cells to nanovials. Biotin-functionalized cells

can also be directly captured on streptavidin-coated nanovials. The morphology of the

nanovial cavity and relative size can be adjusted by tuning the concentration of components

in the particle precursor solutions (Figure S2). We are able to fabricate monodisperse

nanovials across a broad range of mean diameters (Figure S3) from 35 to 83 μm, which

are compatible with a range of cell types and common lab and FACS instruments (Figure

S2). Importantly, this nanovial fabrication step is the only part of the process that requires

use of a specialized microfluidic device, and fabrication is completely decoupled from the

biological assays themselves. All parts of the single-cell assay workflows are performed

directly with pre-fabricated nanovials and standard lab equipment (Video S1). This is

a critical feature of our platform as it enables the more complex microfluidic/particle

fabrication work to be centralized and performed in advance.


**Nanovials as modular single-cell carriers**


Loading cells into the cavities of the nanovials is achieved with simple pipetting steps

followed by incubation to allow cell binding. Nanovials can be first loaded into a standard

well plate by pipetting. Due to their morphology, nanovials settle with their cavities mostly

upright, forming a monolayer of particles, with exposed cavities, at the bottom of the well (Figure S1H, S4, Video S2). [32] Cells are then seeded over the particles and settle with a

sizeable fraction coming to rest in the particle cavities (Figure 2). Notably, this seeding

approach led to cell occupancies that closely followed Poisson statistics (Figure 2D), as is

expected for loading of single cells into microfluidically-generated droplets or for limiting dilution loading of single cells into microwells. [33,34] By controlling the cell seeding density,

we may control occupancy such that most particles have either 0 or 1 cells associated with

them.


Following seeding, cells can be bound to the nanovials through one of a variety of

cell-surface interactions, that are tailored to the cell type of interest. Adherent producer

cell lines used for the production of mAbs and other biologics can be adhered through

alone. However, increased adhesion similar to other cell lines was achieved by modifying

2C). We also showed that surface proteins of HEK293 cells can be biotinylated such that

the cells adhered and were maintained on nanovials through biotin-streptavidin interactions

Uniform droplets can be formed around nanovial particles via simple pipetting steps

with oil and surfactant to seal them and prevent cross-talk between samples (Figure

3). To accomplish this, an aqueous solution of nanovials is first concentrated in a

conical or microcentrifuge tube by centrifuging and aspirating the supernatant. A layer of

biocompatible oil with surfactant is added and the suspension is then pipetted vigorously

for 1 min to create smaller and smaller water-in-oil droplets. Eventually the droplet

size is maintained by the outer periphery of the microparticle and we find that, in agreement with minimal energy considerations (Figure S5), [35] uniform volumes of fluid

remain stably trapped within the cavity by the hydrophilic particle. Any excess fluid in

the suspension is partitioned into much smaller satellite droplets (Figure 3B). The resulting

compartmentalization process was tested successfully over a range of nanovial sizes (35–85

μm diameters). For larger particles, it was found that uniform emulsions (mean diameter

density in the pelleted sample led to numerous droplets containing multiple particles. We

found that dilution of the sample to the same total number of particles per unit volume

remedied this particle aggregation, enabling the formation of smaller uniform partitions

(mean diameter of 40 μm, CV = 3.2%, <5% aggregates, Figure 3).


Importantly, nanovials can be recovered from the oil while still retaining functional

cells. To recover nanovials a biocompatible destabilizing agent is used to coalesce the

indicating that the workflow is biocompatible (Figure S6A–B). Further, we observed similar

and B cells bound via antibodies remained attached to the nanovial cavities over the entire

emulsification process. After washing and emulsification, exceedingly few cells are adhered

to the external surface of the nanovials suggesting these cells are sheared off and that the

cavity can shelter cells from shear forces during processing.


**Single cell secretion analysis and sorting using nanovials**


Using the nanovial platform, we demonstrate a device-free workflow to perform single-cell

secretion assays with minimal crosstalk (Figure S8). Given the importance of selecting cell lines with high antibody titer for therapeutic production, [36] we chose a model system

comprised of a Chinese hamster ovary (CHO) cell line that produces human IgG targeting


interleukin-8 (IL-8) and particles modified to capture human IgG. Cells are first loaded

into the microparticle cavities and adhere via integrin binding sites as previously described.

After initial cell seeding, particles and associated cells are collected and washed to remove

background secretions. Particles are then coated with anti-human IgG Fc antibodies by

binding to biotin groups linked to the particle matrix. Following this step, the nanovials

and associated cells are rapidly compartmentalized in less than 1 minute by pipetting

with oil and surfactants. The compartmentalized CHO cells are then incubated, and the

secreted antibodies are captured onto the associated particle matrix. After incubation for

one to several hours depending on cell type, the emulsions are broken and the nanovials

containing attached cells and secretions are collected and washed. Nanovials are then

labeled with secondary fluorescent antibodies targeting the secreted anti-IL-8 antibodies.

Using fluorescence microscopy, we confirmed retention of cells and associated secretion

signal on the particle surface after recovering out of oil into an aqueous phase (Figure 1C).


Because of the high fraction of secreting cells, preventing secretion cross-talk between

cells in neighboring particles is critical to enable quantitative analysis and sorting based

on secretion differences at the single-cell level. Rapid and effective encapsulation is key

to preventing cross-talk of secretions, as demonstrated by a side-to-side comparison of the

secretion assay with and without the oil encapsulation step (Figure 4A–B). When secretions

are captured on particles without the encapsulation step, particles without associated cells

show high secretion signals indicating significant cross-talk (8.2% of empty particles have

signal above threshold) (Figure 4A). Conversely, with the oil encapsulation step there

are two visibly distinguishable populations, nanovials with and without secreting cells,

and only 1% of nanovials without cells have signal above the cutoff threshold (Figure

4B). Minimizing the fraction of false positives is particularly critical when secretions can

spill over into neighboring nanovials containing non-secreting cells that would contaminate

downstream cultures or sequencing assays.


We observe an increase in mean accumulated fluorescence signal on the particles that trends,

times that there was a sizeable population of cells (~25%) that had no measurable secretion

signal (Figure 4C). Viability analysis of this population revealed that >50% of these cells

were still alive indicating that the lack of signal is likely due to a fraction of the cell

population no longer expressing the antibody production gene or secreting the produced

antibodies.


In addition to characterizing IgG production for the stable CHO cell line, we also

demonstrated the ability to characterize the distribution of secreted product from transiently

transfected HEK293 cells (Figure S9A). HEK293 cells were transfected with plasmids

coding for two recombinant IgGs: atezolizumab and 10H2. Cells were first loaded onto

streptavidin-coated nanovials via surface biotinylation of HEK293 cells, and plasmid was

introduced. Cells and associated nanovials were then emulsified and cells were allowed

to secrete recombinant products for 32 hrs. The emulsion was subsequently broken and

nanovials were recovered for flow cytometry (Figure S9B–C). For atezolizumab and


10H2, 24.2% and 44.7% of cell-containing nanovials, respectively, showed antibody signal

above background empty nanovials (Figure S9D), demonstrating minimal crosstalk in the

system. We also observed a long tail of secretion profiles for both atezolizumab and

10H2, suggesting substantial heterogeneity in the level of gene expression and/or functional

secretion. Similarly, 38.1% and 27.6% of cell-containing nanovials for the atezolizumab and

10H2 transfected conditions, respectively, showed antibody signal above threshold defined

by the non-transfected control (Figure S9E).


To further validate the capacity of our system to identify rare subpopulations based on

secretions, a FACS enrichment experiment was performed. We performed secretion-based

sorting with a mixed population of the anti-IL-8 producing CHO cells and non-producing CHO cells each labeled with a separate Cell Tracker [™] dye (Figure 4E). After the secretion

assay and prior to sorting, fluorescence imaging of the stained 85 μm diameter particles

showed increased signal on particles containing the antibody-secreting cells of interest

compared to those containing non-secreting cells (Figure 4E). This further demonstrated the

lack of cross-talk in our system as well as the specificity of the labels to the secretions

of interest. The particles with associated cells and secretions were then sorted based on

the labeled secretion intensity (Figure 4E). Downstream analysis showed effective isolation

of the sub-population of interest with high-purity (85–99%) (Figure 4F) over a range of

target cell dilutions. In the most dilute case (1:1000) an enrichment ratio of 850-fold

was achieved indicating the capability to isolate rare target cell events at frequencies of

~0.1%. Cells isolated using this approach can be expanded directly from the particle matrix

enabling a streamlined workflow with minimization of trypsinization steps (Figure S6C–

D). Collectively, our stable and transient transfection studies illustrate the versatility of

the nanovial technology for identifying and recovering rare populations of high-yielding

producer cells using standard flow cytometry workflows.


**Enrichment and expansion of high-titer subpopulations using FACS**


We hypothesized that sorted cells would maintain the ability to produce antibodies at

levels correlating with the mean intensity of initial single-cell secreted signal. To test

this hypothesis, we performed the nanovial secretion assay on human anti-IL8 producing

CHO cells and selected out sub-populations based on level of IgG secretion signal using

FACS (Figure 5). Cells secreting antibodies were sorted in high-throughput (>200 events/s) by gating off both the fluorescently labeled secretion channel as well as CellTracker [™ ]


and (2) particles with cells and the top 20% of antibody secretion signal. Microscopy

images of the sorted nanovials and associated cells show successful isolation of secreting

cells with signal proportional to their respective FACS gating (Figure 5B). The selected

sub-populations were sorted into a 96-well plate and expanded out of the particles over the

course of ~10 days (Figure 5C). Samples were then plated at the same cell density and bulk

antibody production of the different subpopulations was measured by ELISA and compared

with non-sorted control samples. We observed a 26% increase in total IgG production for the

sorted sub-population 1 (all secreting cells) in comparison to the pre-sort control population

(Figure 5D). This increase is most likely due to the removal of cells that are no longer


secreting IgG following the sort, which was measured to be ~25% based on microscopy

analysis (Figure 4C) as well as flow analysis (Figure 5A). For sorted sub-population 2 (the

top 20% of secretors) we measured an average increase of 41% in total IgG production

(n =4) with a maximum increase among the samples of 58% (Figure 5D), indicating the

capability of the platform to select out functionally higher producing sub-populations that

maintain the phenotype for at least 10 days.


**Isolation of antigen-specific IgG secreting cells**


In a final application, we tested the feasibility of using our nanovial platform to screen

anti-hen egg lysozyme (anti-HEL) antibodies (IgG1) were used as our target cell population
and were diluted into a background of similar, CellTracker [™] Blue (CTB) labeled, 9E10

hybridoma cells producing anti-myc antibodies (IgG1).


Mixed populations of HyHel-5 and 9E10 hybridoma cells were loaded and bound to

nanovials using anti-CD45 cell capture antibodies as described previously, and all antibodies

secreted from both cell types were captured non-specifically onto the nanovial surfaces

with fluorescently conjugated HEL antigen (HEL-647), revealing the presence of only

the antigen-specific antibody secretions (Figure 6A). When assaying mixed hybridoma

one hour, while no detectable signal was present on nanovials containing 9E10 cells

(Figure 6B). Over one million nanovial events were analyzed and a gate encompassing

0.18% of the nanovial population was sorted based off of their high HEL fluorescence

area. Subsequent microscopic analysis confirmed highly enriched populations of strongly labeled HEL-647 [+] /CTB [−] cell-loaded nanovials in the post-sort population (>90% purity),

confirming that the entire analysis and sorting workflow was compatible with detecting

downstream sequence recovery and re-growth (Figure 6D). We were able to lyse individual

cells loaded on nanovials that were deposited into wells and amplify antibody sequence

materials do not interfere with the RT-PCR chemistry. We were also able to sort single

hybridoma clones loaded on nanovials into individual wells, culture them and expand them

into clonal sub-populations (Figure 6D).


The antigen binding assay was extended to a second antigen and to primary B cells from

immunized mice. We first confirmed that ovalbumin (OVA)-immunized mice produced


IgG that was OVA-specific by incubating nanovials in serum from either immunized or

serum dilution, whereas no detectable signal was generated from control serum at any

concentration (Figure 6E, Figure S12). We then loaded and sorted OVA-specific antibody secreting B cells isolated from the spleens of immunized mice (Figure 6E). A subset of

the analyzed and sorted cell-containing nanovials was associated with strong OVA-specific

signal on the nanovials themselves, indicating capture of secreted antibodies (Figure 6E).

There was little to no surface stain on the captured cells (Figure 6E), suggesting we isolated

plasma B cells which canonically lack high levels of B cell receptor (BCR) on the cell

surface. Another subset of the B cells acquired strong surface fluorescence after exposure

to fluorescent antigen, but did not secrete detectable levels onto the nanovial surface,

suggesting direct binding to BCRs, or non-specific binding to membrane compromised

cells. A third population of cells had both cell surface BCR staining and staining on the

nanovial surfaces, indicative of secreted antibodies. The top ~2% of nanovials with the

highest OVA staining were sorted by FACS and visualized, yielding the same subsets of cell

types (secretion signal, cell surface signal, and combined secretion and cell surface signal)

that likely reflects the ability to isolate a larger repertoire of B cell populations, including

plasma B cells difficult to isolate with standard antigen baiting workflows.
### **CONCLUSIONS**


The nanovial platform provides specific advantages in sorting cells based on secretions, and

also lays the foundation for the next generation of single-cell and single molecule assays

using existing accessible instrumentation. Two key features of the nanovial platform allow

for widely accessible analysis and sorting of cells based on secretions: (i) the ability to

form uniform compartments containing single cells in small volumes with minimal crosstalk

using simple pipetting and no devices; and (ii) the compatibility of the nanovials with

commercially available flow sorters such that viable cells can be sorted based on their

parallel using simple pipetting operations. Parallel encapsulation in < 1 min is an important

differentiator from microfluidic techniques, which often require tens of minutes to several

hours to sequentially form droplets while cells remain mixed and secrete within the input sample volume. [37] Rapid emulsification minimizes cross-talk by minimizing the time cells

secrete into the input sample volume (e.g. a syringe) before they are encapsulated which is

critical for enabling screening of large cell populations. Parallel encapsulation also ensures

that the secretion assay starts at the same time point, reducing differences in secretion signal

resulting from different secretion times that can add noise, reducing selection accuracy.

Nanovial emulsification and analysis steps can also be more easily performed in a sterile

environment (e.g. biosafety hood) using standard sterile plasticware (e.g. well plates, pipette

tips), as opposed to bulkier equipment. Spherical gel particles have been used previously to template emulsions, [28,29] however, the lack of a cavity precluded their use with mammalian

cells, and no secretion assays or compatibility with flow cytometry were demonstrated. We

have also previously used amphiphilic cavity-containing particles to form uniform emulsions


and perform molecular and cellular assays; [25–27] however, these previous systems were not

compatible with commercial flow cytometers due to their hydrophobic components.


Although microfluidics is used to manufacture the nanovials, the particles can be easily

not have expertise in microfluidics. Recent parallelized approaches to manufacture shaped particles using microfluidics can further enable transition to commercial scale volumes. [38 ]


Shipping of particles is far more cost-effective and rapid than replicating microfluidic setups

for generation and sorting of droplets. Further, the amount of additional expertise required

to use the nanovial system is substantially lower than required for microfluidic-based

approaches due to the familiar handling steps. Collaborators across the globe have been

able to perform nanovial assays without any hands-on training, including the experiments

shown in Figure S9 which were performed solely at Johns Hopkins University in a protein

engineering lab without any access to microfluidic devices.


The nanovial system is also compatible with commercial flow cytometers which enabled us

to screen over a million nanovials in under an hour across the experiments described in this

report (at rates exceeding 600 events/second). This throughput outperforms previous droplet microfluidic sorters applied to antibody discovery workflows. [15] Throughput can be further

improved by reduction of the nanovial size for compatibility with smaller FACS nozzle sizes

throughputs exceeding 10 million cells per day.


The structure and surface of the nanovials provide additional capabilities for tuning the

number and type of captured cells, analysis of adherent cell secretions, and analysis and

sorting of clonal colonies. The size and opening diameter of the cavity within a nanovial

can be tuned (Figure S2), enabling more deterministic loading of single cells based on size exclusion effects. [38] This could allow more rapid screening because cell loading rates

are not dictated by Poisson statistics. Besides structural changes to the particles, the

surface of particles can also be functionalized with affinity agents that specifically enrich

certain populations of cells, such as antibodies to CD3 that enrich T cells from a mixed

population. The surface of the particle also enables the attachment and growth of adherent

cell populations, such as the CHO and HEK293 cells used herein. Analysis of secretions

from adherent cells can be challenging with other microfluidic techniques which require

cells to be in suspension to flow into devices and sort afterwards. Adherent cells begin to

undergo apoptosis when removed from a solid substrate and it is expected that secretion rates of biomolecules would change in this condition. [39] The inability to perform these assays

has led to a dearth of information on the secretion phenotypes and heterogeneity of adherent

adherent bacterial biofilms. Notably, the stiffness and ligand density on the substrate can also affect what is secreted by adherent cells such as MSCs and macrophages. [40,41] The

ability to tune these properties on the nanovials could enable a deeper understanding of

substrate effects and recapitulate more relevant microenvironments. Further, in the nanovial


system, when single cells are initially seeded onto particles they adhere and grow without

nutrient limitations (Figure S6). The clonal colonies can then be encapsulated to form

dropicles, enabling high-throughput screening based on the combination of growth and

per cell secretion (i.e. overall biomass produced per unit time), potentially overcoming

previous challenges in cell line selection in which growth and biologic production can be in a trade-off relation. [13] Recent approaches to manufacture nanovials allow for localization of functional groups to the cavity which reduces cross-talk without encapsulation. [38] This

can extend the ability to capture secretions from cells over longer periods of time without

affinity antibody therapeutics relies on the selection of B and plasma cells producing
antibodies with high affinity amongst a large background of clones. [7] Although direct

antigen binding to cell surface-expressed BCRs followed by FACS has been used to isolate

antigen-specific B cells, plasma cells lose BCR expression, but represent an important

population of antibody-secreting cells that have gone through affinity maturation, and may yield higher affinity antibody sequences. [42] In addition, highly-secreting plasma cells and

plasmablasts have larger numbers of transcripts encoding the antibody sequence, making

them prime targets for sequence recovery by single-cell RT-PCR or downstream single-cell

sequencing. More generally, the activity of immune cells is largely connected to their

secretion profiles, which direct communication and effector functions and can be better

studied by sorting out specific sub-populations for further functional testing in vivo or in

vitro. The effectiveness of chimeric antigen receptor-T cell batches also appears to depend

on a multifunctional secretion of cytokines, such that sorting populations based on secretion profiles may enhance therapeutic activity. [43,44] Finally, processes of directed evolution of cell

products and cells themselves can benefit from larger numbers of clones being screened,

mutagenized, and expanded across multiple cycles using an efficient process relying on standard equipment and expertise. [45]


In sum, our approach to encapsulate single entities into uniform compartments with a

solid phase can democratize access to cutting-edge assays, creating a modular “lab on a

particle” platform for a number of single-cell and single-molecule assays. Encapsulation

is a key component for single-cell nucleic acid sequencing. Clonal colonies of bacteria,

yeast, or algae producing engineered proteins (e.g. fluorescent proteins) can also be

maintained in nanovials and sorted based on desirable features (e.g. intensity at particular

excitation/emission wavelengths). Moving beyond cells, the compartments formed can

enable digital nucleic acid amplification assays and immunoassays, where the solid phase

provides potential for barcoding and capturing of amplified assay signals. Given the

and single-molecule assays in the near future. Rapid deployment across the world is of

particular importance during emerging pandemics, enabling collective distributed research

and development, and removing the bottlenecks created by the sparsity of skilled groups

able to contribute to key points in therapeutic and diagnostic pipelines.


Nanovials were fabricated using a standard PDMS microfluidic flow focusing droplet

generator. A PEG phase comprised of 28.9% w/w 4-arm PEG-norbornene (Sigma), 3%

w/w LAP (lithium phenyl-2,4,6-trimethylbenzoylphosphinate, Sigma), and 1 mg/mL biotin PEG-thiol (5000 MW, Nanocs) in phosphate buffered saline (PBS, pH 7.2) was co-injected

PBS at a rates of 0.5 – 5 μL/min, depending on nanovial size, using syringe pumps (Harvard Apparatus PHD 2000). An oil phase comprised of Novec [™] 7500 (3M) and 0.25% w/w

fluorinated surfactant was injected at a rate of 10 – 42 μL/min to partition the aqueous

phases into monodisperse water in oil droplets. PEG and dextran polymers phase separated

on chip after approximately 5 seconds. The PEG phase was crosslinked with focused UV

light through a DAPI filter set and microscope objective (Nikon, Eclipse Ti-S) near the

outlet region of the microfluidic device. Crosslinked nanovials were collected and oil and

dextran were removed using a series of washing steps. Briefly, excess oil was removed by

pipetting and a layer of PBS was added on top of the remaining emulsions. A solution of 20% v/v perfluorooctanol (PFO, Sigma) in Novec [™] 7500 was then added to destabilize the

emulsions and transfer nanovials to the PBS phase. Excess oil was removed and samples were washed two times with Novec [™] 7500 to remove remaining surfactant. Novec [™] 7500

was removed by pipetting and residual oil was removed by washing two to three times with

hexane (Sigma). Samples were then washed three times with PBS to remove dextran from

the system. For cell experiments, nanovials were sterilized by incubating in 70% ethanol

overnight. Nanovials were then washed five times with washing buffer comprised of 0.05% Pluronic [™] F-127 (Sigma), 1% penicillin/streptomycin (Invitrogen), and 0.5% bovine serum

albumum (BSA, GeminiBio) in PBS and stored in a conical tube at 4°C.


PLL modification of nanovials. To modify the nanovial surface with poly-L-lysine (PLL), a

100 μL volume of concentrated 55 μm nanovials was suspended in 1 mL solution consisting

of 1 mg/mL thiol-poly-L-lysine-thiol (32 kDa, Nanosoft Polymers) and 0.2 % w/w LAP.

The nanovial suspension was transferred to a glass vial pre-coated with Sigmacote (Sigma

SL2–25ML) and the vial was placed on top of a mini stir plate (IKA Lab Disc IKAMAG

Magnetic Stirrer) with a micro stir bar in it. With continuous mixing, the particle suspension was exposed to UV for 60 seconds at a power of 2.9 mW/cm [2] . The particle suspension was retrieved into a 1.5 mL Eppendorf tube and washed with PBS containing 0.05% Pluronic [™ ]


F-127 three times. To further modify PLL-conjugated nanovials with fibronectin, 25 μL of

concentrated nanovials were incubated in 500 μL of 10 μg/mL or 500 μg/mL fibronectin

solution for one hour at room temperature and washed with washing buffer three times.


FACS tubes, and well-plates were pre-coated with sterile washing buffer comprised of


serum albumin (BSA, GeminiBio) in PBS unless otherwise noted.


**Nanovial assay washing procedure—** In general, nanovials are washed by centrifuging

at 300 g for 2 – 5 min to create a pellet. Supernatant is removed by carefully pipetting or

aspirating fluid above the pellet. Nanovials are then re-suspended in washing buffer or media

at a 10-fold dilution. This procedure is repeated as needed.


**Streptavidin labeling—** Biotinylated nanovials are pelleted and supernatant is removed.

For 35 and 55 μm nanovials, samples were reconstituted at a five times dilution in washing

streptavidin was included in addition to the unlabeled streptavidin. For 85 μm nanovials, 400

μg/mL streptavidin solution was added to the concentrated pellet at a 1:1 ratio and pipetted

to mix evenly. Fluorophore-conjugated streptavidin was prepared at 4 – 40 μg/mL. Excess

streptavidin was removed by washing three times.


**Biotinylated antibody labeling—** Streptavidin coated nanovials are pelleted and

supernatant is removed. For 35 and 55 μm nanovials, samples were reconstituted at a

five times dilution in washing buffer containing 5 – 20 μg/mL of the desired biotinylated

μg/mL of biotinylated antibodies was added to the concentrated pellet at a 1:1 ratio and

pipetted to mix evenly.


All cells were cultured in incubators at 37°C and 5% CO2 in static conditions unless

otherwise noted.


**Chinese hamster ovary (CHO Cells)—** CHO DP-12 cells (ATCC, CRL-12445 [™] ) were

maintained according to manufacturer’s specifications. Cell culture media was comprised

Elements A (Fisher Scientific), 0.1% Trace Elements B (Fisher Scientific), and 200 nM Methotrexate (MTX, SIGMA). CHO-K1 cells (ATCC, CCL61 [™] ) were cultured in F-12

base media (Invitrogen) supplemented with 10% FBS and 1% penicillin/streptomycin (Invitrogen). ExpiCHO cells (Fisher Scientific A29127 [™] ) were cultured in ExpiCHO [™ ]


Expression Medium (Fisher Scientific) on an orbital shaker in a 37°C incubator with ≥80%

relative humidity and 8% CO2. The shake speed was set to 120 rpm with 25 mm shaking diameter. Cells were seeded at 0.2 × 10 [6] viable cells/mL and subcultured when the cell density reached 4 × 10 [6] – 6 × 10 [6] viable cells/mL.


**Human embryonic kidney (HEK) cells—** HEK 293T cells (Thermo Life Technologies)

were cultured in DMEM medium with 10% FBS, L-glutamine (2 mM), and penicillin streptomycin (500 μg/mL).


**Hybridoma cells—** HyHel-5 cells were maintained in IMDM media (Invitrogen)

supplemented with 10% FBS (Invitrogen) and 1% penicillin/streptomycin (Invitrogen). 9E10 cells (ATCC, CRL-1729 [™] ) were maintained in RPMI media (Invitrogen) supplemented with

10% FBS (Invitrogen) and 1% penicillin/streptomycin (Invitrogen). Cells were passaged down to a final concentration of 4×10 [5] cells/mL every two days.


**Mouse immunization, serum isolation, and splenocyte isolation**


All experiments involving animals, animal cells, or tissues were performed in accordance

with the Chancellor’s Animal Research Committee ethical guidelines at the University

of California Los Angeles under protocol no ARC-2015–125. Ten week old C56BL/6J

mice (Jackson Laboratory) were immunized for a total of 7 times over 28 days with

recombinant ovalbumin (Biosearch Technologies) as a model antigen. Immunizations were made by mixing ovalbumin at 1 μg/μL in PBS with equal volume of Imject [™] alum adjuvant

(ThermoFisher Scientific). 250 μg and 25 μg doses of ovalbumin were used for initial

immunization, and subsequent 7 boosters, respectively. Four days after final immunization,

mice were euthanized with isoflurane overdose followed by cervical dislocation and

sterilized by spraying with 70% ethanol. for tissue and blood collection. For splenocyte

isolation, the spleen was removed, cut into small pieces with scissors, and pushed through a

70 μm cell strainer in a 10 cm petri dish containing 10 mL cold PBS, using the plunger

of a 10 mL syringe. The same syringe was then used to dissociate tissue clumps by

drawing and flushing the solution through a 25-gauge needle 3 times. Cells were pelleted by centrifugation at 300 g for 10 min and resuspended at 10 [8] cells/mL in EasySep [™] buffer and B lineage cells were isolated using an EasySep [™] mouse B cell negative isolation

kit (StemCell Technologies, #19854). For serum, blood was collected directly from left

ventricle via cardiac puncture immediately after euthanasia. Blood was allowed to clot at

room temperature for 4 hours, before centrifuging at 10,000 g for 10 min to separate serum.


**Cell loading in nanovials**


**Nanovial well-plate seeding—** Wells were first partially filled with media or buffer.

Diluted nanovials were then transferred into the well using a micropipette or serological

pipette and dispersed by pipetting up and down in circular motions. Nanovials were then

allowed to settle to the bottom of the well for 15 – 60 min, with longer times being required

for smaller nanovials. A diluted cell suspension was then carefully pipetted into each well

being careful to not disturb the nanovials. Cells were then allowed to settle for 15 – 30 min

and then transferred to an incubator unless otherwise noted. The amount of nanovials and

cells to add into each well was determined both analytically and experimentally. General

values for different nanovial sizes are shown in Table 1.


**Characterization of cell loading in nanovials—** Nanovials were prepared using the

modification procedures described above. 85 μm, 55 μm, and 35 μm nanovials were

used for CHO DP-12, ExpiCHO/HEK293, and B cells, respectively. RGD, RGD+PLL,

and RGD+PLL+ Fibronectin modified nanovials were prepared following procedures

described above. Antibody-coated nanovials were prepared follow procedures above using

8 μg/mL of aCD45-biotin, 8 μg/mL of aCD19-biotin, or 8 μg/mL aCD45-biotin + 8

μg/mL of aCD19-biotin. For all conditions, modified nanovials were seeded into media

containing wells following procedures described above. Cells were fluorescently labeled using CellTracker [™] following the manufacturer’s specification and seeded into the nanovials

by pipetting. HEK293 cells were first biotinylated using EZ-Link Sulfo-NHS-SS-Biotin

(ThermoFisher) following the manufacturer’s specified procedure. B cells were obtained

from mice following procedures described in ‘Mouse immunization, serum isolation, and

splenocyte isolation’. CHO DP-12 and ExpiCHO cells were incubated for 2–4 hrs in an

incubator at 37°C to allow for cell binding. HEK293 cells and B cells were incubated for 1

hr at 37°C to facilitate binding. After incubating, samples were transferred by pipetting and

unbound cells were removed from the nanovial solution by running through a cell strainer.

For 85 μm nanovials a 37 μm cell strainer was used (Stemcell Technologies) and for 35 and

55 μm nanovials a 20 μm cell strainer was used (CellTrics, ThermoFisher). Nanovials and

cell-containing cells were recovered by inverting the cell strainers over a conical tube and

passing washing buffer through it with a pipette. Samples were then imaged in well plates

using bright field and fluorescence microscopy. Cell loading fraction was characterized

using either a Matlab algorithm (CHO DP-12, ExpiCHO, B cells), or using flow cytometry

(HEK293, CytoFlex, Beckman Coulter).


**Dropicle formation and characterization**


Nanovials with 85 μm diameters were suspended in DMEM base media (Invitrogen) and then pelleted and supernatant removed by pipetting. An oil phase comprised of Novec [™ ]


7500 and 2% w/w PicoSurf was added to the particle suspension at approximately two

times the remaining volume. The sample was then vigorously pipetted for 30 – 60 s (~100

pipettes) using a 200 μL micropipette (Eppendorf). The resulting water-in-oil emulsion was

then carefully transferred into a PDMS reservoir by pipetting and imaged. Size distribution

characterization was then performed using image analysis algorithms in MATLAB. For the fluorescent images shown in Figure 1B, particles were first labeled with AlexaFluor [™] 568

streptavidin and suspended in PBS containing 2 mg/mL fluorescein isothiocyanate-dextran

(500,000 MW, Sigma). For 35 and 55 μm nanovials the same procedure was used except the

nanovials were first diluted 10-fold to reduce fraction of aggregates formed.


**Dropicle emulsion breaking**


To recover cells back into an aqueous phase following dropicle formation, excess oil was

first removed via pipetting and several mL of media was added on top of the emulsions.
To destabilize the emulsions a destabilizing agent (20% v/v PFO in Novec [™] 7500) was

pipetted on top of the emulsion layer and the sample was gently agitated. After 5 min most

of the droplets were merged and nanovials and any associated cells were transferred into the

bulk media phase. Optionally, samples can be centrifuged for 15–30 s at 200 g to coalesce

The volume energy curve depicted in Figure S5 was calculated using our previously reported approach [35], which assumes that the energy of the system is dominated by surface energy.

In Figure S5A, for each given fluid volume, the fluid assumes a morphology to minimize

the energy of the system. In Figure S5B, for the two-particle system we calculate the fluid

distribution that minimizes the total energy of the system of two particles containing two


separate fluid volumes, with the modified assumption that below a normalized volume V/V0

=2, the particles remain as aggregates. We assume that the interfacial tension between PEG

and water is negligible such that the normalized interfacial tensions are


where γ PEG/water is the interfacial tension between the PEG based nanovials and water,

γ oil/water is the tension between oil and water and γ PEG/oil is the tension between the

For viability studies depicted in Figure S6, CHO DP-12 cells were seeded into 85 μm RGD

modified nanovials. As a control, free cells were seeded into a separate well plate containing

no nanovials. Cells were allowed to adhere for 4 hours. Samples containing both the cells

and nanovials were transferred into a 15 mL conical tube, exchanged with fresh media and then concentrated via centrifugation and aspiration. Novec [™] + 2% w/w PicoSurf was added

to the concentrated sample and pipetted for 30 s to encapsulate the nanovials and associated

cells into dropicles as discussed above. Light mineral oil was added on top of the samples

to mitigate evaporation during prolonged incubation. Samples were then incubated for 2,

12, and 24 hours in an incubator at 37°C and 5% CO2. Dropicle emulsions were broken

as described above and the suspension of nanovials and cells were then transferred by

pipetting into a separate conical tube. Samples were washed with PBS and then sequentially

stained with calcein AM and propidium iodide (live/dead). The control well plate samples

were stained directly in the well plates with the live/dead stains. Nanovial samples were

transferred back into a well plate, imaged, and then analyzed in MATLAB to determine cell

viability statistics. Live/dead assays were performed with a minimum of n = 3 samples, with

greater than 1000 cells analyzed per condition.


For cell expansion characterization depicted in Figure S6C–D, samples were prepared as above except cells were first stained with CellTracker [™] and then incubated for 2 hrs in a

dropicle emulsion state. Recovered nanovials and cells were seeded into wells of a 96-well

plate and imaged over the course of a week. A control sample was prepared with cells

directly seeded into a well plate after trypsinization. All conditions were performed in

CHO DP-12 cells producing a human anti-IL-8 antibody were used for these studies. To

identify these target cells during downstream analysis CHO DP-12 cells were first stained with CellTracker [™] Blue CMAC Dye (Thermo Fisher). 85 μm nanovials containing RGD

and cells were seeded into a 12-well plate as described above and then incubated at 37°C for

2 hours to allow cells to adhere to the particles. Nanovials were recovered by pipetting and

background cells removed using a 37 μm reversible cell strainer. Recovered nanovials were


above. Samples were then washed and resuspended in CHO DP-12 media. Nanovial samples

were then compartmentalized by pipetting with oil and surfactant as described above to

create dropicles and incubated for a range of times 0, 1, 2, 4, and 8 hours to allow cells

to secrete and to facilitate capture of secreted antibodies onto the associated particle matrix

via anti IgG binding sites. After the incubation period, nanovials and associated cells were

transferred back into media by breaking the emulsions (see ‘Dropicle emulsion breaking’

section). Samples were then washed, and captured secretions were stained by adding a cell staining buffer (0.05% Pluronic [™] F-127, 2% FBS, and 1% penicillin/streptomycin in PBS (Ca [2+],Mg [2+] )) containing 30 μg/mL Goat anti-human IgG H&L (Dylight [®] 488, Abcam

ab96911) at a 1:1 ratio. After 30 min of staining, samples were then washed three to

five times with cell staining buffer and optionally stained with propidium iodide. Samples

were imaged in both brightfield and fluorescence channels in a well plate. To characterize

secretion amount per particle a MATLAB algorithm was used to identify particles in

brightfield and then count the number of cells, check for the presence of dead stain, and

integrate the total secretion label fluorescence intensity for each particle. A minimum of

4000 nanovials were analyzed for each condition and each condition was performed in

To analyze potential cross-talk when nanovials were not emulsified, samples were prepared

as described in the ‘CHO cell IgG secretion assay’ section with several modifications to

the protocol. Two sets of samples were prepared: a control sample that was incubated in

bulk solution (without emulsification) and a test sample incubated after dropicle formation.
Prior to the incubation step a separate suspension of AlexaFluor [™] 647 tagged nanovials

containing no cells were mixed into the samples. This was done in order to ensure signal on

empty nanovials that was measured did not arise from cells that may have detached from the

nanovials during various steps of the assay. Samples were washed and modified with biotin

goat anti-human IgG Fc as described above. The bulk samples were left to incubate in media

while the dropicle samples were emulsified (see ‘Dropicle formation and characterization’).

After incubating for 15 hours samples were recovered and washed with washing buffer,

stained, and imaged. The amount of cross talk was determined by comparing secretion

staining intensity of cell containing nanovials with the intensity on the control particles. A

minimum of 3500 nanovials were analyzed for each condition.


**CHO DP-12 sorting and enrichment from background cells based on secretion**


CHO DP-12 cells and CHO-K1 cells were prelabeled with CellTracker [™] Deep Red and CellTracker [™] Blue (Thermo Fisher). After labelling, cells were mixed together at various ratios (1:5, 1:100, 1:1000) and loaded into nanovials (Seeding density ~84/mm [2], lambda

~0.1). All remaining secretion assay steps were as previously described (see ‘CHO cell IgG

secretion assay’). After labelling secretions on samples with goat anti-human IgG H&L

Dylight 488, samples were sorted using FACS (BioSorter, Unionbio). Samples were excited

using both 488 nm and 561 nm lasers. Events were triggered based on nanovial absorbance

from the 561 nm laser. Single nanovial events were gated based on time of flight. Nanovials


with secretion signal were sorted by thresholding the peak intensity height collected through

a 543/22 nm filter. Samples were sorted directly into a 96-well plate and imaged with a

fluorescence microscope to quantify purity and enrichment. 100,000 single cells were sorted

HEK293T cells were washed three times with PBS pH 8, and then biotinylated using

EZ-Link Sulfo-NHS-SS-Biotin (Thermo Fisher Scientific). Per manufacturer’s protocol, the cells were resuspended at 25×10 [6] cells/mL in PBS pH 8 containing 2 mM of EZ-Link

Sulfo-NHS-SS-Biotin reagent and incubated at room temperature for 30 min with rotation.

Three washes were then conducted using PBS (pH 7.3) to remove excess byproducts. Cells were then stained with CellTrace [™] Violet dye (Thermo Fisher Scientific). Nanovials (55 μm diameter) were prepared by coating with streptavidin and Alexa Fluor [™] 647-conjugated

streptavidin at a 10:1 ratio following standard procedures (See ‘Nanovial handling and

modification’). HEK293T cells were loaded into nanovials as described in ‘Cell loading in

nanovials’. After cell loading, nanovials were modified with biotinylated goat anti-human

IgG Fc antibody (Thermo Fisher Scientific). Samples were resuspended in DMEM and

seeded in a well plate. The anti-programmed death ligand-1 (PD-L1) antibody atezolizumab

and the anti-interleukin 8 receptor beta (IL-8Rb) antibody 10H2 were cloned into the gwiz

mammalian expression vector (Genlantis) and used for transient transfection of HEK 293T

cells loaded into nanovials. Atezolizumab and 10H2 DNA were diluted to 0.05 mg/mL

Polysciences) was independently diluted to 0.1 mg/mL in OptiPro medium and incubated

at room temperature for 5 min. Equal volumes of DNA and polyethyleneimine were mixed

and incubated at room temperature for an additional 15 min. The DNA/PEI mixture was

then added to the 6-well plate while gently rotating the plate to mix. The plate was

breaking’). Recovered nanovials were stained with 30 μg/mL goat anti-human IgG H&L

DyLight 488 (Abcam) and 1 μg/mL of propidium iodide (Thermo Fisher Scientific) for 30

min at 4°C without rotation. Samples were then washed three times and analyzed via flow

cytometry (CytoFlex, Beckman Coulter).


**Enrichment of high IgG producing CHO cells, re-culture, and bulk ELISA on secreted IgG**


CHO-DP12 cells were loaded in nanovials and secreted IgG captured as described in the

‘CHO cell IgG secretion assay’ section. After labelling secretions, a fraction of each sample

was kept and imaged using fluorescence microscopy. The remaining samples were then

sorted using a FACS instrument (On-Chip Sort, On Chip Biotechnologies). Samples were

excited with both a 488 nm and 637 nm laser. Particle events were screened based on the

forward and side scatter. Particles positive for both cells and secretion signal were gated

based on peak fluorescence height collected through a 543/22 nm emission filter and a

676/37 nm emission filter respectively. Two sub-populations were sorted for each sample:

(1) particles with cells and positive secretion signal, (2) particles with cells and the top

20% of positive secretion signal. Collected samples were plated and expanded for >10 days


directly from the nanovials. After expansion, cells were released from the nanovials via

trypsinization and nanovials were removed from solution by using a 40 μm cell strainer.

Example data from this process is shown in figure S7. To quantify antibody production

of the isolated sub-populations, 30,000 cells from the expanded sub-populations as well as

unsorted control samples were plated into a 48-well plate. After cells attached the samples

were washed, replaced with 400 μL of fresh media, and incubated for 6 hours. Supernatant

was then collected and total human IgG amount was measured using ELISA (IgG (Total)

Human ELISA Kit, Invitrogen, BMS2091). Production rate per cell was calculated based

off the measured IgG concentration, incubation time, and initial number of cells seeded.

The full experiment was performed with four separate cell passages and a total of 500,000

nanovials were screened for this experiment.


**Hybridoma secretion assay and sorting**


Nanovials with 55 μm diameters were used for screening antigen-specific antibody

production from HyHel-5 hybridomas. Nanovials were sequentially coated with streptavidin

and biotinylated antibodies (20 μg/mL anti-mouse CD45, 20 μg/mL anti-mouse IgG H+L)

(see ‘Nanovial handling and modification’). Concurrently 9E10 hybridoma cells were labeled with CellTracker [™] Blue dye (Thermo Fisher) and premixed with unlabeled HyHel-5 hybridoma cells at a ratio of 25:1. Importantly the CellTracker [™] Blue dye (Thermo Fisher)

stain was not used for sorting or enrichment purposes, but served to differentiate the two

cell types in pre- and post-sort analysis to benchmark assay performance. The premixed

hybridoma cell populations were next loaded into antibody-coated hydrogel nanovials

chilled to 4°C (see ‘Cell loading in nanovials’). Nanovials and cells were maintained at

4°C for 1 hour to lower their metabolic activity and prevent accumulation of secretion onto

neighboring unloaded nanovials during the binding process. Following adhesion, unbound

cells were removed from the sample by filtering through a 20 μm cell-strainer, and the

recovered cell-loaded particles were incubated in IMDM media at 37°C for another hour

antibody signal was relatively infrequent. Finally, after allowing accumulation of sufficient

antibody signal, samples were washed a final time and labeled with 0.75 μg/mL of hen egg lysozyme (Aviva Systems Biology) tagged with Alexa Fluor [™] 647 (Microscale Protein

Labelling Kit, Thermo Fisher) (HEL-647). All samples were sorted on a Sony SH800 flow

sorter in single-cell mode with minor adjustments to the drop delay to account for the larger size of the particle nanovials. [46] Approximately 10,000 cells were screened in total for these

Nanovials with 35 or 55 μm diameters were labeled with biotinylated anti-mouse CD45

and biotinylated goat anti-mouse IgG H&L chain antibodies (40 μg/mL and 60 μg/mL

respectively) for 30 min. After incubation, nanovials were washed and resuspended in

EasySep buffer. B cell lineage cells purified from splenocytes (see ‘Mouse immunization,

serum isolation, and splenocyte isolation’) were seeded into a 24-well plate according to the

section ‘Cell loading in nanovials’, and then incubated at 37°C for 1 hour to allow cells to

adhere. To remove unattached cells from the background, samples were strained using a 37


μm reversible cell strainer and then particles were recovered by flipping the cell strainer

and washing with washing buffer. After recovery, nanovial samples were concentrated

by centrifuging particles and associated cells at 300 g for 3 min, aspirating, and then

resuspending in 1 mL EasySep buffer. Samples were compartmentalized by pipetting with

oil and surfactant (‘Dropicle formation and characterization’). Samples were then incubated

for 2 hours to allow cells to secrete and to facilitate capture of secreted antibodies onto the

associated nanovial matrix via goat anti-mouse IgG H&L sites. After the incubation period,

nanovials and associated cells were transferred back into EasySep buffer by breaking the

emulsions (see ‘Dropicle emulsion breaking’). Nanovial samples were then washed, and captured secretions were stained with AlexaFluor [™] 647 conjugated ovalbumin (Invitrogen

O34784) at a final concentration of 50 μg/mL. After 30 min of staining, samples were

washed three times in a large volume of EasySep buffer and optionally stained with

propidium iodide. An aliquot of the sample was then either sorted using a Sony SH800

FACS system based on high AF647 signal (e.g. the gate shown in Figure 6) or imaged with

a fluorescence microscope in both brightfield and fluorescence channels in a well plate.

Sorted nanovials were also imaged by fluorescence microscopy. >1,000,000 nanovials were

For assessment of the dynamic range of the on-nanovial immunoassay for antibody

capture and antigen-specific detection, 2 μL aliquots of nanovials were used for each

condition. Nanovials with 55 μm diameters were labeled with biotinylated anti-mouse CD45

and biotinylated goat anti-mouse IgG H&L chain antibodies (40 μg/mL and 60 μg/mL

respectively) for 30 min. After incubation, nanovials were washed and resuspended in

washing buffer. Mouse serum (see ‘Mouse immunization, serum isolation, and splenocyte

isolation’) at various dilutions was added to the particles and incubated for 2 hours.

After the incubation period, particles were washed, and captured secretions were stained with AlexaFluor [™] 647 conjugated ovalbumin (Invitrogen O34784) at a final concentration

of 50 μg/mL. After 30 min of staining, samples were washed five times with washing

buffer. Finally, particles were analyzed by fluorescence microscopy in both brightfield and

Single HyHel-5 hybridoma cells or single nanovials loaded with HyHel-5 cells were

separately sorted into 96-well plates (Sony SH800) containing 5 mM DTT, 0.7% NP-40,

5 μM random hexamers, and 1U RNasin Plus in PBS and stored at −80 °C until analysis.

For first-strand cDNA synthesis, sorted cells were thawed on ice, incubated at 65 °C for

Reverse Transcriptase (Thermo Fisher). The reaction was incubated at 42 °C for 10 min, 25

°C for 10 min, 50 °C for 1 hour, then 94 °C for 5 min. The cDNA product from each single

cell was then amplified for heavy chain in a sequence of nested RT-PCR reactions using primers optimized by von Boehmer et al [47] . All PCR reactions contained 1X HF Buffer, 200

μM dNTPs, and 0.02 U/μL Phusion High Fidelity DNA Polymerase (Thermo Fisher) in a


final reaction volume of 20 μL. The initial, preamplification RT-PCRs contained a mixture

of forward primers at a final concentration of 0.3 μM, the reverse primer at a concentration

of 0.2 μM, and 2 μL of the reverse-transcribed cDNA. The thermocycler conditions included

an initial denaturation at 98 °C for 5 min followed by 50 cycles of 30 sec at 98 °C, 30

sec at 46 °C, and 30 sec at 72°C then a final extension at 72 °C for 10 min. The second,

nested RT-PCRs contained 0.2 μM each of the forward and reverse primers and 2 μL of

the preamplification RT-PCR product. The thermocycler conditions were the same as in the

preamplification PCR, but with a 57 °C annealing temperature. The second PCR products

were visualized on a 1.5% agarose gel with SYBR Safe DNA gel stain (Thermo Fisher).


**Supplementary Material**


Refer to Web version on PubMed Central for supplementary material.
### **ACKNOWLEDGEMENTS**


We acknowledge support from the National Institutes of Health Grants R21GM126414, T32GM008042, T32AR071307, R01EB029455, R01EY031097, U01CA232563, a Maryland Stem Cell Research Fund Discovery Award, and the Simons Foundation Math+X Investigator Award #510776. Device mold fabrication was completed using equipment provided by the Integrated Systems Nanofabrication Cleanroom at the California NanoSystems Institute at the University of California, Los Angeles. Sorting experiments were performed in the UCLA Jonsson Comprehensive Cancer Center (JCCC) and Center for AIDS Research Flow Cytometry Core Facility that is supported by National Institutes of Health awards P30CA016042 and P30AI028697, and by the JCCC, the UCLA AIDS Institute, the David Geffen School of Medicine at UCLA, the UCLA Chancellor’s Office, and the UCLA Vice Chancellor’s Office of Research. The authors acknowledge Philip Scumpia for assistance with mouse immunization studies. The authors acknowledge the help of Aiden Di Carlo in editing the secretion assay workflow video.


Kampf C; Sjostedt E; Asplund A; Olsson I; Edlund K; Lundberg E; Navani S; Szigyarto CAK; Odeberg J; Djureinovic D; Takanen JO; Hober S; Alm T; Edqvist P-H; Berling H; Tegel H; Mulder J; Rockberg J; Nilsson P; Schwenk JM; Hamsten M; von Feilitzen K; Forsberg M; Persson L; Johansson F; Zwahlen M; von Heijne G; Nielsen J; Ponten F Tissue-Based Map of the Human Proteome. Science (80-.). 2015, 347 (6220), 1260419–1260419. 10.1126/ science.1260419.

(2). Tiller T; Meffre E; Yurasov S; Tsuiji M; Nussenzweig MC; Wardemann H Efficient Generation of Monoclonal Antibodies from Single Human B Cells by Single Cell RT-PCR and Expression
Vector Cloning. J. Immunol. Methods 2008, 329 (1–2), 112–124. 10.1016/j.jim.2007.09.017.

Cells. J. Immunol. Methods 2009, 350 (1–2), 183–193. 10.1016/j.jim.2009.08.009. [PubMed:
Giesecke C; Dörner T; Andrews SF; Wilson PC; Hunicke-Smith SP; Willson CG; Ellington AD; Georgiou G High-Throughput Sequencing of the Paired Human Immunoglobulin Heavy and Light Chain Repertoire. Nat. Biotechnol 2013, 31 (2), 166–169. 10.1038/nbt.2492. [PubMed: 23334449]

(5). DeKosky BJ; Kojima T; Rodin A; Charab W; Ippolito GC; Ellington AD; Georgiou G In-Depth Determination and Analysis of the Human Paired Heavy- and Light-Chain Antibody Repertoire.
Nat. Med 2015, 21 (1), 86–91. 10.1038/nm.3743. [PubMed: 25501908]


(6). Mcdaniel JR; DeKosky BJ; Tanno H; Ellington AD; Georgiou G Ultra-High-Throughput Sequencing of the Immune Receptor Repertoire from Millions of Lymphocytes. Nat. Protoc 2016, 11 (3), 429–442. 10.1038/nprot.2016.024. [PubMed: 26844430]

(7). Parola C; Neumeier D; Reddy ST Integrating High-Throughput Screening and Sequencing for Monoclonal Antibody Discovery and Engineering. Immunology. Blackwell Publishing Ltd January 1, 2018, pp 31–41. 10.1111/imm.12838.

(8). Wurm FM Production of Recombinant Protein Therapeutics in Cultivated Mammalian Cells.
Nature Biotechnology. November 2004, pp 1393–1398. 10.1038/nbt1026.

(9). Sander B; Andersson J; Andersson U Assessment of Cytokines by Immunofluorescence and the Paraformaldehyde-Saponin Procedure. Immunol. Rev 1991, 119 (1), 65–93. 10.1111/ j.1600-065X.1991.tb00578.x. [PubMed: 2045123]

(10). Freer G; Rindi L Intracellular Cytokine Detection by Fluorescence-Activated Flow
Cytometry: Basic Principles and Recent Advances. Methods 2013, 61 (1), 30–38. 10.1016/
j.ymeth.2013.03.035. [PubMed: 23583887]

(11). Manz R; Assenmacher M; Pflüger E; Miltenyi S; Radbruch A Analysis and Sorting of Live Cells According to Secreted Molecules, Relocated to a Cell-Surface Affinity Matrix. Proc. Natl. Acad.
Sci. U. S. A 1995, 92 (6), 1921–1925. 10.1073/pnas.92.6.1921. [PubMed: 7892200]

(12). Assenmacher M; Löhning M; Radbruch A Detection and Isolation of Cytokine Secreting Cells Using the Cytometric Cytokine Secretion Assay. Curr. Protoc. Immunol 2001, 46 (1). 10.1002/0471142735.im0627s46.

‐ (13). Borth N; Zeyda M; Katinger H Efficient Selection of High producing Subclones during Gene Amplification of Recombinant Chinese Hamster Ovary Cells by Flow Cytometry and Cell Sorting. Biotechnol. Bioeng 2000, 71 (4), 266–273. 10.1002/1097-0290(2000)71:4<266::AIDBIT1016>3.0.CO;2-2. [PubMed: 11291036]

(14). Chen Z; Chen JJ; Fan R Single-Cell Protein Secretion Detection and Profiling. Annu. Rev. Anal.
Chem 2019, 12 (1), 431–449. 10.1146/annurev-anchem-061318-115055.

(15). Mazutis L; Gilbert J; Ung WL; Weitz DA; Griffiths AD; Heyman JA Single-Cell Analysis and Sorting Using Droplet-Based Microfluidics. Nat. Protoc 2013, 8 (5), 870–891. 10.1038/ nprot.2013.046. [PubMed: 23558786]

(16). Ahn K; Kerbage C; Hunt TP; Westervelt RM; Link DR; Weitz DA Dielectrophoretic Manipulation of Drops for High-Speed Microfluidic Sorting Devices. Appl. Phys. Lett 2006, 88 (2), 1–3. 10.1063/1.2164911.

(17). Baret JC; Miller OJ; Taly V; Ryckelynck M; El-Harrak A; Frenz L; Rick C; Samuels ML;
Hutchison JB; Agresti JJ; Link DR; Weitz DA; Griffiths AD Fluorescence-Activated Droplet Sorting (FADS): Efficient Microfluidic Cell Sorting Based on Enzymatic Activity. Lab Chip 2009, 9 (13), 1850–1858. 10.1039/b902504a. [PubMed: 19532959]

(18). Li M; van Zee M; Riche CT; Tofig B; Gallaher SD; Merchant SS; Damoiseaux R; Goda K;
Di Carlo D A Gelatin Microdroplet Platform for High-Throughput Sorting of Hyperproducing Single-Cell-Derived Microalgal Clones. Small 2018, 14 (44), 1803315. 10.1002/smll.201803315.

(19). Love JC; Ronan JL; Grotenbreg GM; Van Der Veen AG; Ploegh HL A Microengraving Method for Rapid Selection of Single Cells Producing Antigen-Specific Antibodies. Nat. Biotechnol 2006, 24 (6), 703–707. 10.1038/nbt1210. [PubMed: 16699501]

(20). Park S; Han J; Kim W; Lee GM; Kim HS Rapid Selection of Single Cells with High Antibody Production Rates by Microwell Array. J. Biotechnol 2011, 156 (3), 197–202. 10.1016/ j.jbiotec.2011.08.031. [PubMed: 21925218]

(21). Le K; Tan C; Gupta S; Guhan T; Barkhordarian H; Lull J; Stevens J; Munro T A Novel Mammalian Cell Line Development Platform Utilizing Nanofluidics and Optoelectro Positioning Technology. Biotechnol. Prog 2018, 34 (6), 1438–1446. 10.1002/btpr.2690. [PubMed: 30009534]

(22). Winters A; McFadden K; Bergen J; Landas J; Berry KA; Gonzalez A; Salimi-Moosavi H;
Murawsky CM; Tagari P; King CT Rapid Single B Cell Antibody Discovery Using Nanopens and Structured Light. MAbs 2019, 11 (6), 1025–1035. 10.1080/19420862.2019.1624126.

Z; Smith C; Starkie D; White J; Sweeney B; Hinchliffe M; Tickle S; Lightwood DJ; Rehak M; Craig FF; Holmes D Cyto-Mine: An Integrated, Picodroplet System for High-Throughput Single-Cell Analysis, Sorting, Dispensing, and Monoclonality Assurance. SLAS Technol. Transl.
Life Sci. Innov 2020, 25 (2), 177–189. 10.1177/2472630319892571.

(24). Zost SJ; Gilchuk P; Chen RE; Case JB; Reidy JX; Trivette A; Nargi RS; Sutton RE; Suryadevara N; Chen EC; Binshtein E; Shrihari S; Ostrowski M; Chu HY; Didier JE; MacRenaris KW;
Jones T; Day S; Myers L; Eun-Hyung Lee F; Nguyen DC; Sanz I; Martinez DR; Rothlauf PW;
Bloyet L-M; Whelan SPJ; Baric RS; Thackray LB; Diamond MS; Carnahan RH; Crowe JE Rapid Isolation and Profiling of a Diverse Panel of Human Monoclonal Antibodies Targeting the SARS-CoV-2 Spike Protein. Nat. Med. 2020 269 2020, 26 (9), 1422–1427. 10.1038/ s41591-020-0998-x.

(25). Destgeer G; Ouyang M; Wu CY; Di Carlo D Fabrication of 3D Concentric Amphiphilic Microparticles to Form Uniform Nanoliter Reaction Volumes for Amplified Affinity Assays.
Lab Chip 2020, 20 (19), 3503–3514. 10.1039/d0lc00698j. [PubMed: 32895694]

(26). Wu C-Y; Ouyang M; Wang B; de Rutte J; Joo A; Jacobs M; Ha K; Bertozzi AL; Di Carlo D Monodisperse Drops Templated by 3D-Structured Microparticles. Sci. Adv 2020, 6 (45), eabb9023. 10.1126/sciadv.abb9023.

(27). Destgeer G; Ouyang M; Di Carlo D Engineering Design of Concentric Amphiphilic Microparticles for Spontaneous Formation of Picoliter to Nanoliter Droplet Volumes. Anal.
Chem 2021. 10.1021/acs.analchem.0c04184.

(28). Novak R; Zeng Y; Shuga J; Venugopalan G; Fletcher DA; Smith MT; Mathies RA Single-Cell Multiplex Gene Detection and Sequencing with Microfluidically Generated Agarose Emulsions.
Angew. Chemie Int. Ed 2011, 50 (2), 390–395. 10.1002/anie.201006089.

(29). Hatori MN; Kim SC; Abate AR Particle-Templated Emulsification for Microfluidics-Free Digital Biology. Anal. Chem 2018, 90 (16), 9813–9820. 10.1021/acs.analchem.8b01759. [PubMed: 30033717]

(30). Ma S; Thiele J; Liu X; Bai Y; Abell C; Huck WTS Fabrication of Microgel Particles with Complex Shape via Selective Polymerization of Aqueous Two-Phase Systems. Small 2012, 8 (15), 2356–2360. 10.1002/smll.201102715. [PubMed: 22648761]

(31). Fairbanks BD; Schwartz MP; Halevi AE; Nuttelman CR; Bowman CN; Anseth KS A Versatile Synthetic Extracellular Matrix Mimic via Thiol-Norbornene Photopolymerization. Adv. Mater 2009. 10.1002/adma.200901808.

(32). Liu Q; Zhao M; Mytnyk S; Klemm B; Zhang K; Wang Y; Yan D; Mendes E; van Esch JH Self-Orienting Hydrogel Micro-Buckets as Novel Cell Carriers. Angew. Chemie Int. Ed 2019, 58 (2), 547–551. 10.1002/anie.201811374.

(33). Collins DJ; Neild A; deMello A; Liu AQ; Ai Y The Poisson Distribution and beyond: Methods
for Microfluidic Droplet Production and Single Cell Encapsulation. Lab on a Chip. Royal Society of Chemistry July 21, 2015, pp 3439–3459. 10.1039/c5lc00614g.

(34). Basu AS Digital Assays Part II: Digital Protein and Cell Assays. SLAS Technol. 2017, 22 (4), 387–405. 10.1177/2472630317705681. [PubMed: 28548029]

(35). Ha K; de Rutte J; Di Carlo D; Bertozzi A Minimal Surface Configurations for Axisymmetric Microparticles. UCLA Comput. Appl. Math. Reports 2020, No. 20–38.

(36). Hong JK; Lakshmanan M; Goudar C; Lee DY Towards next Generation CHO Cell Line Development and Engineering by Systems Approaches. Current Opinion in Chemical Engineering. Elsevier Ltd December 1, 2018, pp 1–10. 10.1016/j.coche.2018.08.002.

(37). Eyer K; Doineau RCL; Castrillon CE; Briseño-Roa L; Menrath V; Mottet G; England P;
Godina A; Brient-Litzler E; Nizak C; Jensen A; Griffiths AD; Bibette J; Bruhns P; Baudry J Single-Cell Deep Phenotyping of IgG-Secreting Cells for High-Resolution Immune Monitoring.
Nat. Biotechnol 2017, 35 (10), 977–982. 10.1038/nbt.3964. [PubMed: 28892076]

(38). Lee S; de Rutte J; Dimatteo R; Koo D; Di Carlo D Scalable Fabrication and Use of 3D Structured Microparticles Spatially Functionalized with Biomolecules. ACS Nano 2021. 10.1021/acsnano.1c05857.


(39). Zhong X; Rescorla FJ Cell Surface Adhesion Molecules and Adhesion-Initiated Signaling:
Understanding of Anoikis Resistance Mechanisms and Therapeutic Opportunities. Cellular Signalling. Pergamon February 1, 2012, pp 393–401. 10.1016/j.cellsig.2011.10.005.

(40). McWhorter FY; Davis CT; Liu WF Physical and Mechanical Regulation of Macrophage Phenotype and Function. Cell. Mol. Life Sci 2015, 72 (7), 1303–1316. 10.1007/ S00018-014-1796-8/FIGURES/4. [PubMed: 25504084]

(41). Wechsler ME; Rao VV; Borelli AN; Anseth KS Engineering the MSC Secretome: A Hydrogel Focused Approach. Adv. Healthc. Mater 2021, 10 (7), 2001948. 10.1002/ADHM.202001948.

(42). Reddy ST; Ge X; Miklos AE; Hughes RA; Kang SH; Hoi KH; Chrysostomou C; Hunicke-Smith SP; Iverson BL; Tucker PW; Ellington AD; Georgiou G Monoclonal Antibodies Isolated without Screening by Analyzing the Variable-Gene Repertoire of Plasma Cells. Nat. Biotechnol. 2010 289 2010, 28 (9), 965–969. 10.1038/nbt.1673.

Dorfmeier C; Chen F; Tian L; Parakandi H; Gupta M; Young RM; Johnson FB; Kulikovskaya I; Liu L; Xu J; Kassim SH; Davis MM; Levine BL; Frey NV; Siegel DL; Huang AC; Wherry EJ; Bitter H; Brogdon JL; Porter DL; June CH; Melenhorst JJ Determinants of Response and Resistance to CD19 Chimeric Antigen Receptor (CAR) T Cell Therapy of Chronic Lymphocytic Leukemia. Nat. Med 2018, 24 (5), 563–571. 10.1038/s41591-018-0010-1. [PubMed: 29713085]

(44). Rossi J; Paczkowski P; Shen YW; Morse K; Flynn B; Kaiser A; Ng C; Gallatin K; Cain T;
Fan R; Mackay S; Heath JR; Rosenberg SA; Kochenderfer JN; Zhou J; Bot A Preinfusion Polyfunctional Anti-CD19 Chimeric Antigen Receptor T Cells Are Associated with Clinical Outcomes in NHL. Blood 2018, 132 (8), 804–814. 10.1182/blood-2018-01-828343. [PubMed: 29895668]

(45). Di Carlo D Technologies for the Directed Evolution of Cell Therapies. SLAS Technol. Transl.
Life Sci. Innov 2019, 24 (4), 359–372. 10.1177/2472630319834897.

(46). de Rutte J; Dimatteo R; Zhu S; Archang M; Di Carlo D Sorting Single-Cell Microcarriers Using Commercial Flow Cytometers. SLAS Technol. Transl. Life Sci. Innov 2021.

(47). von Boehmer L; Liu C; Ackerman S; Gitlin AD; Wang Q; Gazumyan A; Nussenzweig MC Sequencing and Cloning of Antigen-Specific Antibodies from Mouse Memory B Cells. Nat.
Protoc. 2016 1110 2016, 11 (10), 1908–1923. 10.1038/nprot.2016.102.


**Figure 1. Microparticle platform for high-throughput single-cell secretion screening.**
**(A)** Individual cells are loaded into prefabricated microparticle containers (nanovials) and

bound using a variety of binding schemes (i,ii). Particles and associated cells are agitated

by pipetting with biocompatible oil and surfactant to generate monodisperse compartments

(known as dropicles), which are dictated by the particle size preventing crosstalk between

microcontainers. Cells are incubated to accumulate secretions on associated particles and

transferred back to a water phase for fluorescent labeling. Particles, cells, and associated

secretions are then analyzed and sorted using high-throughput commercial flow sorters.

Isolated populations can then be screened downstream for different phenotypic (growth,

productivity) and genotypic properties (RNA expression). **(B)** Photograph of a tube with

2 million dropicles formed using simple pipetting steps in less than 1 minute (left).

Microscopy image of nanovials with cells and associated secretions after unsealing the

nanovials and staining with fluorescent labels. **(D)** Example of a flow cytometry plot and

post-sort images of enriched highly-secreting populations. Scale bars are 100 μm.


**Figure 2. Loading and binding of single cells into nanovials.**
**(A)** Particles are loaded into wells and settle with their cavities oriented upright due to

their asymmetric center of mass. Cells are then seeded into the open cavities and attach to

various binding moieties. Unbound cells are washed away using a reversible cell strainer

and recovered particles and associated cells are analyzed. **(B)** Example microscopy images

of fluorescently tagged cells bound to nanovials. **(C)** Comparison of cell binding is plotted

below for different cell types and binding moieties. Adherent CHO DP-12 (blue) cells

are bound to particle cavities through integrin binding sites (RGD peptide) linked to the

particle matrix. Cell retention for suspension adapted ExpiCHO (green) was increased by

the nanovial surface increased retention of B cells (red). **(D)** Loading of cells into nanovial

cavities follows Poisson statistics. > 500 particles were analyzed for each condition in cell

retention experiments. Error bars represent SD of n = 3 samples for loading distribution.


**Figure 3. Massively parallel device-free formation of uniform droplets.**
**(A)** Biocompatible oil and surfactant are added to a tube containing concentrated particles.

The suspension is pipetted vigorously for 1 minute to generate smaller and smaller

emulsions. **(B)** Microscopy images of the emulsions show a uniform population of droplets

containing particles and smaller background satellite droplets. **(C)** Histograms of dropicle

diameter for different nanovial sizes. Nanovial-containing droplets are highly uniform with

comparable size distributions to advanced microfluidic techniques (CV<5%). **(D)** For both

nanovial sizes, nearly all droplets formed have either 0 or 1 particle encapsulated, with only

a small fraction (<1% for 85 μm particles and <5% for 35 μm particles) containing 2 or more

particles per droplet. Scale bars, 200 μm.


**Figure 4. Analysis of single-cell secretions using dropicles.**
**(A-B)** Characterization of cross-talk when performing a secretion assay with human IgG

producing CHO cells with and without an encapsulation step. **(A)** Significant cross-talk is

observed when cells and particles are left in an aqueous phase during secretion incubation.

**(B)** Minimal cross-talk is observed when cells and associated particles are encapsulated

in oil during the secretion incubation step. Thresholds in both **(A)** and **(B)** are set at

3 standard deviations above empty particle signal for the encapsulation condition. **(C)**

Measured secretion signal increases with incubation time due to accumulation of more

secreted molecules. **(D)** Averaged secretion measurements across the producing population

shows signal increasing proportionally with time across 3 separate samples. Error bars

represent standard deviation between samples. **(E)** A secretion assay was performed on a

mixture of human IgG producing CHO cells (magenta) spiked into a non-producing CHO

cell population (blue). Samples were sorted based on positive IgG signal using FACS and

imaged using fluorescence microscopy to determine purity and enrichment ratio. **(F)** Spiked

target cells were successfully isolated across a range of dilutions (1:5 – 1:1000) at purity

up to 99% and nearly 1000-fold enrichment. 100,000 single cells were sorted during the

enrichment study.


**Figure 5. Selection of highly secreting cell sub-populations using FACS.**
**(A)** The secreting population of cells were gated and sorted based on IgG secretion signal and CellTracker [™] (CT) labelling. Both cells with any secretion signal disparate from

background as well as the top 20% of secretors were separately sorted. **(B)** Microscopy

images before and after sorting show enrichment of secreting cells with fluorescence

intensity proportional to the selection criteria. **(C)** Example images of cells expanded

out of nanovials after encapsulation and release. **(D)** After expanding isolated cells for

10 days, bulk ELISA was performed to determine the production rate for the different

sub-populations. The full experiment was performed with separate cell passages (n = 4).

**Figure 6. Detection and sorting of antigen-specific antibody secreting cells.**
**(A)** Hybridomas or B cells loaded into nanovials secrete antibodies which are captured onto

the nanovial surface via biotinylated capture antibodies. Captured IgG is then labeled with

fluorescent antigen to assess specificity of the secreted IgG. **(B)** Fluorescence microscopy images reveal specific signal from binding to Alexa Fluor [™] 647 conjugated hen egg

hybridomas spiked into 9E10 hybridomas (CellTracker [™] Blue) at a 1:25 ratio were assayed

by fluorescence microscopy for HEL-specific signal before FACS sorting (Pre-Sort) and

after sorting using a high HEL-AF647 gate (Post-Sort). A table showing the Pre-Sort and

Post-Sort statistics is shown. **(D)** Using the index sorting function of the flow cytometer we

sorted single hybridomas loaded onto nanovials and (i) demonstrate that RNA can be reverse

transcribed and amplified from single cells loaded on nanovials at comparable rates to single

cells sorted that were freely suspended. A gel band corresponding to the correct heavy chain

amplicon length is observed. (ii) We additionally demonstrate that individual hybridomas

can be expanded into a clonal colony directly from the nanovials following sorting. **(E)**


Antibody-secreting B cells from ovalbumin (OVA)-immunized mice are assayed for antigen

specificity using nanovials. OVA-specific signal is observed directly on the nanovials by

fluorescence microscopy down to 20,000-times dilution of serum from OVA-immunized

mice but not control mice. B cells loaded on nanovials were observed to have both cell

surface signal and OVA-specific signal by fluorescence microscopy. Following FACS sorting

based on a gate encompassing the top 2.17% of OVA fluorescence area signal, OVA-specific

antibody-secreting cells were successfully imaged possessing minimal cell surface staining

**Table 1.**


Volume of concentrated nanovials to add for different well and nanovial sizes.