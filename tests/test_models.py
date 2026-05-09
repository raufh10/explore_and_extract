from agent.models import Element, Elements


def test_element_accepts_class_alias() -> None:
  element = Element.model_validate({
    "tag": "a",
    "class": "product-link",
    "id": "product-1",
    "other_attrs": {"href": "/products/1"},
  })

  assert element.css_class == "product-link"
  assert element.model_dump(by_alias=True, exclude_none=True) == {
    "tag": "a",
    "class": "product-link",
    "id": "product-1",
    "other_attrs": {"href": "/products/1"},
  }


def test_element_uses_defaults() -> None:
  element = Element()

  assert element.tag == "div"
  assert element.css_class is None
  assert element.id is None
  assert element.other_attrs == {}


def test_elements_wraps_flat_element_list() -> None:
  elements = Elements(elements=[
    Element(tag="p", css_class="price_color"),
    Element(tag="span", css_class="availability"),
  ])

  assert elements.model_dump(by_alias=True, exclude_none=True) == {
    "elements": [
      {"tag": "p", "class": "price_color", "other_attrs": {}},
      {"tag": "span", "class": "availability", "other_attrs": {}},
    ]
  }
