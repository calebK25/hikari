from prefect.server.schemas.schedules import CronSchedule
from src.flows.nightly_ingest import nightly_ingest_flow

if __name__ == "__main__":
    # Deploy the flow with nightly schedule (2 AM every day)
    nightly_ingest_flow.serve(
        name="hikari",
        schedule=CronSchedule(cron="0 2 * * *")  # 2 AM daily
    ) 