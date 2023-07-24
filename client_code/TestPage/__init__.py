from ._anvil_designer import TestPageTemplate
from anvil import *

class TestPage(TestPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_3_click(self, **event_args):
    """This method is called when the component is clicked"""
    alert("clicked button in elevated card")

