
def conversorUnidadesMetros(x): #Convierte las unidades del sistema imperial en metros
	return UnitUtils.ConvertFromInternalUnits(x, DisplayUnitType.DUT_METERS)

def conversorUnidadesMetrosCuadrados(x): #Convierte las unidades del sistema imperial en metros cuadrados
	return UnitUtils.ConvertFromInternalUnits(x, DisplayUnitType.DUT_SQUARE_METERS)

def conversorUnidadesMetrosCubicos(x): #Convierte las unidades del sistema imperial en metros cubicos
	return UnitUtils.ConvertFromInternalUnits(x, DisplayUnitType.DUT_CUBIC_METERS)

def conversorUnidadesMetros2021(x): #Convierte las unidades del sistema imperial en metros
	return UnitUtils.ConvertFromInternalUnits(x, UnitTypeId.DUT_METERS)

def conversorUnidadesMetrosCuadrados2021(x): #Convierte las unidades del sistema imperial en metros cuadrados
	return UnitUtils.ConvertFromInternalUnits(x, UnitTypeId.DUT_SQUARE_METERS)

def conversorUnidadesMetrosCubicos2021(x): #Convierte las unidades del sistema imperial en metros cubicos
	return UnitUtils.ConvertFromInternalUnits(x, UnitTypeId.DUT_CUBIC_METERS)

def valorParametro(parametro):
	if parametro.StorageType == StorageType.String:
		return parametro.AsString()
	elif parametro.StorageType == StorageType.ElementId:
		return doc.GetElement(parametro.AsElementId())
	elif parametro.StorageType == StorageType.Double:
		return parametro.AsDouble()
	else:
		return parametro.AsInteger()
