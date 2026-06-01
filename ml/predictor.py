import joblib

modelo = joblib.load(
    "ml/modelo_predictor_ventas_random_forest.pkl"
)

def predecir(datos):

    resultado = modelo.predict(datos)

    return resultado