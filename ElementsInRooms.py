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



rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()
ventanas = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElements()


geometryRooms = []
localizacion = []
puntos= []


#OBTIENE LA GEOMETRÍA DE LAS HABITACINES
for room in rooms:

	calculator = SpatialElementGeometryCalculator(doc)
	results = calculator.CalculateSpatialElementGeometry(room)
	geo = results.GetGeometry()
	geometryRooms.append(geo.ToProtoType)

#OBTIENE EL PUNTO DE LOCALIZACIÓN DE LAS VENTANAS
for ventana in ventanas:
	puntos.append(ventana.Location.Point)

resultado = []
Cumple =[]

#NOS DICE SI EL PUNTO ESTA EN LA HABITACIÓN O NO
for room in rooms:
	Cumple.append(room.IsPointInRoom(XYZ(0,0,0)))
	
OUT = rooms, ventanas, Cumple, geometryRooms, puntos