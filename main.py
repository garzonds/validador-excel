"""
Automatización de validación de Excel
--------------------------------------
Uso:
    python main.py --input datos.xlsx
    python main.py --input datos.xlsx --rules config/rules.json --output output/reporte.xlsx
"""
import argparse
import json
import sys
from pathlib import Path

from modules.loader    import load_excel
from modules.validator import apply_rules
from modules.reporter  import generate_report


def main():
    parser = argparse.ArgumentParser(description="Validador de Excel con reglas configurables")
    parser.add_argument("--input",  required=True,  nargs="+",              help="Ruta al Excel de entrada")
    parser.add_argument("--rules",  default="config/rules.json", nargs="+", help="Ruta al archivo de reglas")
    parser.add_argument("--output", default="output/reporte_validado.xlsx", nargs="+", help="Ruta del reporte de salida")
    args = parser.parse_args()

    input_path  = Path(" ".join(args.input))
    rules_path  = Path(" ".join(args.rules)  if isinstance(args.rules,  list) else args.rules)
    output_path = Path(" ".join(args.output) if isinstance(args.output, list) else args.output)

    # Validaciones de rutas
    if not input_path.exists():
        print(f"❌ No se encontró el archivo: {input_path}")
        sys.exit(1)
    if not rules_path.exists():
        print(f"❌ No se encontró el archivo de reglas: {rules_path}")
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Leer configuración para obtener output_column
    with open(rules_path, encoding="utf-8") as f:
        config = json.load(f)
    out_col = config["output_column"]

    print(f"📂 Cargando: {input_path}")
    df = load_excel(str(input_path))
    print(f"   → {len(df)} filas encontradas")

    print("⚙️  Aplicando reglas...")
    df_result = apply_rules(df, str(rules_path))

    # Mini resumen en consola
    print(f"\n📊 Resultado de la clasificación ({out_col}):")
    for val, cnt in df_result[out_col].value_counts().items():
        pct = cnt / len(df_result) * 100
        print(f"   {val}: {cnt} ({pct:.1f}%)")

    print(f"\n📝 Generando reporte en: {output_path}")
    generate_report(df_result, out_col, str(output_path))


if __name__ == "__main__":
    main()
