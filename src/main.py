import os
from tqdm import tqdm


from src.csv_handler.csv_handler import CSVHandler
from src.llm_manager.llm_config import LLMConfig
from src.llm_manager.llm_factory import LLMFactory
from src.llm_tasks.radiology_report_extractor import RadiologyReportStructuredDataExtractor

if __name__ == "__main__":

    current_dir = os.path.dirname(os.path.abspath(__file__))

    radiology_reports_csv_path = os.path.join(current_dir, "..", "data_source", "ReportsDATASET.csv")
    save_path = os.path.join(current_dir, "..", "data_output", "ReportsDATASET_processed_v5")

    reports = CSVHandler.read_csv(radiology_reports_csv_path)

    llm_config = LLMConfig(
        provider=None,
        temperature=0.1,
        max_tokens=4,
        base_url="http://localhost:5001/v1/"
    )

    llm = LLMFactory.create_llm(llm_config)

    report_classifier = RadiologyReportStructuredDataExtractor(llm)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    for report in tqdm(reports, desc="Processing reports"):
        extracted_pe_data = report_classifier.extract_pe_data(report)
        extracted_lung_abnormality_data = report_classifier.extract_lung_abnormality_data(report)
        CSVHandler.write_to_csv(extracted_pe_data, (save_path + "_pe_data.csv"), "pe")
        CSVHandler.write_to_csv(extracted_lung_abnormality_data, (save_path + "_lung_abnormality.csv"), "lung_abnormality")

