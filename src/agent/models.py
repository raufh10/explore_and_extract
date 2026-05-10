from typing import List, Optional, Dict
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

class NetworkRequest(BaseModel):
  model_config = ConfigDict(extra="forbid")
  url: str = Field(description="The full target URL.")
  method: str = Field(description="HTTP Method (GET, POST, etc.)")
  headers: Dict[str, str] = Field(
    default_factory=dict, 
    description="Full request headers for Postman replication."
  )
  post_data: Optional[str] = Field(
    default=None, 
    description="The raw payload sent to the server (JSON or form data)."
  )
  resource_type: str = Field(description="Type: fetch, xhr, or document.")

class APIBlueprint(BaseModel):
  """Collection of discovered API endpoints."""
  model_config = ConfigDict(extra="forbid")
  endpoints: List[NetworkRequest] = Field(
    default_factory=list,
    description="List of discovered API requests that carry data."
  )
  summary: str = Field(
    description="Brief technical summary of the API's behavior."
  )

