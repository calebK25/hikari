import typer, pathlib, json
from .ocr import ocr_pdf

app = typer.Typer()

@app.command()
def add(file: str):
    path = pathlib.Path(file)
    if path.suffix.lower() == ".pdf":
        pages = ocr_pdf(str(path))
        out = path.with_suffix(".jsonl")
        with out.open("w") as f:
            for p in pages:
                f.write(json.dumps(p) + "\n")
        typer.echo(f"Saved → {out}")
    else:
        typer.echo("Only PDF files are supported.")

if __name__ == "__main__":
    app()