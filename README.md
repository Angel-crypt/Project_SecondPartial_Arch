# **Party, Affiliates and Representatives Management System**

## 📌 Descripción
Este proyecto es un servidor desarrollado en **Flask** para la gestión de partidos políticos, sus representantes y afiliados. La aplicación permite realizar operaciones **CRUD** (Crear, Leer, Actualizar, Eliminar) sobre estas tres entidades, asegurando que tanto los **representantes** como los **afiliados** solo puedan estar vinculados a un único partido político.  


## ⚙️ Instalación  

### 1️⃣ **Crear el entorno virtual**  
Para garantizar un entorno controlado y evitar conflictos de dependencias, crea un entorno virtual llamado `political_management` ejecutando el siguiente comando:  

```bash
python -m venv political_management
```

### 2️⃣ **Activar el entorno virtual** 
Dependiendo de tu sistema operativo, usa el comando correspondiente:

```bash
Windows:
    political_management\Scripts\activate

Linux/macOS:
    source political_management/bin/activate
```

### 3️⃣ **Instalar las dependencias**
Una vez activado el entorno virtual, instala los paquetes necesarios:
```bash
pip install -r requirements.txt
```

## 🚀 Uso
Después de instalar y configurar el entorno virtual, puedes ejecutar el servidor con los siguientes comandos según tu sistema operativo:
```bash
Windows:
    political_management\Scripts\activate
    python main.py

Linux/macOS:
    source political_management/bin/activate
    python main.py
```

## 📂 Estructura del Proyecto
```plaintext
Political Project/
│── political_management/  # Entorno virtual
│── models/                # Definición de entidades
│── server/                # Endpoints de la API
│── controllers/           # Lógica de negocio y validaciones
│── main.py                # Archivo para ejecutar el servidor
│── requirements.txt       # Dependencias del proyecto
│── README.md              # Documentación del proyecto

```

## 📡 Endpoints de la API
### 📂 Rutas estáticas

|  Ruta	                         | Métodos	             | Descripción               |
|--------------------------------|-----------------------|---------------------------|
| /static/\<path:filename>	     | GET, HEAD, OPTIONS	 |   Servir archivos estáticos|

### 🆕 Autenticación
|  Ruta	                         | Métodos	             | Descripción               |
|--------------------------------|-----------------------|---------------------------|
| /register	                     | POST, OPTIONS	     | Registra un usuario en la base de datos |
| /login	                     | POST, OPTIONS	| Inicia sesión de un usuario en la base de | datos |

### 🏛 Partidos Políticos
|  Ruta	                         | Métodos	             | Descripción               |
|--------------------------------|-----------------------|---------------------------|
| /parties	                     | GET, HEAD, OPTIONS	 | Obtiene todos los partidos|
| /parties/id/<int:id>	         | GET, HEAD, OPTIONS	 | Obtiene un partido por su ID|
| /parties/name/<string:name>	 | GET, HEAD, OPTIONS	 | Obtiene un partido por su nombre|
| /parties/acronym/<string:acronym>	| GET, HEAD, OPTIONS	|Obtiene un partido por sus siglas|
| /parties	| POST, OPTIONS 	| Crea un partido en la base de datos |
| /parties/<int:id>	| PUT, OPTIONS	| Actualiza un partido en la base de datos |
| /parties/<int:id>	| DELETE, OPTIONS	| Elimina un partido de la base de datos| 

### 👥 Afiliados
|  Ruta	                         | Métodos	             | Descripción               |
|--------------------------------|-----------------------|---------------------------|
| /affiliates	| GET, HEAD, OPTIONS	|Obtiene todos los afiliados|
| /affiliates/id/<int:id>	| GET, HEAD, OPTIONS	|Obtiene un afiliado por su ID|
| /affiliates/name/<string:name>	| GET, HEAD, OPTIONS	|btiene un afiliado por su nombre|
| /affiliates/party/<int:id_party>	| GET, HEAD, OPTIONS	|Obtiene los afiliados de un partido|
| /affiliates	| POST, OPTIONS	|Crea un afiliado en la base de datos|
| /affiliates/<int:id>	| PUT, OPTIONS	|Actualiza un afiliado en la base de datos|
| /affiliates/<int:id>	| DELETE, OPTIONS	|Elimina un afiliado de la base de datos|

