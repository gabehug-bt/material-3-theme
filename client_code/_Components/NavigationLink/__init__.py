from ._anvil_designer import NavigationLinkTemplate
from anvil import *
import anvil.js
from ...Functions import color_property, role_property, tooltip_property, href_property, innerHTML_property, font_family_property, font_size_property, spacing_property, italic_property, bold_property, underline_property
import anvil.designer
from ...utils.properties import get_unset_value, get_unset_spacing, anvil_prop

class NavigationLink(NavigationLinkTemplate):
  def __init__(self, **properties):
    self.tag = ComponentTag()
    self._props = properties
    self._tooltip_node = None
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.dom_nodes['anvil-m3-navigation-link'].addEventListener("click", self._handle_click)
    self.add_event_handler("x-anvil-page-removed", self._on_cleanup)
    
  def _on_cleanup(self, **event_args):
    if anvil.designer.in_designer:
      anvil.designer.register_interaction(self, self.dom_nodes['anvil-m3-navigation-link'], 'dblclick', lambda x: anvil.designer.start_editing_form(self.navigate_to))

  def _handle_click(self, event):
    self.raise_event("click", event=event)
    if self.navigate_to:
      open_form(self.navigate_to)
      self.selected = True

  def _anvil_get_interactions_(self):
    return [{
        "type": "whole_component",
        "title": "Edit text",
        "icon": "edit",
        "default": True,
        "callbacks": {
          "execute": lambda: anvil.designer.start_inline_editing(self, "text", self.dom_nodes['anvil-m3-navigation-link-text'])
        }
      }]

  def _anvil_get_unset_property_values_(self):
    el = self.dom_nodes["anvil-m3-navigation-link-container"]
    sp = get_unset_spacing(el, el, self.spacing)
    tfs = get_unset_value(self.dom_nodes['anvil-m3-navigation-link-text'], "fontSize", self.font_size)
    ifs = get_unset_value(self.dom_nodes['anvil-m3-navigation-link-icon'], "fontSize", self.icon_size)
    return {"font_size": tfs, "icon_size": ifs, "spacing": sp}

  #!componentEvent(material_3.NavigationLink)!1: {name: "click", description: "When the NavigationLink is clicked."}
  #!componentEvent(material_3.NavigationLink)!1: {name: "show", description: "When the NavigationLink is shown on the screen."}
  #!componentEvent(material_3.NavigationLink)!1: {name: "hide", description: "When the NavigationLink is removed from the screen."}

  #!componentProp(material_3.NavigationLink)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."} 
  #!componentProp(material_3.NavigationLink)!1: {name:"text",type:"string",description:"The text displayed on this component."}
  #!componentProp(material_3.NavigationLink)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."} 
  #!componentProp(material_3.NavigationLink)!1: {name:"italic",type:"boolean",description:"If True, this component’s text will be italic."}
  #!componentProp(material_3.NavigationLink)!1: {name:"bold",type:"boolean",description:"If True, this component’s text will be bold."}
  #!componentProp(material_3.NavigationLink)!1: {name:"underline",type:"boolean",description:"If True, this component’s text will be underlined."}
  #!componentProp(material_3.NavigationLink)!1: {name:"text_color",type:"color",description:"The color of the text on the component."} 
  #!componentProp(material_3.NavigationLink)!1: {name:"icon_color",type:"color",description:"The color of the icon displayed on this component."}
  #!componentProp(material_3.NavigationLink)!1: {name:"font_family",type:"string",description:"The font family to use for this component."}
  #!componentProp(material_3.NavigationLink)!1: {name:"font_size",type:"number",description:"The font size of text displayed on this component."}
  #!componentProp(material_3.NavigationLink)!1: {name:"icon_size",type:"number",description:"The size (pixels) of the icon displayed on this component."}
  #!componentProp(material_3.NavigationLink)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
  #!componentProp(material_3.NavigationLink)!1: {name:"spacing",type:"spacing",description:"The margin and padding (pixels) of the component."}
  #!componentProp(material_3.NavigationLink)!1: {name:"url",type:"string",description:"TThe target URL of the link. Can be set to a URL string or to a Media object."}
  #!componentProp(material_3.NavigationLink)!1: {name:"icon",type:"enum",description:"The icon to display on this component."} 
  #!componentProp(material_3.NavigationLink)!1: {name:"selected",type:"boolean",description:"If True, the component is in the selected state."} 
  #!componentProp(material_3.NavigationLink)!1: {name:"badge",type:"boolean",description:"If True, display a notification badge on the icon."} 
  #!componentProp(material_3.NavigationLink)!1: {name:"badge_count",type:"number",description:"The number to display on the badge."} 
  #!componentProp(material_3.NavigationLink)!1: {name:"navigate_to",type:"form",description:"The Form to navigate to when the link is clicked."} 
  #!componentProp(material_3.NavigationLink)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}
  #!componentProp(material_3.NavigationLink)!1: {name:"background_color",type:"color",description:"The color of the background of this component."}

  visible = HtmlTemplate.visible
  text = innerHTML_property('anvil-m3-navigation-link-text')
  role = role_property('anvil-m3-navigation-link')
  italic = italic_property('anvil-m3-navigation-link-text')
  bold = bold_property('anvil-m3-navigation-link-text')
  underline = underline_property('anvil-m3-navigation-link-text')
  text_color = color_property('anvil-m3-navigation-link-text', 'color', 'text_color')
  icon_color = color_property('anvil-m3-navigation-link-icon', 'color', 'icon_color')
  font_family = font_family_property('anvil-m3-navigation-link-text')
  font_size = font_size_property('anvil-m3-navigation-link-text', 'font_size')
  icon_size = font_size_property('anvil-m3-navigation-link-icon', 'icon_size')
  tooltip = tooltip_property('anvil-m3-navigation-link-container')
  spacing = spacing_property('anvil-m3-navigation-link-container')
  background_color = color_property('anvil-m3-navigation-link-container', 'backgroundColor', 'background_color')
  navigate_to = anvil_prop("navigate_to")
  
  @anvil_prop
  def url(self, value):
    if value:
      self.dom_nodes['anvil-m3-navigation-link'].href = value
    else:
      self.dom_nodes['anvil-m3-navigation-link'].href = 'javascript:void(0)'

  @anvil_prop
  def icon(self, value):
    link_icon = self.dom_nodes['anvil-m3-navigation-link-icon']
    if value:
      link_icon.className = ""
      link_icon.classList.add("material-symbols-outlined")
      link_icon.innerText = value[3:]

  @anvil_prop
  def selected(self, value):
    if value:
      self.dom_nodes['anvil-m3-navigation-link'].classList.add('anvil-m3-navigation-link-selected')
    else:
      self.dom_nodes['anvil-m3-navigation-link'].classList.remove('anvil-m3-navigation-link-selected')

  @anvil_prop
  def badge(self, value):
    if value:
      self.dom_nodes['anvil-m3-navigation-link'].classList.add('anvil-m3-has-badge')
    else:
      self.dom_nodes['anvil-m3-navigation-link'].classList.remove('anvil-m3-has-badge')

  @anvil_prop
  def badge_count(self, value):
    if value and self.badge:
      self.dom_nodes['anvil-m3-icon-badge'].innerHTML = value
      self.dom_nodes['anvil-m3-icon-badge'].classList.add("anvil-m3-large-badge")
      self.dom_nodes['anvil-m3-navigation-drawer-icon-badge'].innerHTML = value
      self.dom_nodes['anvil-m3-navigation-drawer-icon-badge'].classList.add("anvil-m3-large-badge")
    else:
      self.dom_nodes['anvil-m3-icon-badge'].innerHTML = ""
      self.dom_nodes['anvil-m3-icon-badge'].classList.remove("anvil-m3-large-badge")
      self.dom_nodes['anvil-m3-navigation-drawer-icon-badge'].innerHTML = ""
      self.dom_nodes['anvil-m3-navigation-drawer-icon-badge'].classList.remove("anvil-m3-large-badge")

#!defClass(material_3, NavigationLink, anvil.Component)!:
