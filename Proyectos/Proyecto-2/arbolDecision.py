from sklearn import tree
import graphviz

def generar_arbol(datos, columnas, clases):
    # Separar las características (X) y las etiquetas (y)
    X = [fila[:-1] for fila in datos]  # Todas las columnas excepto la última
    y = [fila[-1] for fila in datos]  # Última columna como etiqueta

    # Crear el clasificador del Árbol de Decisión
    clf = tree.DecisionTreeClassifier()

    # Entrenar el modelo con los datos
    clf = clf.fit(X, y)

    # Exportar el árbol de decisión en formato DOT para su visualización
    dot_data = tree.export_graphviz(clf, out_file=None, 
                                    feature_names=columnas,  
                                    class_names=clases,  
                                    filled=True, rounded=True,  
                                    special_characters=True)  

    # Crear el gráfico con graphviz
    graph = graphviz.Source(dot_data)

    # Guardar el gráfico como un archivo PDF (opcional)
    graph.render("arboles/decision_treeT")

    # Mostrar el gráfico directamente
    graph.view()