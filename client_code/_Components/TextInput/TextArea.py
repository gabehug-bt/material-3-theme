import anvil.server
from . import TextInput
import anvil.designer
import anvil.js
from anvil.js.window import ResizeObserver, requestAnimationFrame
from ...utils.properties import get_unset_value, anvil_prop, italic_property, bold_property, underline_property, font_family_property, font_size_property, color_property, style_property

text_property = {
  "name": "text",
  "type": "string",
  "default_value": "None",
  "description": "The input text displayed on this component",
  "supportsWriteback": True,
  "important": True
}

height_property = {"name": "height",
                   "type": "number",
                   "default_value": None,
                   "description": "The initial height of this TextArea",}

class TextArea(TextInput):
  _anvil_properties_ = [text_property, height_property, *TextInput._anvil_properties_]
  
  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)
    hiddenInput = self.dom_nodes['anvil-m3-textbox']
    self.dom_nodes['anvil-m3-input-container'].removeChild(hiddenInput)

    self._on_change = self._on_change
    self._on_focus = self._on_focus
    self._on_lost_focus = self._on_lost_focus

    self.dom_nodes['anvil-m3-textarea'].addEventListener("input", self._expand_to_fit_content)
    self.dom_nodes['anvil-m3-textarea'].addEventListener("input", self._on_input)
    self.dom_nodes['anvil-m3-textarea'].addEventListener("change", self._on_change)
    self.dom_nodes['anvil-m3-textarea'].addEventListener("focus", self._on_focus)
    self.dom_nodes['anvil-m3-textarea'].addEventListener("blur", self._on_lost_focus)

    self.add_event_handler("x-anvil-page-added", self._on_mount)
    self.add_event_handler("x-anvil-page-removed", self._on_cleanup)

  def _on_mount(self, **event_args):
    self.resize_observer = ResizeObserver(self._on_resize)
    self.resize_observer.observe(self.dom_nodes['anvil-m3-textarea'])
    
  def _on_cleanup(self, **event_args):
    self.resize_observer.unobserve(self.dom_nodes['anvil-m3-textarea'])

  def _anvil_get_unset_property_values_(self):
    common_props = TextInput._get_common_unset_property_values_(self)
    common_props['display_font_size'] = get_unset_value(self.dom_nodes['anvil-m3-textarea'], "fontSize", self.display_font_size)
    return common_props

  def _expand_to_fit_content(self, event):
    if event.target.scrollHeight > event.target.clientHeight:
      self.dom_nodes['anvil-m3-textarea'].style.height = '56px' #Min-height based off M3 specs
      self._set_height(event.target.scrollHeight)

  def _on_resize(self, entries, observer):
    for entry in entries:
      h = entry.target.scrollHeight
    requestAnimationFrame(lambda _: self._set_height(h))

  def _set_height(self, h):
    # Keep this function, because it's easier to call it from a lambda than setting the height property.
    self.dom_nodes['anvil-m3-textarea'].style.height = f'{h}px'
    self.dom_nodes['anvil-m3-border-container'].style.height = f"{self.dom_nodes['anvil-m3-textarea'].clientHeight}px"

  def _set_id(self, value):
    super()._set_id(value)
    self.dom_nodes["anvil-m3-textarea"].id = value

  def focus(self):
    self.dom_nodes['anvil-m3-textarea'].focus()

  def select(self):
    self.dom_nodes['anvil-m3-textarea'].select()
  
  display_italic = italic_property('anvil-m3-textarea', 'display_italic')
  display_bold = bold_property('anvil-m3-textarea', 'display_bold')
  display_underline = underline_property('anvil-m3-textarea', 'display_underline')
  display_font_size = font_size_property('anvil-m3-textarea', 'display_font_size')
  display_font = font_family_property('anvil-m3-textarea', 'display_font')
  text_color = color_property('anvil-m3-textarea', 'color', 'text_color')
  background = color_property('anvil-m3-textarea', 'backgroundColor', 'background')
  align = style_property('anvil-m3-textarea', 'textAlign', 'align')

  @anvil_prop
  def placeholder(self, value):
    input = self.dom_nodes['anvil-m3-textarea']
    if value:
      input.placeholder = value
      input.classList.add('anvil-m3-has-placeholder')
    else:
      input.placeholder = " "
      input.classList.remove('anvil-m3-has-placeholder')

  @anvil_prop
  def label(self, value):
    self.dom_nodes['anvil-m3-label-text'].innerText = value or ""
    if value:
      self.dom_nodes['anvil-m3-textarea'].classList.toggle('has_label_text', True)
    else:
      self.dom_nodes['anvil-m3-textarea'].classList.toggle('has_label_text', anvil.designer.in_designer)

  @property
  def text(self):
    return self.dom_nodes['anvil-m3-textarea'].value

  @text.setter
  def text(self, value):
    self.dom_nodes['anvil-m3-textarea'].value = value

  @anvil_prop
  def enabled(self, value):
    supporting_text = self.dom_nodes['anvil-m3-subcontent']
    if value:
      self.dom_nodes['anvil-m3-textarea'].removeAttribute("disabled")
      supporting_text.classList.remove("anvil-m3-textinput-disabled")
    else:
      self.dom_nodes['anvil-m3-textarea'].setAttribute("disabled", " ")
      supporting_text.classList.add("anvil-m3-textinput-disabled")

  @property
  def height(self):
    return self.dom_nodes['anvil-m3-textarea'].scrollHeight

  @height.setter
  def height(self, value):
    self._set_height(value)

  @anvil_prop
  def character_limit(self, value):
    if value is None or value < 1:
      text_area_input = self.dom_nodes['anvil-m3-textarea'].removeAttribute("maxlength")
      self.dom_nodes['anvil-m3-character-counter'].style = "display: none"
    else:
      text_area_input = self.dom_nodes['anvil-m3-textarea'].setAttribute("maxlength", value)
      self.dom_nodes['anvil-m3-character-counter'].style = "display: inline";
      self.dom_nodes['anvil-m3-character-limit'].innerText = int(value);

  def _anvil_get_interactions_(self):
    
    def on_grab(x,y):
      self._grab_height = self.height

    def on_drag(dx, dy, ctrl):
      self.height = self._grab_height + dy

    def on_drop(dx, dy):
      h = self._grab_height + dy
      self.height = h
      anvil.designer.update_component_properties(self, {"height": h})
    
    return [
      {
        "type": "handle",
        "position": "bottom",
        "direction": "y",
        "callbacks": {
          "grab": on_grab,
          "drag": on_drag,
          "drop": on_drop,
        },
      }
    ]  

  #!componentProp(material_3.TextArea)!1: {name:"align",type:"enum",options:["left", "right", "center"],description:"The position of this component in the available space."} 
  #!componentProp(material_3.TextArea)!1: {name:"appearance",type:"enum",options:["filled", "outlined"],description:"A predefined style for this component."}  
  #!componentProp(material_3.TextArea)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."} 
  #!componentProp(material_3.TextArea)!1: {name:"enabled",type:"boolean",description:"If True, this component allows user interaction."}
  #!componentProp(material_3.TextArea)!1: {name:"error",type:"boolean",description:"If True, this component is in an error state."}
  #!componentProp(material_3.TextArea)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles"}

  #!componentProp(material_3.TextArea)!1: {name:"label_color",type:"color",description:"The colour of the label text on the component."} 
  #!componentProp(material_3.TextArea)!1: {name:"label",type:"string",description:"The label text of the component."} 
  #!componentProp(material_3.TextArea)!1: {name:"label_font_family",type:"string",description:"The font family to use for the label on this component."}
  #!componentProp(material_3.TextArea)!1: {name:"label_font_size",type:"number",description:"The font size of the label text on this component."}
  #!componentProp(material_3.TextArea)!1: {name:"label_underline",type:"boolean",description:"If True, the label text will be underlined."}
  #!componentProp(material_3.TextArea)!1: {name:"label_italic",type:"boolean",description:"If True, the label text will be italic."}
  #!componentProp(material_3.TextArea)!1: {name:"bold_label",type:"boolean",description:"If True, the label text will be bold."}

  #!componentProp(material_3.TextArea)!1: {name:"text_color",type:"color",description:"The colour of the input text displayed on this component."}
  #!componentProp(material_3.TextArea)!1: {name:"display_font_family",type:"string",description:"The font family to use for the input and placeholder text."}
  #!componentProp(material_3.TextArea)!1: {name:"display_font_size",type:"number",description:"The font size of the input and placeholder text."}
  #!componentProp(material_3.TextArea)!1: {name:"display_underline",type:"boolean",description:"The font family to use for the label on this component."}
  #!componentProp(material_3.TextArea)!1: {name:"display_italic",type:"boolean",description:"If True, the input and placeholder text will be italic."}
  #!componentProp(material_3.TextArea)!1: {name:"display_bold",type:"boolean",description:"If True, the input and placeholder text will be bold."}

  #!componentProp(material_3.TextArea)!1: {name:"supporting_text",type:"string",description:"The supporting text displayed underneath this component"}
  #!componentProp(material_3.TextArea)!1: {name:"character_limit",type:"number",description:"The max number of characters a user can enter into this component. The limit is displayed below the component."}
  #!componentProp(material_3.TextArea)!1: {name:"subcontent_color",type:"color",description:"The colour of the supporting text and the character limit underneath this component."}
  #!componentProp(material_3.TextArea)!1: {name:"subcontent_font_family",type:"color",description:"The font family to use for the supporting text and the character limit underneath this component."}
  #!componentProp(material_3.TextArea)!1: {name:"subcontent_font_size",type:"color",description:"The font size of the supporting text and the character limit displayed underneath this component."}

  #!componentProp(material_3.TextArea)!1: {name:"background_color",type:"color",description:"The colour of the background of this component."}
  #!componentProp(material_3.TextArea)!1: {name:"border_color",type:"color",description:"The colour of the border of this component."}
  #!componentProp(material_3.TextArea)!1: {name:"placeholder",type:"string",description:"The text to be displayed when the component is empty"}

  #!componentProp(material_3.TextArea)!1: {name:"margin",type:"margin",description:"The margin of this component. Default value is in pixels."}
  #!componentProp(material_3.TextArea)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
  #!componentProp(material_3.TextArea)!1: {name:"text",type:"string",description:"The input text to display on this component"}
  #!componentProp(material_3.TextArea)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}

  #!componentEvent(material_3.TextArea)!1: {name: "change", description: "When the text in this component is edited.", parameters:[]}
  #!componentEvent(material_3.TextArea)!1: {name: "focus", description: "When the component gets focus.", parameters:[]}
  #!componentEvent(material_3.TextArea)!1: {name: "lost_focus", description: "When the component loses focus.", parameters:[]}

  #!componentEvent(material_3.TextArea)!1: {name: "change", description: "When the text in this component is edited.", parameters:[]}
  #!componentEvent(material_3.TextArea)!1: {name: "focus", description: "When the component gets focus.", parameters:[]}
  #!componentEvent(material_3.TextArea)!1: {name: "lost_focus", description: "When the component loses focus.", parameters:[]}

  #!defMethod(_)!2: "Set the keyboard focus to this TextArea." ["focus"]
  #!defMethod(_)!2: "Set the input text on this TextArea." ["select"]

#!defClass(material_3,TextArea, anvil.Component)!:
