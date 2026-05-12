# OpenBook — Sistema de Gestión de Biblioteca

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Estado](https://img.shields.io/badge/estado-funcional-green)

OpenBook es un sistema de gestión de biblioteca desarrollado en Python como proyecto de Programación Orientada a Objetos. Permite gestionar el catálogo de materiales, los usuarios (socios y bibliotecarios), los préstamos y las reservas, todo guardado en archivos JSON para que los datos persistan entre sesiones.

## 👥 Equipo

| Nombre | Rol |
|--------|-----|
| **Marcos** | Coordinador — integración, persistencia de préstamos, servicios de sanciones, menú de informes y punto de entrada |
| **Viviana** | Lógica de negocio — servicios de catálogo y préstamos, repositorio de usuarios |
| **Marc** | Modelo y persistencia — clases del modelo (Material, Usuario, Préstamo), repositorio de materiales |
| **Manuel** | Interfaz y pruebas — todos los menús de consola, tests manuales |

## 📁 Estructura del proyecto

```
OpenBook/
├── main.py                          # Punto de entrada, conecta todo
├── model/                           # Clases del dominio (Material, Usuario, Préstamo)
├── repository/                      # Acceso a datos y persistencia en JSON
├── service/                         # Lógica de negocio (préstamos, catálogo, sanciones)
├── exception/                       # Excepciones propias del proyecto
├── ui/                              # Menús de consola (interfaz de usuario)
├── util/                            # Funciones auxiliares (limpiar pantalla, pedir datos)
├── tests/                           # Tests manuales del sistema
└── datos/                           # Archivos JSON con los datos guardados
```

## ▶️ Cómo ejecutar

Solo hace falta Python 3.8 o superior. No hay que instalar ninguna librería externa.

```bash
python main.py
```

Ejecutar desde la carpeta raíz del proyecto (`OpenBook/`).

## ✅ Funcionalidades

- **Materiales**: añadir libros, revistas y recursos digitales al catálogo
- **Usuarios**: registrar socios y bibliotecarios, dar de baja usuarios
- **Préstamos**: prestar materiales, devolver con control de fecha límite
- **Reservas**: reservar un material que está prestado, cancelar reservas
- **Sanciones**: sancionar automáticamente a socios con devoluciones tardías, revisar sanciones expiradas al arrancar
- **Informes**: ver materiales disponibles, préstamos vencidos y usuarios sancionados
- **Persistencia**: todos los datos se guardan en JSON y se recuperan al volver a abrir el programa

## 🛠️ Tecnologías

- **Python 3** — sin dependencias externas, solo librería estándar
- **JSON** — para guardar y cargar los datos entre sesiones
- **Módulos usados**: `json`, `os`, `datetime`

## 🏗️ Arquitectura

El proyecto sigue un patrón en capas que aprendimos en clase:

- **model** — define las clases del sistema: `Material` (y sus subclases `Libro`, `Revista`, `RecursoDigital`), `Usuario` (`Socio`, `Bibliotecario`, `Administrador`), `Prestamo` y `Reserva`
- **repository** — se encarga de guardar y cargar los objetos en JSON; cada repositorio gestiona un tipo de dato
- **service** — contiene la lógica de negocio: qué pasa cuando se hace un préstamo, cómo se aplica una sanción, etc.
- **ui** — los menús de consola que ve el usuario; llaman a los servicios pero no tienen lógica propia

Separar estas capas nos ayudó a trabajar en paralelo sin pisarnos: cada uno podía trabajar en su parte sin romper la del otro.

## 🗂️ Datos de demo

La carpeta `datos/` ya incluye datos precargados para poder probar el sistema desde el primer momento sin tener que crear nada:

- 5 materiales: 3 libros (uno prestado), 1 revista, 1 recurso digital
- 4 usuarios: 2 socios libres, 1 socio sancionado hasta el 15/05/2026, 1 bibliotecario
- 1 préstamo activo: Laura Fernandez tiene prestado *Harry Potter y la piedra filosofal*

Para empezar desde cero, basta con borrar los archivos dentro de `datos/`.
