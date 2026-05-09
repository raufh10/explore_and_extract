from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class Element(BaseModel):
  model_config = ConfigDict(populate_by_name=True)

  tag: str = Field(
    default="div",
    description="The HTML tag name (e.g., 'div', 'h1', 'a').",
  )

  css_class: Optional[str] = Field(
    default=None,
    alias="class",
    description="The CSS class string (e.g., 'product-title').",
  )

  id: Optional[str] = Field(
    default=None,
    description="The unique HTML ID attribute.",
  )

  other_attrs: Dict[str, str] = Field(
    default_factory=dict,
    description="Other attributes like 'href' or 'data-id'.",
  )
