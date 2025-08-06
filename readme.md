KRYPTON: Aplicación de Criptomonedas
¡Bienvenido al proyecto Krypton! Este repositorio contiene el código fuente para una aplicación de gestión de criptomonedas. La arquitectura del proyecto está diseñada en microservicios para garantizar la escalabilidad y la mantenibilidad.

Estructura del Proyecto
El proyecto está organizado en una arquitectura de microservicios, donde cada servicio es un componente autónomo con su propia lógica de negocio.

crypto_app/
├── microservicios/
│   ├── api_gateway/
│   ├── servicio_conversion/
│   ├── servicio_datos_cripto/
│   └── servicio_usuarios/
├── entorno_virtual/
├── .gitkeep
├── readme.md
└── requirements.txt
Descripción de los Componentes Principales
microservicios/
Este directorio contiene la capa de lógica de negocio, donde cada subdirectorio es un microservicio independiente.

api_gateway/

Actúa como el punto de entrada para todas las solicitudes del cliente.

Se encarga de la autenticación, autorización y el enrutamiento de las peticiones a los microservicios correspondientes.

Este servicio aún no contiene código, por lo que hemos añadido un archivo .gitkeep para preservar la estructura de carpetas en el repositorio.

servicio_conversion/

Se encarga de la lógica para la conversión de divisas.

El subdirectorio services contendrá los clientes de API para obtener las tasas de cambio.

servicio_datos_cripto/

Este servicio gestiona la obtención y el procesamiento de datos en tiempo real y datos históricos de criptomonedas.

El directorio models contendrá las clases de datos de las criptomonedas.

El directorio services contendrá los clientes de API para interactuar con APIs externas como CoinGecko, CoinMarketCap, etc.

servicio_usuarios/

Gestiona toda la lógica relacionada con los usuarios: registro, inicio de sesión, perfiles, etc.

El subdirectorio database contendrá los scripts y la lógica de conexión a la base de datos de usuarios.

El subdirectorio models contendrá las clases de datos para los usuarios.

Otros Archivos Importantes
entorno_virtual/: Directorio que contiene el entorno virtual del proyecto, asegurando el aislamiento de las dependencias.

requirements.txt: Archivo que lista todas las dependencias de Python del proyecto.

readme.md: Este archivo, que proporciona una descripción general del proyecto y su estructura.

.gitkeep: Archivos marcadores que permiten a Git rastrear y mantener carpetas que de otro modo estarían vacías.

---------------------------------------------------------------------------------------


CI

![CI de Python](https://github.com/Kanciro/Krypton/actions/workflows/main.yml/badge.svg)