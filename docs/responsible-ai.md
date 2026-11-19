# Responsible AI and Limitations

               ## Human Oversight

               The system is designed to assist recruiters, not replace them.
               A human recruiter must review candidates before making
               shortlisting or rejection decisions.

               ## Current Limitations

               - Skill extraction uses a manually maintained skill dictionary.
               - API skill matching uses substring matching.
               - Experience extraction relies on regular expressions.
               - Education extraction recognizes a limited list of qualifications.
               - Resume formatting can affect text extraction.
               - Semantic similarity may not capture every job requirement.
               - The ranking model has not been validated on a large,
                 representative real-world dataset.

                 ## Evaluation Caution

                 The initial evaluation used only three synthetic candidates.
                 The reported ROC-AUC and PR-AUC of 1.0 are illustrative
                 and do not establish real-world accuracy or fairness.

                 ## Fairness and Privacy

                 - Do not use protected characteristics to rank candidates.
                 - Avoid collecting unnecessary personal information.
                 - Restrict access to resumes and candidate records.
                 - Obtain appropriate consent before processing resumes.
                 - Regularly review ranking outcomes for potential bias.

                 ## Intended Use

                 Use rankings as decision-support information only.
                 Recruiters remain responsible for all hiring decisions.
