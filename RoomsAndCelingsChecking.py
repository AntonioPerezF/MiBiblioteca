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

def conversorUnidadesMetros(x): #Convierte las unidades del sistema imperial en metros
	return UnitUtils.ConvertFromInternalUnits(x, DisplayUnitType.DUT_METERS)

def valorParametro(parametro):
	if parametro.StorageType == StorageType.String:
		return parametro.AsString()
	elif parametro.StorageType == StorageType.ElementId:
		return doc.GetElement(parametro.AsElementId())
	elif parametro.StorageType == StorageType.Double:
		return parametro.AsDouble()
	else:
		return parametro.AsInteger()

#SELECCIÓN DE TODOS LOS VÍNCULOS PRESENTES EN EL DOCUMENTO ACTUAL
linkInstances = FilteredElementCollector(doc).OfClass(Autodesk.Revit.DB.RevitLinkInstance)

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

#SE FILTRAN TODAS LAS HABITACIONES QUE CONTIENEN EN EL NOMBRE LA PALABRA SALON
roomSalones = []
for room in listaRoomsAplanadaLimpia:
	nombreHabitacion = valorParametro(room.LookupParameter("Nombre"))
	if "Salon" in nombreHabitacion:
		roomSalones.append(room)
		
		
#SELECCIÓN DE TODOS LOS TECHOS DENTRO DE LOS LINKS
AllCeilingsInLinks = []
for link in linkInstances:
	if RevitLinkType.IsLoaded(doc, link.GetTypeId()):
		linkDoc = link.GetLinkDocument()
		elementosDeCategoria = FilteredElementCollector(linkDoc).WherePasses(ElementCategoryFilter(BuiltInCategory.OST_Ceilings)).WhereElementIsNotElementType().ToElements()
		AllCeilingsInLinks.append(elementosDeCategoria)

#LISTADO DE TECHOS APLANANDO LA LISTA (FLATTEN)
listaCeilingsAplanada = []
for listaCeilings in AllCeilingsInLinks:
	for ceiling in listaCeilings:
		listaCeilingsAplanada.append(ceiling)

#LISTADO DE TECHOS QUITANDO VALORES NULOS O VACIOS
listaCeilingsAplanadaLimpia = []
for element in listaCeilingsAplanada:
    if element != "Empty List":
        listaCeilingsAplanadaLimpia.append(element)

#SE FILTRAN TODAS LAS HABITACIONES QUE CONTIENEN EN EL NOMBRE LA PALABRA SALON
salidaTechos = []
for ceiling in listaCeilingsAplanadaLimpia:
	alturaTecho = conversorUnidadesMetros(valorParametro(ceiling.LookupParameter("Desfase de altura desde nivel")))
	if alturaTecho == 2.4:
		salidaTechos.append(ceiling)

OUT = roomSalones, salidaTechos