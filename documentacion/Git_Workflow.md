
-----

### **1. Convención de Commits**

Para mantener el historial del proyecto limpio y fácil de entender, utilizaremos la convención de commits **Conventional Commits**. Cada mensaje de commit debe seguir una estructura estandarizada:

```
<tipo>: <descripción>
```

#### **Tipos de Commit**

| Tipo | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `feat` | Una nueva característica (agrega funcionalidad). | `feat: Agregar API para obtener precios de criptomonedas` |
| `fix` | Una corrección de un bug. | `fix: Corregir error en el cálculo de ganancias` |
| `docs` | Cambios en la documentación. | `docs: Actualizar README con la estructura del proyecto` |
| `style` | Cambios de estilo (formato, espacios en blanco), sin cambios en el código. | `style: Formatear código con Black` |
| `refactor` | Un cambio en el código que no agrega funcionalidad ni corrige un bug. | `refactor: Extraer lógica de conversión a un nuevo servicio` |
| `test` | Añadir o modificar tests. | `test: Añadir pruebas unitarias para el servicio de usuarios` |
| `chore` | Actualizaciones en el proceso de construcción, dependencias, scripts o archivos de configuración. | `chore: Actualizar dependencias de la API` |

-----

### **2. Frecuencia de Push/Pull**

Para evitar conflictos de fusión y mantener a todos sincronizados, seguiremos la siguiente política:

  * **Pull (Obtener Cambios):**

      * Siempre realiza un `git pull` al inicio de tu jornada laboral o antes de comenzar a trabajar en una nueva tarea.
      * Realiza un `git pull` antes de comenzar a trabajar en tu rama (`feature`).
      * Realiza un `git pull` antes de subir tus cambios a `develop`. Esto te permite resolver conflictos localmente antes de crear una `Pull Request`.

  * **Push (Subir Cambios):**

      * Realiza `git push` regularmente, al menos una vez al día, o cuando completes una porción significativa de tu tarea. Esto sirve como un backup de tu trabajo.
      * Siempre asegúrate de que tu rama local esté sincronizada con la rama remota antes de hacer un `push`.

-----

### **3. Política de Pull Requests (PR)**

Las Pull Requests son la forma principal de fusionar código en `develop`. Una PR debe ser concisa y clara.

  * **Creación de la PR:**

      * Una vez que tu trabajo en una rama `feature` esté completo y probado localmente, crea una `Pull Request` desde tu rama hacia la rama `develop`.
      * El título de la PR debe seguir la misma convención que los commits (`feat:`, `fix:`, etc.).
      * La descripción de la PR debe incluir:
          * **¿Qué hace?** Explica la funcionalidad o el bugfix que introduce la PR.
          * **¿Por qué lo hace?** Explica el razonamiento detrás de la implementación.
          * **Pasos para probar:** Proporciona instrucciones claras para que el revisor pueda probar los cambios.

  * **Proceso de Revisión (Code Review):**

      * **Solicitud:** Asigna al menos a un compañero de equipo para que revise tu código.
      * **Revisión:** El revisor debe revisar el código en busca de errores, posibles mejoras, y asegurarse de que cumple con los estándares del proyecto (convenciones de commits, estilo de código, etc.).
      * **Aprobación:** La PR solo se fusionará una vez que reciba la aprobación de al menos un revisor.

  * **Resolución de Conflictos:**

      * Si tu PR tiene conflictos de fusión, es tu responsabilidad resolverlos en tu rama local y volver a subir los cambios antes de que la PR pueda ser fusionada.