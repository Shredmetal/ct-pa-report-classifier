# Radiology Report Extraction System

This repository contains the source code for a system designed to extract structured clinical data from unstructured radiology reports.

# Usage

It is currently a work-in-progress, however, the intention is for this to run using local inference with ease of set-up being the primary design goal.

Therefore, it is designed to connect to a kobold.cpp backend for inference, which handles the model and exposes an OpenAI v1 Completions API.

The `base_url` is currently set in `src/main.py`.

The system reads in a 1-column csv from `root/data_source` and writes to `root/data_output`.

Please refer to `src/csv_handler/csv_handler.py` for how reports are ingested. 

Further functionality relating to lung abnormalities and a frontend and in the process of being implemented.