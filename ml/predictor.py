import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
from datetime import datetime, timedelta

class ModeloPredictorVentas:
    """Modelo predictivo para ventas usando Random Forest"""
    
    def __init__(self):
        self.modelo = None
        self.modelo_path = "ml/modelo_predictor_ventas_random_forest.pkl"
        self.cargar_modelo()
    
    def cargar_modelo(self):
        """Carga el modelo entrenado si existe"""
        try:
            if os.path.exists(self.modelo_path):
                self.modelo = joblib.load(self.modelo_path)
            else:
                self.modelo = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
        except:
            self.modelo = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
    
    def guardar_modelo(self):
        """Guarda el modelo entrenado"""
        try:
            joblib.dump(self.modelo, self.modelo_path)
        except:
            pass
    
    def entrenar_modelo(self, datos_historicos):
        """Entrena el modelo con datos historicos"""
        try:
            if datos_historicos.empty or len(datos_historicos) < 30:
                return False
            
            # Verificar que la columna Total exista
            if 'Total' not in datos_historicos.columns:
                return False
            
            # Asegurar que los datos son numericos
            datos_historicos = datos_historicos.copy()
            datos_historicos['Total'] = pd.to_numeric(datos_historicos['Total'], errors='coerce')
            datos_historicos = datos_historicos.dropna(subset=['Total'])
            
            if len(datos_historicos) < 30:
                return False
            
            # Preparar caracteristicas (usando ventas de los ultimos 7 dias)
            caracteristicas = []
            objetivos = []
            
            for i in range(len(datos_historicos) - 7):
                try:
                    ventas_semana = datos_historicos['Total'].iloc[i:i+7].values
                    # Asegurar que los valores son numericos
                    ventas_semana = ventas_semana.astype(float)
                    caracteristicas.append(ventas_semana)
                    objetivos.append(float(datos_historicos['Total'].iloc[i+7]))
                except:
                    continue
            
            if len(caracteristicas) > 10:
                caracteristicas = np.array(caracteristicas)
                objetivos = np.array(objetivos)
                
                # Entrenar modelo
                self.modelo.fit(caracteristicas, objetivos)
                self.guardar_modelo()
                return True
            
            return False
            
        except Exception as e:
            print(f"Error entrenando modelo: {e}")
            return False
    
    def predecir_ventas(self, datos_historicos, dias=7):
        """Predice ventas para los proximos dias"""
        try:
            if datos_historicos.empty or 'Total' not in datos_historicos.columns:
                # Datos simulados si no hay historicos
                return [100 + i * 5 for i in range(dias)]
            
            # Asegurar datos numericos
            datos = datos_historicos.copy()
            datos['Total'] = pd.to_numeric(datos['Total'], errors='coerce')
            datos = datos.dropna(subset=['Total'])
            
            if len(datos) < 14:
                # Si hay pocos datos, usar promedio simple
                promedio = datos['Total'].mean()
                return [max(50, promedio + (i * 2)) for i in range(dias)]
            
            predicciones = []
            ultimas_ventas = datos['Total'].tail(7).values.astype(float)
            
            for _ in range(dias):
                try:
                    if len(ultimas_ventas) == 7 and self.modelo is not None:
                        prediccion = self.modelo.predict([ultimas_ventas])[0]
                        prediccion = max(50, float(prediccion))  # Minimo 50
                        predicciones.append(prediccion)
                        # Actualizar ventana deslizante
                        ultimas_ventas = np.append(ultimas_ventas[1:], prediccion)
                    else:
                        # Fallback a promedio simple
                        promedio = datos['Total'].mean()
                        predicciones.append(max(50, promedio))
                except:
                    # Error en prediccion, usar promedio
                    promedio = datos['Total'].mean()
                    predicciones.append(max(50, promedio))
            
            return predicciones
            
        except Exception as e:
            print(f"Error en prediccion: {e}")
            return [100 + i * 5 for i in range(dias)]
    
    def predecir_productos_populares(self, facturas_df, top_n=5):
        """Predice productos mas vendidos"""
        try:
            if facturas_df.empty:
                return pd.DataFrame({
                    'Producto': ['Producto A', 'Producto B', 'Producto C'], 
                    'Ventas_Estimadas': [100, 85, 70]
                })
            
            if 'Idproducto' in facturas_df.columns:
                ventas_por_producto = facturas_df.groupby('Idproducto').size().sort_values(ascending=False)
                
                # Si no hay suficientes datos, devolver datos simulados
                if len(ventas_por_producto) < 3:
                    return pd.DataFrame({
                        'Producto': ['Producto A', 'Producto B', 'Producto C'], 
                        'Ventas_Estimadas': [100, 85, 70]
                    })
                
                # Aplicar tendencia simple
                predicciones = ventas_por_producto.head(top_n).values * (1 + np.random.uniform(-0.1, 0.1, top_n))
                
                return pd.DataFrame({
                    'ID_Producto': ventas_por_producto.head(top_n).index,
                    'Ventas_Estimadas': predicciones.astype(int)
                })
            else:
                return pd.DataFrame({
                    'Producto': ['Producto A', 'Producto B', 'Producto C'], 
                    'Ventas_Estimadas': [100, 85, 70]
                })
                
        except Exception as e:
            print(f"Error en prediccion de productos: {e}")
            return pd.DataFrame({
                'Producto': ['Producto A', 'Producto B', 'Producto C'], 
                'Ventas_Estimadas': [100, 85, 70]
            })

# Instancia global del predictor
predictor = ModeloPredictorVentas()