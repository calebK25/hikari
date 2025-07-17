from prefect import flow, task
import subprocess

@task
def run_eval():
    subprocess.run(["python", "src/eval/qa_eval.py"], check=True)

@flow(name="daily-eval")
def daily_eval():
    run_eval()

if __name__ == "__main__":
    daily_eval()