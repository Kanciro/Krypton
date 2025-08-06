-- REGLAS DE NOMBRES (VARIABLES, CLASES, MÉTODOS)

TODO VA A SER ESCRITO EN ESPAÑOL 

Variables
Formato: Utiliza camelCase. La primera letra es minúscula y las siguientes palabras comienzan con mayúscula.

Ejemplos: precioActual, nombreCriptomoneda, cantidadEnPortafolio, tasaDeCambioUSD

Significado:

Deben describir el dato que almacenan.

Para variables booleanas, usa prefijos como es, esta, tiene.

Ejemplos: esEstable, estaActivo, tieneSaldoSuficiente

Para colecciones (listas, arrays), usa nombres en plural.

Ejemplos: criptomonedasDisponibles, transaccionesRecientes, usuariosRegistrados

Clases (Objetos / Tipos de Datos)
Formato: Utiliza PascalCase (también conocido como UpperCamelCase). La primera letra de cada palabra está en mayúscula.

Ejemplos: Criptomoneda, Usuario, Transaccion, ExchangeRateService, Wallet

Significado:

Deben ser sustantivos o frases nominales que representen una entidad o concepto.

Deben ser singulares, ya que una clase es una plantilla para un solo objeto.

Para clases que representan un servicio o controlador, a menudo terminan en Service, Manager, Controller, Repository.

Ejemplos: CryptoDataService, ConversionManager, UserController, TransactionRepository

Métodos (Funciones)
Formato: Utiliza camelCase. Similar a las variables, la primera letra es minúscula y las siguientes palabras comienzan con mayúscula.

Ejemplos: obtenerPrecioActual, calcularGanancia, actualizarPortafolio, autenticarUsuario, convertirDivisa

Significado:

Deben ser verbos o frases verbales que describan la acción que realiza el método.

Para métodos que devuelven un valor booleano, usa prefijos como es, esta, puede.

Ejemplos: esValidaTransaccion(), estaConectado(), puedeComprar()

Para métodos "getters" (que obtienen datos), usa el prefijo get.

Ejemplos: getCodigoMoneda(), getUltimaActualizacion()

Para métodos "setters" (que establecen datos), usa el prefijo set.

Ejemplos: setPrecio()

Para métodos que realizan una acción y no devuelven necesariamente un valor, describe la acción.

Ejemplos: guardarTransaccion(), iniciarSesion(), enviarNotificacion()

----------------------------------------------------

COMENTARIOS Y DOCUMENTACIÓN INTERNA

1. Comentarios en el Código
Los comentarios en el código Python deben ser claros, concisos y útiles. Su objetivo principal es explicar el por qué y no el qué. El código en sí mismo debe ser lo suficientemente legible para explicar el "qué" (qué hace una función o una línea de código).
Prácticas recomendadas:
Docstrings: Utiliza los docstrings (cadenas de documentación) para describir módulos, clases, funciones y métodos. Sigue los estándares como PEP 257 para mantener la consistencia.
Funciones/Métodos: Describe su propósito, sus parámetros (Args:) y lo que devuelve (Returns:).
Módulos: Describe brevemente el propósito del archivo y su contenido principal.
Clases: Describe el propósito de la clase, sus atributos y los métodos importantes.
Python
# Ejemplo de un docstring para una función
def calcular_total_pedido(productos: list) -> float:
    """
    Calcula el precio total de un pedido a partir de una lista de productos.

    Args:
        productos (list): Una lista de diccionarios, donde cada diccionario representa un producto
                         y contiene las claves 'precio' y 'cantidad'.

    Returns:
        float: El precio total del pedido.
    """
    total = 0
    for producto in productos:
        total += producto['precio'] * producto['cantidad']
    return total