### 🏛 Representantes
|  Ruta	                         | Métodos	             | Descripción               |
|--------------------------------|-----------------------|---------------------------|
|/representatives	|GET, HEAD, OPTIONS	|Obtiene todos los representantes|
|/representatives/id/<int:id>	|GET, HEAD, OPTIONS	|Obtiene un representante por su ID|
|/representatives/name/<string:name>	|GET, HEAD, OPTIONS	|Obtiene un representante por su nombre|
|/representatives/party/<int:id_party>	|GET, HEAD, OPTIONS	O|btiene los representantes de un partido|
|/representatives	|POST, OPTIONS	|Crea un representante en la base de datos|
|/representatives/<int:id>	|PUT, OPTIONS	|Actualiza un representante en la base de datos|
|/representatives/<int:id>	|DELETE, OPTIONS	|Elimina un representante de la base de datos|

## 📌 Métodos que requieren JSON
Estos endpoints requieren que los datos sean enviados en formato JSON en la solicitud.
|  Ruta	                         | Métodos	             | Descripción               |
|--------------------------------|-----------------------|---------------------------|
| /register	| POST, OPTIONS	register	| Registra un usuario en la base de datos
| /login	| POST, OPTIONS	login	| Inicia sesión en la base de datos
| /parties	| POST, OPTIONS	create_party	| Crea un partido en la base de datos
| /parties/<int:id>	| PUT, OPTIONS	update_party	| Actualiza un partido
| /affiliates	| POST, OPTIONS	create_affiliate	| Crea un afiliado en la base de datos
| /affiliates/<int:id>	| PUT, OPTIONS	update_affiliate	| Actualiza un afiliado
| /representatives	| POST, OPTIONS	create_representative	| Crea un representante en la base de datos
| /representatives/<int:id>	| PUT, OPTIONS	update_representative	| Actualiza un representante

## 📌 Estructura de JSON y peticiones
### 📁 JSON
#### Ejemplo de JSON con los datos del usuario.
```json
{
    "name": "Juan",
    "password": "123456"
}
```
#### Ejemplo de JSON con los datos del partido.
```json
{
    "name": "Partido Revolucionario Independiente",
    "acronym": "PRI",
    "fundation_date": "2000-03-12",
    "ideology": "Derecha"
}
```
#### Ejemplo de JSON con los datos del afiliado.
```json
{
    "name": "Juan",
    "id_card": "123456",
    "birth_date": "2000-03-12",
    "enrollment_date": "2025-03-6",
    "id_party": 1
}
```
#### Ejemplo de JSON con los datos del representante.
```json
{
    "name": "Juan",
    "id_card": "123456",
    "birth_date": "2000-03-12",
    "enrollment_date": "2025-03-6",
    "id_party": 1,
    "party_position": "Presidente"
}
```

### ⚠️ Manejo de espacios en parámetros de la URL

Si el nombre (u otro parámetro en la URL) tiene espacios, estos deben ser reemplazados por el carácter `%20`.

**Ejemplo de parámetro con espacios:**
```javascript
El valor de `<name>` es `"Juan Perez"`, se deben convertir los espacios en `%20`, quedando así:
    GET /representatives/Juan%20Perez
```

Esto aplica para cualquier parámetro en la URL que contenga espacios. El reemplazo de los espacios con `%20` asegura que la solicitud se procese correctamente.

### ⚠️ Confirmación para eliminar recursos
Para poder eliminar cualquier recurso, es necesario confirmar la eliminación enviando el parámetro `confirm` con el valor `true`.

**Ejemplo de solicitud HTTP para eliminar un representante:**

```javascript
DELETE /representatives/1?confirm=true
```

## 🛠 Tecnologías utilizadas
- Python 3.12.3
- Flask (Microframework para desarrollo web)
- Supabase
- Virtualenv (Para el manejo de entornos virtuales)

## 📢 Notas
- Asegúrate de que Python 3.12 está instalado en tu sistema antes de iniciar el proyecto.
- El entorno virtual debe activarse siempre antes de ejecutar el servidor.
- Si encuentras errores de permisos en Linux/macOS, usa chmod +x political_management/bin/activate antes de activarlo.
- Si deseas detener el entorno virtual, usa deactivate.
