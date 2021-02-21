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

#SELECCIÓN DE TODOS LOS VÍNCULOS PRESENTES EN EL DOCUMENTO ACTUAL
linkInstances = FilteredElementCollector(doc).OfClass(Autodesk.Revit.DB.RevitLinkInstance)
#SELECCIÓN DE TODOS LOS ELEMENTOS DE LA CATEGORIA ESPECIFICADA EN EL INPUT EN EL DOCUMENTO ACTUAL
AllRoomsInModel = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsElementType().ToElements()


#SELECCIÓN DE TODAS LAS HABITACIONES DENTRO DE LOS LINKS
AllRoomsInLinks = []
for link in linkInstances:
	if RevitLinkType.IsLoaded(doc, link.GetTypeId()):
		linkDoc = link.GetLinkDocument()
		elementosDeCategoria = FilteredElementCollector(linkDoc).WherePasses(ElementCategoryFilter(BuiltInCategory.OST_Rooms)).WhereElementIsNotElementType().ToElements()
		AllRoomsInLinks.append(elementosDeCategoria)

#LISTADO DE ROOMS APLANANDO LA LISTA (FLATTEN)
listaRoomsAplanada = []
for listaRooms in AllRoomsInLinks:
	for room in listaRooms:
		listaRoomsAplanada.append(room)

#LISTADO DE ROOMS QUITANDO VALORES NULOS O VACIOS
listaRoomsAplanadaLimpia = []
for element in listaRoomsAplanada:
    if element != "Empty List":
        listaRoomsAplanadaLimpia.append(element)
		
OUT = listaRoomsAplanadaLimpia

