# Validador de Excel — Interfaz Web Local

## Instalación (solo la primera vez)

```bash
pip install flask pandas openpyxl
```

## Cómo arrancar

```bash
cd proyecto
python app.py
```

Luego abre tu navegador en: **http://localhost:5000**

## Uso

1. Arrastra o selecciona tu archivo Excel (.xlsx)
2. Presiona **Ejecutar validación**
3. Ve el resumen de resultados
4. Presiona **Descargar reporte Excel**

## Configurar reglas

Edita el archivo `config/rules.json`:

```json
{
  "output_column": "Clasificacion",
  "rules": [
    {
      "conditions": [
        {"column": "Nombre", "operator": "==", "value": "David"},
        {"column": "Edad",   "operator": "==", "value": 22}
      ],
      "logic": "AND",
      "result": "Joven"
    }
  ],
  "default_result": "No Joven"
}
```

Operadores disponibles: `==`, `!=`, `>`, `<`, `>=`, `<=`, `contains`
Lógica: `AND` / `OR`
