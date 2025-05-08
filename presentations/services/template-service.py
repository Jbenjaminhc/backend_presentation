import json
import os

# Definición de temas predeterminados
DEFAULT_THEMES = {
    "professional": {
        "name": "Professional",
        "colors": {
            "primary": "#1976D2",
            "secondary": "#455A64",
            "accent": "#FFC107",
            "background": "#FFFFFF",
            "text": "#333333"
        },
        "fonts": {
            "title": "Roboto",
            "heading": "Roboto",
            "body": "Open Sans"
        },
        "spacing": {
            "margin": "24px",
            "padding": "16px"
        }
    },
    "creative": {
        "name": "Creative",
        "colors": {
            "primary": "#FF5722",
            "secondary": "#9C27B0",
            "accent": "#8BC34A",
            "background": "#FAFAFA",
            "text": "#212121"
        },
        "fonts": {
            "title": "Montserrat",
            "heading": "Montserrat",
            "body": "Roboto"
        },
        "spacing": {
            "margin": "32px",
            "padding": "24px"
        }
    },
    "minimalist": {
        "name": "Minimalist",
        "colors": {
            "primary": "#212121",
            "secondary": "#757575",
            "accent": "#2196F3",
            "background": "#FFFFFF",
            "text": "#212121"
        },
        "fonts": {
            "title": "Lato",
            "heading": "Lato",
            "body": "Lato"
        },
        "spacing": {
            "margin": "24px",
            "padding": "16px"
        }
    }
}

# Plantillas de diapositivas predefinidas
SLIDE_TEMPLATES = {
    "title": {
        "name": "Diapositiva de título",
        "structure": {
            "title": {
                "type": "text",
                "placeholder": "Título de la presentación",
                "fontSize": "42px",
                "align": "center"
            },
            "subtitle": {
                "type": "text",
                "placeholder": "Subtítulo o autor",
                "fontSize": "24px",
                "align": "center"
            }
        }
    },
    "title_content": {
        "name": "Título y contenido",
        "structure": {
            "title": {
                "type": "text",
                "placeholder": "Título de la diapositiva",
                "fontSize": "36px",
                "align": "left"
            },
            "content": {
                "type": "text_block",
                "placeholder": "Contenido de la diapositiva...",
                "fontSize": "20px",
                "align": "left"
            }
        }
    },
    "title_two_columns": {
        "name": "Título y dos columnas",
        "structure": {
            "title": {
                "type": "text",
                "placeholder": "Título de la diapositiva",
                "fontSize": "36px",
                "align": "left"
            },
            "column_left": {
                "type": "text_block",
                "placeholder": "Contenido de la columna izquierda...",
                "fontSize": "20px",
                "align": "left"
            },
            "column_right": {
                "type": "text_block",
                "placeholder": "Contenido de la columna derecha...",
                "fontSize": "20px",
                "align": "left"
            }
        }
    },
    "title_image": {
        "name": "Título e imagen",
        "structure": {
            "title": {
                "type": "text",
                "placeholder": "Título de la diapositiva",
                "fontSize": "36px",
                "align": "left"
            },
            "image": {
                "type": "image",
                "placeholder": "Imagen",
                "width": "70%",
                "height": "auto",
                "align": "center"
            },
            "caption": {
                "type": "text",
                "placeholder": "Descripción de la imagen",
                "fontSize": "16px",
                "align": "center"
            }
        }
    },
    "chart": {
        "name": "Gráfico con título",
        "structure": {
            "title": {
                "type": "text",
                "placeholder": "Título del gráfico",
                "fontSize": "36px",
                "align": "left"
            },
            "chart": {
                "type": "chart",
                "chart_type": "bar",
                "width": "80%",
                "height": "400px",
                "align": "center"
            },
            "description": {
                "type": "text",
                "placeholder": "Descripción del gráfico",
                "fontSize": "18px",
                "align": "left"
            }
        }
    }
}

def get_available_themes():
    """Devuelve los temas disponibles"""
    return DEFAULT_THEMES

def get_theme_by_name(theme_name):
    """Obtiene un tema específico por nombre"""
    return DEFAULT_THEMES.get(theme_name, DEFAULT_THEMES["professional"])

def get_slide_templates():
    """Devuelve las plantillas de diapositivas disponibles"""
    return SLIDE_TEMPLATES

def get_template_by_name(template_name):
    """Obtiene una plantilla específica por nombre"""
    return SLIDE_TEMPLATES.get(template_name, SLIDE_TEMPLATES["title_content"])

def apply_theme_to_presentation(presentation, theme_name):
    """Aplica un tema a una presentación"""
    theme = get_theme_by_name(theme_name)
    presentation.theme = theme
    presentation.save()
    return presentation