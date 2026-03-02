import json
import operator
import pandas as pd

OPS = {
    "==":       operator.eq,
    "!=":       operator.ne,
    ">":        operator.gt,
    "<":        operator.lt,
    ">=":       operator.ge,
    "<=":       operator.le,
    "contains": lambda a, b: str(b).lower() in str(a).lower(),
}

def _eval_condition(row, condition: dict) -> bool:
    col   = condition["column"]
    op    = condition["operator"]
    value = condition["value"]
    if col not in row:
        raise KeyError(f"Columna '{col}' no encontrada en el Excel.")
    cell_val = row[col]
    # Intentar castear el value al mismo tipo que la celda
    try:
        if isinstance(cell_val, (int, float)):
            value = type(cell_val)(value)
    except (ValueError, TypeError):
        pass
    return OPS[op](cell_val, value)

def _eval_rule(row, rule: dict) -> bool:
    conditions = rule["conditions"]
    logic      = rule.get("logic", "AND").upper()
    results    = [_eval_condition(row, c) for c in conditions]
    return all(results) if logic == "AND" else any(results)

def apply_rules(df: pd.DataFrame, rules_path: str) -> pd.DataFrame:
    with open(rules_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    out_col  = config["output_column"]
    rules    = config["rules"]
    default  = config["default_result"]

    def classify(row):
        for rule in rules:
            if _eval_rule(row, rule):
                return rule["result"]
        return default

    df = df.copy()
    df[out_col] = df.apply(classify, axis=1)
    return df
