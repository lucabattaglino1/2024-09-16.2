from model.modello import Model

mdl = Model()
mdl.buildGraph(28,-132,'light')
print(f"Nodi: {mdl.getNumNodes()}")
print(f"Archi: {mdl.getNumEdges()}")
