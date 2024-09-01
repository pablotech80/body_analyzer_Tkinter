.. analisis_corporal documentation master file, created by
   sphinx-quickstart on Sun Sep  1 19:50:32 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Proyecto Final Python/ Tokio School
===================================

Aplicación de escritorio - Análisis de composición corporal
===========================================================

.. contents:: Tabla de contenidos
   :local:

Introducción
------------

### 1.1 Descripción General del Proyecto

**"Análisis de Composición Corporal"** es una aplicación de escritorio desarrollada en Python, diseñada para obtener resultados
de salud mediante cálculos biométricos.

Esta herramienta permite a profesionales de la salud, entrenadores personales, nutricionistas (como lo soy yo),
calcular y hacer seguimiento de diversos parámetros de composición corporal. Además, se podrá escalar a mejoras en funcionalidad,
estética de la interfaz de usuario y en términos de seguridad en la base de datos.

### 1.2 Objetivos del Proyecto

Los principales objetivos de este proyecto son:

- `Proporcionar una interfaz intuitiva para la entrada de datos biométricos.`
- `Calcular con precisión diversos indicadores de composición corporal, incluyendo:`

  - `Índice de Masa Corporal (IMC)`
  - `Porcentaje de Grasa Corporal`
  - `Masa Muscular`
  - `Tasa Metabólica Basal (TMB)`
  - `FFMI (calidad de masa muscular y tope genético)`
  - `Ratio Cintura/Cadera`
  - `Reparto de Macronutrientes según objetivo.`
- `Almacenar y gestionar perfiles de clientes para un seguimiento a largo plazo(en desarrollo).`
- `Generar informes detallados sobre la composición corporal y su evolución en el tiempo(CSV).`
- `Ofrecer recomendaciones e interpretaciones personalizadas basadas en los resultados del análisis.`

### 1.3 Alcance del Proyecto

Esta aplicación está diseñada para ser utilizada como herramienta complementaria por profesionales de la salud,
como en clínicas de nutrición, gimnasios, consultas médicas, entrenadores personales,
y cualquier persona que necesite medir parámetros biométricos.

**Funcionalidades principales:**

- Registro y autenticación de usuarios.
- Entrada y almacenamiento de datos de clientes.
- Cálculos automáticos de composición corporal.
- Visualización de resultados y tendencias.
- Generación de informes.
- Extracción de archivos.

Requisitos del sistema
----------------------

Esta aplicación ha sido desarrollada y probada con Python 3.12. Se recomienda usar esta versión para garantizar la compatibilidad.

### Librerías y Dependencias

Las siguientes librerías son necesarias para ejecutar la aplicación:

- `altgraph==0.17.4`
- `greenlet==3.0.3`
- `iniconfig==2.0.0`
- `macholib==1.16.3`
- `packaging==24.1`
- `pluggy==1.5.0`
- `pyinstaller==6.10.0`
- `pyinstaller-hooks-contrib==2024.8`
- `pytest==8.3.2`
- `setuptools==72.2.0`
- `SQLAlchemy==2.0.31`
- `typing_extensions==4.12.2`
- `bcrypt==4.2.0`

Para instalar estas dependencias, ejecute el siguiente comando en la terminal:




Instalación - Configuración
---------------------------

Introducción
============


