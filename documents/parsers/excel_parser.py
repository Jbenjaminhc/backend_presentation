import pandas as pd
from io import BytesIO
import logging
import json
import numpy as np

logger = logging.getLogger(__name__)


# Helper para serializar tipos de NumPy a tipos Python nativos
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def extract_data_from_xlsx(file):
    """
    Extrae datos y estructura de un archivo Excel

    Args:
        file: Objeto archivo Excel

    Returns:
        dict: Diccionario con hojas, tablas y datos para gráficos
    """
    result = {
        'sheets': [],
        'tables': [],
        'chart_data': []
    }

    try:
        # Manejar diferentes tipos de entrada
        if hasattr(file, 'read'):
            file_content = file.read()
            excel_file = BytesIO(file_content)
        else:
            excel_file = BytesIO(file)

        # Leer todas las hojas
        excel = pd.ExcelFile(excel_file)
        sheet_names = excel.sheet_names

        for sheet_name in sheet_names:
            df = pd.read_excel(excel, sheet_name=sheet_name)

            # Convertir DataFrame a formato para tablas
            headers = df.columns.tolist()
            data = df.values.tolist()

            # Detectar posibles datos para gráficos (columnas numéricas)
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            if len(numeric_columns) > 0 and len(df) > 0:
                # Primera columna como potencial eje X
                x_column = df.columns[0]

                for y_column in numeric_columns:
                    # Skip if it's the same as x_column
                    if y_column == x_column:
                        continue

                    chart_data = {
                        'sheet': sheet_name,
                        'title': f"{y_column} vs {x_column}",
                        'type': 'line',  # Default chart type
                        'x_axis': {
                            'label': x_column,
                            'data': df[x_column].tolist()
                        },
                        'y_axis': {
                            'label': y_column,
                            'data': df[y_column].tolist()
                        }
                    }

                    result['chart_data'].append(chart_data)

            # Agregar información de la hoja
            result['sheets'].append({
                'name': sheet_name,
                'headers': headers,
                'data': data,
                'row_count': len(df),
                'column_count': len(headers)
            })

            # Agregar la hoja como una tabla
            result['tables'].append({
                'sheet': sheet_name,
                'headers': headers,
                'data': json.loads(json.dumps(data, cls=NpEncoder))
            })

        return result

    except Exception as e:
        logger.error(f"Error extracting data from Excel: {str(e)}")
        result['error'] = str(e)
        return result