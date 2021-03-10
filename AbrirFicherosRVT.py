import clr
import sys
sys.path.append('C:\Program Files (x86)\IronPython 2.7\Lib')
import System
from System import Array
from System.Collections.Generic import *
clr.AddReference('ProtoGeometry')       #Es una biblioteca de Dynamo pensada para interactuar con geometría de Dynamo
from Autodesk.DesignScript.Geometry import *
clr.AddReference('RevitNodes')          #Carga los nodos de Dynamo, las bibliotecas de elementos de Revit en Dynamo y las conversiones geométricas
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)
clr.AddReference('RevitServices')       #Permite manejar los documentos y modificarlos a través del DocumentManager y el TransactionManager
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
clr.AddReference('RevitAPI')            #Agrega las clases que se encuentran en el archivo dll de la API de Revit
clr.AddReference('RevitAPIUI')          #Permite acceder a la interfaz de usuario desde la API
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
doc = DocumentManager.Instance.CurrentDBDocument            #Identificador del documento actual de Revit
uiapp = DocumentManager.Instance.CurrentUIApplication       #Identificador de la interfaz de usuario del documento de Revit activo
app = uiapp.Application                                     #Identificador de la aplicación de Revit abierta actualmente
uidoc = uiapp.ActiveUIDocument                              #Identificador de la Interfaz de usuario del documento abierto actualmente


# Configuración de las opciones de apertura de fichero central para que se abran solo los subproyectos que se especifiquen
subproyectos = UnWrapElement(IN[0])
subproyectosIds = List[WorksetId]()
for subproyecto in subproyectos:
    subproyectosIds.Add(subproyecto.Id)

configuracionSubproyectos = WorksetConfiguration(WorksetConfigurationOption.CloseAllWorksets)
configuracionSubproyectos.Open(subproyectosIds)


# Configuración de las opciones de apertura de fichero central para que se abran todos los subproyectos
opciones = OpenOptions()
configuracionSubproyectos = WorksetConfiguration(WorksetConfigurationOption.OpenAllWorksets)
opciones.SetOpenWorksetsConfiguration(configuracionSubproyectos)


# Configurar la apertura del fichero
opciones.AllowOpeningLocalByWrongUser = False
opciones.Audit = True
opciones.DetachFromCentralOption = DetachFromCentralOption.DoNotDetach


#Abrir modelo en BIM 360
modelId = Guid("")
proyectoId = Guid("")

path = ModelPathUtils.ConvertUserVisiblePathToModelPath("BIM 360://Pruebas BMO/Revit2021/Centralizado.rvt")

class OpenFromCloud(IOpenFromCloudCallback):
    def OnOpenConflict(scenario):
        scenerio = OpenConflictScenario.VersionArchived
        return True

opciones = OpenOptions()
uiApp.OpenAndActivateDocument(path, opciones, False, OpenFromCloud())