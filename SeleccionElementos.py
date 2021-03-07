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



#INPUT de tipo categoría que desempacamos para poder usar con la API de revit
categoria = UnwrapElement(IN[0])
#Selección de todos los ejemplares de muro por el id de la categoría
muros = FilteredElementCollector(doc).OfCategoryId(categoria.Id).WhereElementIsNotElementType().ToElements()


#Selección de ejemplares y tipos por BuiltIn parameters (en este caso de categoria muros)
collectorMuros = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).ToElements()
#Selección de los tipos por BuiltIn parameters (en este caso de categoria muros)
collector_TiposMuros = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsElementType().ToElements()
#Selección de los tipos por BuiltIn parameters (en este caso de categoria puertas)
collector_EjemplaresPuertas = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()



#Se crea un filtro inverso para posteriormente seleccionar todos los elementos que no pertenezcan a la categoria especificada. FilteredElementCollector siempre seleccionará por defecto tanto a los ejemplares como a los tipos de la categoria.
filtroInverso = ElementCategoryFilter(categoria.Id, True)
elementosNoMuros = FilteredElementCollector(doc).WherePasses(filtroInverso).ToElements()



#Seleccionar elementos a través de un filtro multicategoría.
#Crear lista fuertemente tipada
builtInCat = List[BuiltInCategory]()
#Se añaden dos categorias con BuiltIn Parameters
builtInCat.Add(BuiltInCategory.OST_Doors)
builtInCat.Add(BuiltInCategory.OST_Windows)
#Se crea filtro multicategoría
filtroBuiltIn = ElementMulticategoryFilter(builtInCat)
#Se seleccionan los ejemplares de las categorias especificadas en la lista del filtro
elements = FilteredElementCollector(doc).WherePasses(filtroBuiltIn).WhereElementIsNotElementType().ToElements()
#Se obtienen los ids de los elementos seleccionados por las categorias especificadas en la lista del filtro usando ".ToElementIds()"
elementsIds = FilteredElementCollector(doc).WherePasses(filtroBuiltIn).WhereElementIsNotElementType().ToElementIds()




#Vamos a crear otra selección por multicategoria por otro camino, creando una ICollection
#Desempacar las categorias y obtener sus ids
listaCategorias = UnwrapElement(IN[1])
listaCategoriasId = [c.Id for c in listaCategorias]
#Construir una ICollection de ElementIds
catId = List[ElementId](listaCategoriasId)
#Se podría haber hecho como en el ejemplo anterior añadiendo uno a uno
#Crear el filtro
filtroCat = ElementMulticategoryFilter(catId)
#Selección usando el filtro multicategorias. Esta vez seleccionamos ejemplares y tipos
elements2 = FilteredElementCollector(doc).WherePasses(filtroCat).ToElements()





OUT = muros, collectorMuros, collector_TiposMuros, collector_EjemplaresPuertas, elementosNoMuros, elements, elementsIds, elements2
