INFO:__main__:Found 8 PDF files to test
INFO:__main__:
================================================================================
INFO:__main__:TEST 1: test.pdf
INFO:__main__:================================================================================
INFO:services.parser.pipeline.builder:Starting pipeline for document.pdf
INFO:services.parser.pipeline.stages.loader:Loaded PDF: 33 pages
INFO:services.parser.pipeline.stages.loader:Extracted metadata: {'page_count': 33, 'pdf_author': '', 'pdf_title': 'Building an atlas of mechanobiology: high-throughput contractility screen of 2418 kinase inhibitors in five primary human cell types reveals selective divergent responses among related cell types', 'pdf_subject': '', 'pdf_creator': ''}
INFO:services.parser.pipeline.stages.loader:PDF validation passed
INFO:services.parser.pipeline.stages.analysis:Extracted 126 bold text spans
INFO:services.parser.pipeline.stages.analysis:Detected title: Building an atlas of mechanobiology: high-throughput contractility screen of
INFO:services.parser.pipeline.stages.analysis:Detected 7 section headers
INFO:services.parser.pipeline.stages.analysis:Analyzing page 1 for abstract (2129 chars)
INFO:services.parser.pipeline.stages.analysis:Found Abstract section (1067 chars)
INFO:services.parser.pipeline.stages.geometry:Detected line numbers, suggested crop at 58.928001403808594pt
INFO:services.parser.pipeline.stages.geometry:No footer detected, using default 40pt bottom margin
INFO:services.parser.pipeline.stages.geometry:Cropping margins: default top=60pt, bottom=40pt, left=58.928001403808594pt
INFO:services.parser.pipeline.stages.geometry:Page 1: Detected large header, top margin: 60pt
INFO:services.parser.pipeline.stages.geometry:Cropped left margin at 58.928001403808594pt for line numbers
INFO:services.parser.pipeline.stages.geometry:Detected 13 captions
INFO:services.parser.pipeline.stages.geometry:Detected 13 captions on cropped pages
INFO:services.parser.pipeline.stages.figures:Detecting figure regions for 13 captions using vertical deletion + clusters
WARNING:services.parser.pipeline.stages.figures:Figure region too short (6.168773651123047pt), skipping
INFO:services.parser.pipeline.stages.figures:Created 25 figure regions total
INFO:services.parser.pipeline.stages.extraction:Extracting markdown from 33 pages using pymupdf4llm
INFO:services.parser.pipeline.stages.extraction:Extracted 42837 characters total
INFO:services.parser.pipeline.stages.reflow:Reflowed text: 1491 lines -> 1491 lines
INFO:services.parser.pipeline.stages.cleanup:Cleanup: 42836 -> 35282 chars (82.4% retained)
INFO:services.parser.pipeline.stages.labeling:Injecting section labels
INFO:services.parser.pipeline.stages.labeling:Labeled section: introduction
INFO:services.parser.pipeline.stages.labeling:Labeled section: results
INFO:services.parser.pipeline.stages.labeling:Labeled section: discussion
INFO:services.parser.pipeline.stages.labeling:Labeled section: acknowledgements
INFO:services.parser.pipeline.stages.formatting:Split document into 5 sections: ['preamble', 'introduction', 'results', 'discussion', 'acknowledgements']
WARNING:services.parser.pipeline.stages.formatting:Missing title
WARNING:services.parser.pipeline.stages.formatting:Missing required section group 'abstract'. Expected one of: ['abstract']
WARNING:services.parser.pipeline.stages.formatting:Missing authors information
WARNING:services.parser.pipeline.stages.formatting:Missing required section group 'methods'. Expected one of: ['methods', 'materials_and_methods', 'experimental', 'methodology', 'materials and methods']
WARNING:services.parser.pipeline.stages.formatting:Missing required section group 'references'. Expected one of: ['references', 'bibliography']
WARNING:services.parser.pipeline.builder:Validation failed: has_title
WARNING:services.parser.pipeline.builder:Validation failed: has_abstract
WARNING:services.parser.pipeline.builder:Validation failed: has_authors
WARNING:services.parser.pipeline.builder:Validation failed: has_methods
WARNING:services.parser.pipeline.builder:Validation failed: has_references
INFO:services.parser.pipeline.stages.indexing:Indexed 298 sentences across 5 sections
INFO:services.parser.pipeline.extractors.citations:Extracted 6 citations
INFO:services.parser.pipeline.extractors.figures:Extracted 22 figures and 22 figure references
INFO:services.parser.pipeline.builder:Pipeline complete: 5 sections, 6 citations, 22 figures, 0 bibliography entries
INFO:__main__:
First 500 characters:
INFO:__main__:--------------------------------------------------------------------------------
INFO:__main__:--------------------------------------------------------------------------------
INFO:__main__:
Last 500 characters:
INFO:__main__:--------------------------------------------------------------------------------
INFO:__main__:--------------------------------------------------------------------------------
INFO:__main__:
ANALYSIS:
INFO:__main__:  Length: 35281 characters
INFO:__main__:  Figures detected: 0
INFO:__main__:  Section headers: 4
INFO:__main__:  ✓ No obvious issues detected
INFO:__main__:
================================================================================
INFO:__main__:TEST 2: test2.pdf
INFO:__main__:================================================================================
INFO:services.parser.pipeline.builder:Starting pipeline for document.pdf
INFO:services.parser.pipeline.stages.loader:Loaded PDF: 16 pages
INFO:services.parser.pipeline.stages.loader:Extracted metadata: {'page_count': 16, 'pdf_author': 'Ivan Pushkarsky', 'pdf_title': 'Elastomeric sensor surfaces for high-throughput single-cell force cytometry', 'pdf_subject': 'Nature Biomedical Engineering, doi:10.1038/s41551-018-0193-2', 'pdf_creator': 'Springer'}
INFO:services.parser.pipeline.stages.loader:PDF validation passed
INFO:services.parser.pipeline.stages.analysis:Extracted 280 bold text spans
INFO:services.parser.pipeline.stages.analysis:Detected title: Elastomeric sensor surfaces for high-throughput
INFO:services.parser.pipeline.stages.analysis:Detected 5 section headers
INFO:services.parser.pipeline.stages.analysis:Analyzing page 1 for abstract (6437 chars)
WARNING:services.parser.pipeline.stages.analysis:No suitable abstract paragraph found
INFO:services.parser.pipeline.stages.geometry:No line numbers detected
INFO:services.parser.pipeline.stages.geometry:Detected footer, suggested bottom margin: 44pt
INFO:services.parser.pipeline.stages.geometry:Cropping margins: default top=60pt, bottom=43.86407470703125pt, left=0pt
INFO:services.parser.pipeline.stages.geometry:Detected 8 captions
INFO:services.parser.pipeline.stages.geometry:Detected 8 captions on cropped pages
INFO:services.parser.pipeline.stages.figures:Detecting figure regions for 8 captions using vertical deletion + clusters
WARNING:services.parser.pipeline.stages.figures:Figure region too short (15.8798828125pt), skipping
WARNING:services.parser.pipeline.stages.figures:Figure region too short (-11.399365425109863pt), skipping
INFO:services.parser.pipeline.stages.figures:Created 37 figure regions total
INFO:services.parser.pipeline.stages.extraction:Extracting markdown from 16 pages using pymupdf4llm
INFO:services.parser.pipeline.stages.extraction:Extracted 97267 characters total
INFO:services.parser.pipeline.stages.reflow:Reflowed text: 1590 lines -> 704 lines
INFO:services.parser.pipeline.stages.cleanup:Cleanup: 97267 -> 94605 chars (97.3% retained)
INFO:services.parser.pipeline.stages.labeling:Injecting section labels
INFO:services.parser.pipeline.stages.labeling:Labeled section: methods
INFO:services.parser.pipeline.stages.labeling:Labeled section: acknowledgements
INFO:services.parser.pipeline.stages.labeling:Inserted Introduction label (fallback)
INFO:services.parser.pipeline.stages.formatting:Split document into 4 sections: ['preamble', 'introduction', 'methods', 'acknowledgements']
WARNING:services.parser.pipeline.stages.formatting:Missing title
WARNING:services.parser.pipeline.stages.formatting:Missing required section group 'abstract'. Expected one of: ['abstract']
WARNING:services.parser.pipeline.stages.formatting:Missing authors information
WARNING:services.parser.pipeline.stages.formatting:Missing required section group 'results'. Expected one of: ['results', 'results_and_discussion']
WARNING:services.parser.pipeline.stages.formatting:Missing required section group 'discussion'. Expected one of: ['discussion', 'conclusions', 'results_and_discussion', 'conclusion']
WARNING:services.parser.pipeline.stages.formatting:Missing required section group 'references'. Expected one of: ['references', 'bibliography']
WARNING:services.parser.pipeline.builder:Validation failed: has_title
WARNING:services.parser.pipeline.builder:Validation failed: has_abstract
WARNING:services.parser.pipeline.builder:Validation failed: has_authors
WARNING:services.parser.pipeline.builder:Validation failed: has_results
WARNING:services.parser.pipeline.builder:Validation failed: has_discussion
WARNING:services.parser.pipeline.builder:Validation failed: has_references
INFO:services.parser.pipeline.stages.indexing:Indexed 937 sentences across 4 sections
INFO:services.parser.pipeline.extractors.citations:Extracted 104 citations
INFO:services.parser.pipeline.extractors.figures:Extracted 47 figures and 0 figure references
INFO:services.parser.pipeline.builder:Pipeline complete: 4 sections, 104 citations, 47 figures, 0 bibliography entries
INFO:__main__:
First 500 characters:
INFO:__main__:--------------------------------------------------------------------------------
INFO:__main__:--------------------------------------------------------------------------------
INFO:__main__:
Last 500 characters:
INFO:__main__:--------------------------------------------------------------------------------
INFO:__main__:--------------------------------------------------------------------------------
INFO:__main__:
ANALYSIS:
INFO:__main__:  Length: 94636 characters
INFO:__main__:  Figures detected: 0
INFO:__main__:  Section headers: 7
WARNING:__main__:  ISSUES FOUND:
WARNING:__main__:    - Found 8 very long paragraphs (>2000 chars)
INFO:__main__:
================================================================================
INFO:__main__:TEST 3: test3.pdf
INFO:__main__:================================================================================
INFO:services.parser.pipeline.builder:Starting pipeline for document.pdf
INFO:services.parser.pipeline.stages.loader:Loaded PDF: 15 pages
INFO:services.parser.pipeline.stages.loader:Extracted metadata: {'page_count': 15, 'pdf_author': 'Rene Yu-Hong Cheng', 'pdf_title': 'SEC-seq: association of molecular signatures with antibody secretion in thousands of single human plasma cells', 'pdf_subject': 'Nature Communications, doi:10.1038/s41467-023-39367-8', 'pdf_creator': 'Springer'}
INFO:services.parser.pipeline.stages.loader:PDF validation passed
INFO:services.parser.pipeline.stages.analysis:Extracted 55 bold text spans
INFO:services.parser.pipeline.stages.analysis:Detected 0 section headers
INFO:services.parser.pipeline.stages.analysis:Analyzing page 1 for abstract (3857 chars)
WARNING:services.parser.pipeline.stages.analysis:No suitable abstract paragraph found
INFO:services.parser.pipeline.stages.geometry:No line numbers detected
INFO:services.parser.pipeline.stages.geometry:Detected footer, suggested bottom margin: 37pt
INFO:services.parser.pipeline.stages.geometry:Cropping margins: default top=60pt, bottom=37.2957763671875pt, left=0pt
INFO:services.parser.pipeline.stages.geometry:Detected 5 captions
INFO:services.parser.pipeline.stages.geometry:Detected 5 captions on cropped pages
INFO:services.parser.pipeline.stages.figures:Detecting figure regions for 5 captions using vertical deletion + clusters
INFO:services.parser.pipeline.stages.figures:Created 30 figure regions total
INFO:services.parser.pipeline.stages.extraction:Extracting markdown from 15 pages using pymupdf4llm
INFO:services.parser.pipeline.stages.extraction:Extracted 76316 characters total
INFO:services.parser.pipeline.stages.reflow:Reflowed text: 1241 lines -> 448 lines
INFO:services.parser.pipeline.stages.cleanup:Cleanup: 76316 -> 64538 chars (84.6% retained)
INFO:services.parser.pipeline.stages.labeling:Injecting section labels
INFO:services.parser.pipeline.stages.formatting:Split document into 1 sections: ['preamble']
WARNING:services.parser.pipeline.stages.formatting:Missing title
WARNING:services.parser.pipeline.stages.formatting:Missing required section group 'abstract'. Expected one of: ['abstract']
WARNING:services.parser.pipeline.stages.formatting:Missing authors information
WARNING:services.parser.pipeline.stages.formatting:Missing required section group 'introduction'. Expected one of: ['introduction']
WARNING:services.parser.pipeline.stages.formatting:Missing required section group 'methods'. Expected one of: ['methods', 'materials_and_methods', 'experimental', 'methodology', 'materials and methods']
WARNING:services.parser.pipeline.stages.formatting:Missing required section group 'results'. Expected one of: ['results', 'results_and_discussion']
WARNING:services.parser.pipeline.stages.formatting:Missing required section group 'discussion'. Expected one of: ['discussion', 'conclusions', 'results_and_discussion', 'conclusion']
WARNING:services.parser.pipeline.stages.formatting:Missing required section group 'references'. Expected one of: ['references', 'bibliography']
WARNING:services.parser.pipeline.builder:Validation failed: has_title
WARNING:services.parser.pipeline.builder:Validation failed: has_abstract
WARNING:services.parser.pipeline.builder:Validation failed: has_authors
WARNING:services.parser.pipeline.builder:Validation failed: has_introduction
WARNING:services.parser.pipeline.builder:Validation failed: has_methods
WARNING:services.parser.pipeline.builder:Validation failed: has_results
WARNING:services.parser.pipeline.builder:Validation failed: has_discussion
WARNING:services.parser.pipeline.builder:Validation failed: has_references
INFO:services.parser.pipeline.stages.indexing:Indexed 616 sentences across 1 sections
INFO:services.parser.pipeline.extractors.citations:Extracted 64 citations
INFO:services.parser.pipeline.extractors.figures:Extracted 90 figures and 0 figure references
INFO:services.parser.pipeline.builder:Pipeline complete: 1 sections, 64 citations, 90 figures, 0 bibliography entries
INFO:__main__:
First 500 characters:
INFO:__main__:--------------------------------------------------------------------------------
INFO:__main__:--------------------------------------------------------------------------------
INFO:__main__:
Last 500 characters:
INFO:__main__:--------------------------------------------------------------------------------
INFO:__main__:--------------------------------------------------------------------------------
INFO:__main__:
ANALYSIS:
INFO:__main__:  Length: 64538 characters
INFO:__main__:  Figures detected: 0
INFO:__main__:  Section headers: 0
WARNING:__main__:  ISSUES FOUND:
WARNING:__main__:    - Found 6 very long paragraphs (>2000 chars)
INFO:__main__:
================================================================================
INFO:__main__:TEST 4: test4.pdf
INFO:__main__:================================================================================
INFO:services.parser.pipeline.builder:Starting pipeline for document.pdf
INFO:services.parser.pipeline.stages.loader:Loaded PDF: 33 pages
INFO:services.parser.pipeline.stages.loader:Extracted metadata: {'page_count': 33, 'pdf_author': 'Joseph de Rutte, Robert Dimatteo, Maani M. Archang, Mark van Zee, Doyeon Koo, Sohyung Lee, Allison C. Sharrow, Patrick J. Krohl, Michael Mellody, Sheldon Zhu, James V. Eichenbaum, Monika Kizerwetter, Shreya Udani, Kyung Ha, Richard C. Willson, Andrea L. Bertozzi, Jamie Spangler, Robert Damoiseaux, Dino Di Carlo', 'pdf_title': 'Suspendable hydrogel nanovials for massively parallel single-cell functional analysis and sorting', 'pdf_subject': '', 'pdf_creator': 'AH Formatter V7.2 MR3 for Linux64 : 7.2.4.55390 (2022-01-31T09:48+09)'}
INFO:services.parser.pipeline.stages.loader:PDF validation passed
INFO:services.parser.pipeline.stages.analysis:Extracted 107 bold text spans
INFO:services.parser.pipeline.stages.analysis:Detected 6 section headers
INFO:services.parser.pipeline.stages.analysis:Analyzing page 1 for abstract (4698 chars)
WARNING:services.parser.pipeline.stages.analysis:No suitable abstract paragraph found
INFO:services.parser.pipeline.stages.geometry:No line numbers detected
INFO:services.parser.pipeline.stages.geometry:Detected footer, suggested bottom margin: 80pt
INFO:services.parser.pipeline.stages.geometry:Cropping margins: default top=60pt, bottom=80pt, left=0pt
INFO:services.parser.pipeline.stages.geometry:Detected 6 captions
INFO:services.parser.pipeline.stages.geometry:Detected 6 captions on cropped pages
INFO:services.parser.pipeline.stages.figures:Detecting figure regions for 6 captions using vertical deletion + clusters
INFO:services.parser.pipeline.stages.figures:Created 14 figure regions total
INFO:services.parser.pipeline.stages.extraction:Extracting markdown from 33 pages using pymupdf4llm
