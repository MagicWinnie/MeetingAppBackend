import logging
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"
jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=True,
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_template(template_path: str, context: dict[str, Any] | None = None) -> str:
    """Render a template with Jinja2.

    Args:
        template_path: Path to the template relative to the templates directory
        context: Dictionary with variables to be inserted into the template

    Returns:
        Rendered template as a string
    """
    if context is None:
        context = {}

    try:
        template = jinja_env.get_template(template_path)
        return template.render(**context)
    except Exception as e:
        logger.exception("Error rendering template '%s': %s", template_path, str(e))
        raise ValueError(f"Error rendering template '{template_path}': {str(e)}") from e