Comentarios en Línea: Úsalos con moderación para explicar decisiones de diseño complejas, "hacks" o para señalar partes del código que podrían ser problemáticas o que requieren una refactorización futura (# TODO:).
# TODO:: Indica una tarea pendiente. Por ejemplo: # TODO: Refactorizar esta función para que sea más eficiente.
# HACK:: Indica una solución temporal o no ideal. Por ejemplo: # HACK: Esta es una solución temporal para evitar un bug conocido del framework.
# FIX ME:: Indica un código que está roto y necesita ser arreglado.
Evita comentarios redundantes: No comentes lo obvio. Por ejemplo, x = x + 1 # Incrementa x en 1 es un mal comentario.

2. Documentación Interna
La documentación interna se enfoca en el proyecto en su conjunto y es crucial para el equipo de desarrollo, especialmente para los nuevos miembros. A diferencia de la documentación de usuario final, esta se centra en la arquitectura, las decisiones de diseño, los procesos de despliegue y las dependencias.

Prácticas recomendadas:
README.md: Este archivo es el punto de partida del proyecto. Debe contener información esencial para cualquier desarrollador.
Descripción del proyecto: Una breve descripción de qué es la aplicación.
Requisitos: Lista de dependencias del sistema y versiones de Python necesarias.
Instalación: Instrucciones paso a paso para configurar el entorno de desarrollo y la instalación de dependencias (por ejemplo, con pip install -r requirements.txt).
Ejecución: Cómo iniciar la aplicación y ejecutar pruebas.
Estructura del Proyecto: Una breve explicación de la organización de los directorios y archivos.

----------------------------------------------------

IDENTACIÓN Y ESTILO DE CÓDIGO

Estándar de Estilo: PEP 8
El estándar de facto para el estilo de código en Python es PEP 8. Es el conjunto de guías oficial que promueve la legibilidad y la consistencia. Cumplir con PEP 8 es una práctica fundamental en cualquier proyecto.
Reglas clave de PEP 8 para la identación y el estilo:
Identación: Utiliza cuatro espacios por nivel de identación. Nunca mezcles espacios y tabulaciones. La mayoría de los editores de código están configurados por defecto para esto.
Python
def mi_funcion():
    # Esta es la identación correcta de 4 espacios
    if True:
        # Otro nivel de identación
        print("Hola, mundo!")

Longitud de Línea: Limita todas las líneas a un máximo de 79 caracteres. Esto mejora la legibilidad en pantallas pequeñas y permite ver dos archivos uno al lado del otro. Si una línea es demasiado larga, puedes dividirla usando paréntesis, corchetes o llaves.
Python
# Línea larga
total = (precio_producto_1 + precio_producto_2 +
         precio_producto_3)

Espacios en Blanco:
Alrededor de operadores: Utiliza un solo espacio a cada lado de los operadores binarios (=, +, -, ==, >, etc.).
Python
# Correcto
a = 1 + 2

# Incorrecto
a=1+2


Dentro de estructuras de control: No uses espacios adicionales inmediatamente dentro de paréntesis, corchetes o llaves.
Python
# Correcto
mi_lista = [1, 2, 3]

# Incorrecto
mi_lista = [ 1, 2, 3 ]


Saltos de línea: Usa dos líneas en blanco para separar funciones y clases a nivel superior, y una línea en blanco para separar métodos dentro de una clase.
Nomenclatura:
Funciones y variables: Utiliza snake_case (minúsculas y guiones bajos). Por ejemplo: calcular_costo_total.
Clases: Utiliza CamelCase (la primera letra de cada palabra en mayúscula). Por ejemplo: MiClaseDePrueba.
Constantes: Utiliza SCREAMING_SNAKE_CASE (todo en mayúsculas y guiones bajos). Por ejemplo: MAX_VALOR.
Importaciones: Coloca todas las sentencias import al principio del archivo. Organízalas en grupos: primero las de la biblioteca estándar de Python, luego las de terceros, y finalmente las de tu propio proyecto, separadas por una línea en blanco.

Herramientas para Garantizar el Estilo de Código
Para mantener la consistencia en el equipo, es recomendable utilizar herramientas automatizadas que revisen y corrijan el estilo del código.
Linters: Un linter es una herramienta que analiza el código fuente para detectar errores de programación, fallos, errores de estilo y construcciones sospechosas.
pylint: Es un linter muy completo que comprueba errores y verifica el cumplimiento de PEP 8.
flake8: Una herramienta más ligera que combina pycodestyle (para PEP 8), pyflakes (para errores) y McCabe (para complejidad ciclomática).
Formateadores de código: Estas herramientas reescriben automáticamente tu código para que cumpla con los estándares de estilo.
black: Es un formateador "inflexible" que formatea el código sin necesidad de configuración, garantizando la consistencia en todo el equipo.
autopep8: Una herramienta que formatea automáticamente el código para cumplir con la mayoría de las reglas de estilo de PEP 8.
Integrar estas herramientas en el flujo de trabajo de desarrollo (por ejemplo, en los "hooks" de Git antes de cada commit) asegura que todo el código que se añade al repositorio ya cumple con los estándares del proyecto.
