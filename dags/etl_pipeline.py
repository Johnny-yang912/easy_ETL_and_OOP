from __future__ import annotations
from airflow.decorators import dag, task
from datetime import datetime
from src.pipeline import extract, transform, load

PARAMS = {
    "src_csv": "/opt/airflow/data/input.csv",
    "raw_csv": "/opt/airflow/data/raw.csv",
    "out_csv": "/opt/airflow/data/new.csv",
    "sqlite_path": "/opt/airflow/db/pipeline_etl.db",
    "table": "data",
    "datetime_col": "ts",
}

@dag(
    dag_id="etl_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,          # 需要時改成 "@daily" 等
    catchup=False,
    tags=["demo", "etl"],
)
def etl_pipeline():

    @task(task_id="extract")
    def extract_task(cfg: dict) -> str:
        # 回傳 raw_csv 路徑字串（可做 XCom）
        return extract(cfg["src_csv"], cfg["raw_csv"])

    @task(task_id="transform")
    def transform_task(raw_csv: str, cfg: dict) -> str:
        # 回傳 out_csv 路徑字串
        return transform(raw_csv, cfg["out_csv"], datetime_col=cfg["datetime_col"])

    @task(task_id="load")
    def load_task(out_csv: str, cfg: dict) -> None:
        load(out_csv, cfg["sqlite_path"], cfg["table"])

    raw = extract_task(PARAMS)
    new = transform_task(raw, PARAMS)
    load_task(new, PARAMS)

dag = etl_pipeline()

