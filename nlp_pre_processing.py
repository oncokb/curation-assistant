from nltk.stem import WordNet Lemmatizer
import nltk
text = word_tokenize(u'The echinoderm microtubule-associated protein-like 4 '
                u'(EML4)-anaplastic lymphoma kinase (ALK) fusion oncogene '
                u'represents a molecular target in a small subset of non-small'
                u' cell lung cancers (NSCLCs). This fusion leads to '
                u'constitutive ALK activation with potent transforming '
                u'activity. In a pivotal phase 1 clinical trial, the ALK '
                u'tyrosine kinase inhibitor (TKI) crizotinib (PF-02341066) '
                u'demonstrated impressive antitumor activity in the majority '
                u'of patients with NSCLC harboring ALK fusions. However, '
                u'despite these remarkable initial responses, cancers e'
                u'ventually develop resistance to crizotinib, usually '
                u'within 1 y, thereby limiting the potential clinical benefit. '
                u'To determine how cancers acquire resistance to ALK inhibitors, '
                u'we established a model of acquired resistance to crizotinib by '
                u'exposing a highly sensitive EML4-ALK-positive NSCLC cell line to '
                u'increasing doses of crizotinib until resistance emerged. We found'
                u' that cells resistant to intermediate doses of crizotinib developed '
                u'amplification of the EML4-ALK gene. Cells resistant to higher doses '
                u'(1 μM) also developed a gatekeeper mutation, L1196M, within the kinase'
                u' domain, rendering EML4-ALK insensitive to crizotinib. This gatekeeper '
                u'mutation was readily detected using a unique and highly sensitive '
                u'allele-specific PCR assay. Although crizotinib was ineffectual '
                u'against EML4-ALK harboring the gatekeeper mutation, we observed '
                u'that two structurally different ALK inhibitors, NVP-TAE684 and '
                u'AP26113, were highly active against the resistant cancer cells '
                u'in vitro and in vivo. Furthermore, these resistant cells remained'
                u' highly sensitive to the Hsp90 inhibitor 17-AAG. Thus, we have '
                u'developed a model of acquired resistance to ALK inhibitors and have '
                u'shown that second-generation ALK TKIs or Hsp90 inhibitors are effective in '
                u'treating crizotinib-resistant tumors harboring secondary gatekeeper '
                u'mutations.')

pos_tags = nltk.pos_tag(text) # part of speech tags

wnet = WordNetLemmatizer()
wnet.lemmatizer(u'The echinoderm microtubule-associated protein-like 4 '
                u'(EML4)-anaplastic lymphoma kinase (ALK) fusion oncogene '
                u'represents a molecular target in a small subset of non-small'
                u' cell lung cancers (NSCLCs). This fusion leads to '
                u'constitutive ALK activation with potent transforming '
                u'activity. In a pivotal phase 1 clinical trial, the ALK '
                u'tyrosine kinase inhibitor (TKI) crizotinib (PF-02341066) '
                u'demonstrated impressive antitumor activity in the majority '
                u'of patients with NSCLC harboring ALK fusions. However, '
                u'despite these remarkable initial responses, cancers e'
                u'ventually develop resistance to crizotinib, usually '
                u'within 1 y, thereby limiting the potential clinical benefit. '
                u'To determine how cancers acquire resistance to ALK inhibitors, '
                u'we established a model of acquired resistance to crizotinib by '
                u'exposing a highly sensitive EML4-ALK-positive NSCLC cell line to '
                u'increasing doses of crizotinib until resistance emerged. We found'
                u' that cells resistant to intermediate doses of crizotinib developed '
                u'amplification of the EML4-ALK gene. Cells resistant to higher doses '
                u'(1 μM) also developed a gatekeeper mutation, L1196M, within the kinase'
                u' domain, rendering EML4-ALK insensitive to crizotinib. This gatekeeper '
                u'mutation was readily detected using a unique and highly sensitive '
                u'allele-specific PCR assay. Although crizotinib was ineffectual '
                u'against EML4-ALK harboring the gatekeeper mutation, we observed '
                u'that two structurally different ALK inhibitors, NVP-TAE684 and '
                u'AP26113, were highly active against the resistant cancer cells '
                u'in vitro and in vivo. Furthermore, these resistant cells remained'
                u' highly sensitive to the Hsp90 inhibitor 17-AAG. Thus, we have '
                u'developed a model of acquired resistance to ALK inhibitors and have '
                u'shown that second-generation ALK TKIs or Hsp90 inhibitors are effective in '
                u'treating crizotinib-resistant tumors harboring secondary gatekeeper '
                u'mutations.')

# THIS SEEMS TO BE MUCH, MUCH FASTER but i'll post speed testing later this weekend

import spacy
nlp = spacy.load('en')

doc = nlp(u'The echinoderm microtubule-associated protein-like 4 '
                u'(EML4)-anaplastic lymphoma kinase (ALK) fusion oncogene '
                u'represents a molecular target in a small subset of non-small'
                u' cell lung cancers (NSCLCs). This fusion leads to '
                u'constitutive ALK activation with potent transforming '
                u'activity. In a pivotal phase 1 clinical trial, the ALK '
                u'tyrosine kinase inhibitor (TKI) crizotinib (PF-02341066) '
                u'demonstrated impressive antitumor activity in the majority '
                u'of patients with NSCLC harboring ALK fusions. However, '
                u'despite these remarkable initial responses, cancers e'
                u'ventually develop resistance to crizotinib, usually '
                u'within 1 y, thereby limiting the potential clinical benefit. '
                u'To determine how cancers acquire resistance to ALK inhibitors, '
                u'we established a model of acquired resistance to crizotinib by '
                u'exposing a highly sensitive EML4-ALK-positive NSCLC cell line to '
                u'increasing doses of crizotinib until resistance emerged. We found'
                u' that cells resistant to intermediate doses of crizotinib developed '
                u'amplification of the EML4-ALK gene. Cells resistant to higher doses '
                u'(1 μM) also developed a gatekeeper mutation, L1196M, within the kinase'
                u' domain, rendering EML4-ALK insensitive to crizotinib. This gatekeeper '
                u'mutation was readily detected using a unique and highly sensitive '
                u'allele-specific PCR assay. Although crizotinib was ineffectual '
                u'against EML4-ALK harboring the gatekeeper mutation, we observed '
                u'that two structurally different ALK inhibitors, NVP-TAE684 and '
                u'AP26113, were highly active against the resistant cancer cells '
                u'in vitro and in vivo. Furthermore, these resistant cells remained'
                u' highly sensitive to the Hsp90 inhibitor 17-AAG. Thus, we have '
                u'developed a model of acquired resistance to ALK inhibitors and have '
                u'shown that second-generation ALK TKIs or Hsp90 inhibitors are effective in '
                u'treating crizotinib-resistant tumors harboring secondary gatekeeper '
                u'mutations.')

for word in doc:
    print(word.text, word.lemma, word.lemma_)

# STEMMING ALGORITHMS TO TRY
# 1) Porter Algorithm
# 2) Lancaster Algorithm
# 3) Snowball Algorithm

# But I'm gonna write my own biolemmatization scheme based on medical text training anyways
