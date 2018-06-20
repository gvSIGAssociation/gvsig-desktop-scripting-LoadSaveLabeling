import gvsig

from gvsig import getResource
from gvsig.libs.formpanel import load_icon
from javax.swing import AbstractAction
from javax.swing import Action

from org.gvsig.tools.util import ToolsUtilLocator

from gvsig.commonsdialog import openFileDialog
from org.gvsig.tools import ToolsLocator

from gvsig.commonsdialog import filechooser
from gvsig.commonsdialog import OPEN_FILE
from java.io import FileOutputStream

from java.io import FileInputStream

def trace(msg):
  print "###> ", msg

class SaveLabelingAction(AbstractAction):

  def __init__(self):
    AbstractAction.__init__(self,"Save labeling")
    self.putValue(Action.ACTION_COMMAND_KEY, "SaveLabeling")
    self.putValue(Action.SMALL_ICON, load_icon(getResource(__file__,"saveLabeling.png")))
    self.putValue(Action.SHORT_DESCRIPTION, "Save labeling to a file")

  def actionPerformed(self,e=None):
    i18n = ToolsLocator.getI18nManager()
    panel = e.getSource()
    if not panel.isLabelingEnabled():
      return
    labeling = panel.getLabelingStrategy()
    if labeling == None:
      return
    layer = panel.getLayer()
    initialPath = None
    getFile = getattr(layer.getDataStore().getParameters(),"getFile",None)
    if getFile != None:
      initialPath=getFile().getParent()
    else:
      initialPath = ToolsUtilLocator.getFileDialogChooserManager().getLastPath("OPEN_LAYER_FILE_CHOOSER_ID", None)
    f = filechooser(
      OPEN_FILE,
      title=i18n.getTranslation("_Select_a_file_to_save_the_labeling"),
      initialPath=initialPath,
      multiselection=False,
      filter=("gvslab",)
    )
    if f==None :
      return
    trace("filename %s" % f)
    try:
      fos = FileOutputStream(f)
      persistenceManager = ToolsLocator.getPersistenceManager()
      persistenceManager.putObject(fos, labeling)
    finally:
      fos.close()
      
  def isEnabled(self):
    return True

class LoadLabelingAction(AbstractAction):

  def __init__(self):
    AbstractAction.__init__(self,"Load labeling")
    self.putValue(Action.ACTION_COMMAND_KEY, "LoadLabeling")
    self.putValue(Action.SMALL_ICON, load_icon(getResource(__file__,"loadLabeling.png")))
    self.putValue(Action.SHORT_DESCRIPTION, "Load labeling from a file")

  def actionPerformed(self,e=None):
    i18n = ToolsLocator.getI18nManager()
    panel = e.getSource()

    layer = panel.getLayer()
    initialPath = None
    getFile = getattr(layer.getDataStore().getParameters(),"getFile",None)
    if getFile != None:
      initialPath=getFile().getParent()
    else:
      initialPath = ToolsUtilLocator.getFileDialogChooserManager().getLastPath("OPEN_LAYER_FILE_CHOOSER_ID", None)
    f = filechooser(
      OPEN_FILE,
      title=i18n.getTranslation("_Select_a_file_to_load_the_labeling"),
      initialPath=initialPath,
      multiselection=False,
      filter=("gvslab",)
    )
    if f==None :
      return
    try:
      fis = FileInputStream(f)
      persistenceManager = ToolsLocator.getPersistenceManager()
      labeling = persistenceManager.getObject(fis)
    finally:
      fis.close()
    layer.setLabelingStrategy(labeling)
    panel.setLayer(layer)
    panel.setLabelingEnabled(True)
          
  def isEnabled(self):
    return True

def selfRegister():
  cfgActionsManager = ToolsUtilLocator.getConfigurableActionsMamager()
  cfgActionsManager.addConfigurableAction("labelingPropertiesPage",SaveLabelingAction())
  cfgActionsManager.addConfigurableAction("labelingPropertiesPage",LoadLabelingAction())
  
def main(*args):
  pass
  