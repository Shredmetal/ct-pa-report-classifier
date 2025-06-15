import os
from tqdm import tqdm


from src.csv_handler.csv_handler import CSVHandler
from src.llm_manager.llm_config import LLMConfig
from src.llm_manager.llm_factory import LLMFactory
from src.llm_tasks.radiology_report_categoriser import RadiologyReportCategoriser

if __name__ == "__main__":

    current_dir = os.path.dirname(os.path.abspath(__file__))

    radiology_reports_csv_path = os.path.join(current_dir, "..", "data_source", "ReportsDATASET.csv")
    save_path = os.path.join(current_dir, "..", "data_output", "ReportsDATASET_processed_v5.csv")

    reports = CSVHandler.read_csv(radiology_reports_csv_path)

    llm_config = LLMConfig(
        provider=None,
        temperature=0.1,
        max_tokens=4,
        base_url="http://localhost:5001/v1/"
    )

    llm = LLMFactory.create_llm(llm_config)

    report_categoriser = RadiologyReportCategoriser(llm)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    for report in tqdm(reports, desc="Processing reports"):
        categorised_report = report_categoriser.categorise_report(report)
        CSVHandler.write_to_csv(categorised_report, save_path)

