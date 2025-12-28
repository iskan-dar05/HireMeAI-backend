from pdf2image import convert_from_path
from pathlib import Path

def generate_pdf_thumbnail(pdf_path: str, output_dir: str) -> str:
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)  # 🔹 ensure folder exists

    images = convert_from_path(pdf_path, dpi=150, first_page=1, last_page=1)
    img = images[0]
    img.thumbnail((400, 560))

    output_path = output_dir_path / (Path(pdf_path).stem + ".png")
    img.save(output_path, "PNG")

    return str(output_path)
