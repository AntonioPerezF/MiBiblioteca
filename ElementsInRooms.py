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


#-----------------------------------------------------------------------------------------------------------------
# geometryRooms = []
# #OBTIENE LA GEOMETRÍA DE LAS HABITACINES
# for room in rooms:

# 	calculator = SpatialElementGeometryCalculator(doc)
# 	results = calculator.CalculateSpatialElementGeometry(room)
# 	geo = results.GetGeometry()
# 	geometryRooms.append(geo.ToProtoType)
#----------------------------------------------------------------------------------------------------------------

class VentanasConPuntoDeComprobacion:
    def __init__(self, objetoVentana, puntoComprobacion1, puntoComprobacion2, puntoComprobacion3, puntoComprobacion4, roomEnContacto):
    	self.ObjetoVentana = objetoVentana
    	self.PuntoComprobacion1 = puntoComprobacion1
	self.PuntoComprobacion2 = puntoComprobacion2
  	self.PuntoComprobacion3 = puntoComprobacion3
    	self.PuntoComprobacion4 = puntoComprobacion4
    	self.RoomEnContacto = roomEnContacto

def ConversorUnidades(x): #Convierte las unidades del sistema imperial en metros
	return UnitUtils.ConvertFromInternalUnits(x, DisplayUnitType.DUT_METERS)

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


#SELECCIÓN DE TODOS LOS ELEMENTOS DE LA CATEGORIA ESPECIFICADA
allElementsInModel = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElements()

#SE OBTIENE EL PUNTO DE LOCALIZACIÓN DEL ELEMENTO
listaVentanasConPunto = []
for element in allElementsInModel:
	#OBTENEMOS COMPONENTES X, Y, Z DEL PUNTO DE COLOCACIÓN DE LA INSTANCIA DE FAMILIA
	ComponenteX = ConversorUnidades(element.Location.Point.X)
	ComponenteY = ConversorUnidades(element.Location.Point.Y)
	ComponenteZ = ConversorUnidades(element.Location.Point.Z)
	d = 0.35
 	#SUMAMOS UN DESFASE PARA GARANTIZAR QUE EL PUNTO ESTA DENTRO DE LA HABITACIÓN
 	puntoComprobacion1 = XYZ(ComponenteX+d, ComponenteY+d, ComponenteZ+d)
	puntoComprobacion2 = XYZ(ComponenteX+d, ComponenteY-d, ComponenteZ+d)
 	puntoComprobacion3 = XYZ(ComponenteX-d, ComponenteY+d, ComponenteZ+d)
	puntoComprobacion4 = XYZ(ComponenteX-d, ComponenteY-d, ComponenteZ+d)
 	
  #CREAMOS UNA LISTA CON LAS INSTANCIAS DE LA CLASE CREADA
	listaVentanasConPunto.append(VentanasConPuntoDeComprobacion(element,puntoComprobacion1,puntoComprobacion2,puntoComprobacion3,puntoComprobacion4,0))
 	
  
	roomCalculationPoint= []
	roomCalculationPoint.append(element.get_Parameter(BuiltInParameter.ROOM_CALCULATION_POINT))


TransactionManager.Instance.EnsureInTransaction(doc)

#NOS DICE SI EL PUNTO ESTA EN LA HABITACIÓN O NO
for room in listaRoomsAplanadaLimpia:
	nombreRoom = room.LookupParameter("Nombre").AsString()
	for ventanaConPunto in listaVentanasConPunto:
		parametroDestino = ventanaConPunto.ObjetoVentana.LookupParameter("Comentarios")
    
		if room.IsPointInRoom(ventanaConPunto.PuntoComprobacion1) and nombreRoom!="Terraza Cub." and nombreRoom!="Terraza Descub.":
			parametroDestino.Set(nombreRoom)
   			VentanasConPuntoDeComprobacion.roomEnContacto = room
  
		elif room.IsPointInRoom(ventanaConPunto.PuntoComprobacion2) and nombreRoom!="Terraza Cub." and nombreRoom!="Terraza Descub.":
			parametroDestino.Set(nombreRoom)
   			VentanasConPuntoDeComprobacion.roomEnContacto = room
		
  		elif room.IsPointInRoom(ventanaConPunto.PuntoComprobacion3) and nombreRoom!="Terraza Cub." and nombreRoom!="Terraza Descub.":
			parametroDestino.Set(nombreRoom)
   			VentanasConPuntoDeComprobacion.roomEnContacto = room
		
  		elif room.IsPointInRoom(ventanaConPunto.PuntoComprobacion4) and nombreRoom!="Terraza Cub." and nombreRoom!="Terraza Descub.":
			parametroDestino.Set(nombreRoom)
   			VentanasConPuntoDeComprobacion.roomEnContacto = room

TransactionManager.Instance.TransactionTaskDone()
		
OUT = listaRoomsAplanadaLimpia, allElementsInModel, listaVentanasConPunto
