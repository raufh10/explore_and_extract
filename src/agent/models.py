from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

class ElementAttribute(BaseModel):
  """Strictly defined key-value pair for HTML attributes."""
  model_config = ConfigDict(extra="forbid") 
  name: str = Field(description="The attribute name (e.g., 'href')")
  value: str = Field(
    description="The attribute value pattern. Use placeholders like '{value}' for dynamic data."
  )

class Element(BaseModel):
  model_config = ConfigDict(populate_by_name=True, extra="forbid")

  tag: str = Field(
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
  attributes: List[ElementAttribute] = Field(
    default_factory=list,
    description="List of other attributes. Required for strict mode instead of a dict.",
  )
  description: Optional[str] = Field(
    default=None,
    description="A brief explanation of what this element represents (e.g., 'Book Title Container')."
  )

class Elements(BaseModel):
  model_config = ConfigDict(extra="forbid")
  elements: List[Element] = Field(
    description="A list of unique element templates representing the blueprint for extraction. Avoid duplicate patterns.",
  )

