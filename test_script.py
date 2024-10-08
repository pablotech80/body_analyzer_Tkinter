from calculadora import interpretar_porcentaje_generico

# Pruebas manuales
print(interpretar_porcentaje_generico(30, 'h'))  # Debería retornar "Alto"
print(interpretar_porcentaje_generico(8, 'h'))   # Debería retornar "Bajo"
print(interpretar_porcentaje_generico(15, 'h'))  # Debería retornar "Normal"
print(interpretar_porcentaje_generico(20, 'm'))  # Debería retornar "Normal"
print(interpretar_porcentaje_generico(35, 'm'))  # Debería retornar "Alto"
print(interpretar_porcentaje_generico(16, 'm'))  # Debería retornar "Bajo"
