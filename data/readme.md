This directory is for echr data.

The data is downloaded from Open-echr on 25.04.2024.

The data utilized is the files with the name echr_2_0_0_unstructured_cases.json and echr_2_0_0_structured_cases.

The code for processing the data is in transform-echr.py

The processed data is structred that each case is in a separate json file with the name of the case id, for ex: 001-57416.json.

The information each case file has is:

    - meta-data:
        - 'itemid'
        - 'importance'
        - 'judgementdate'

    - case text data:
        - 'law'
        - 'procedure'
        - 'abbreviations'
        - 'appendix'
        - 'other'
        - 'opinion'
        - 'toc'
        - 'submission'
        - 'schedule'
        - 'relevant_law'
        - 'facts'
        - 'introduction'
        - 'conclusion'
