doc = DocumentManager.Instance.CurrentDBDocument

worksetnames = IN[0]
newWorksets = []

# Comienzo de la transacción
TransactionManager.Instance.EnsureInTransaction(doc)

for name in worksetnames:
	Workset.Create(doc,name)
	newWorksets.append(name)

# Fin de la transacción
TransactionManager.Instance.TransactionTaskDone()

OUT = newWorksets
