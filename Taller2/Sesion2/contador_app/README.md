# Contador App - Sesión 2

Aplicación Flutter desarrollada para la **Sesión 2** del taller universitario de Nuevas Tecnologías del Desarrollo. Es la versión ampliada de la Sesión 1.

---

## Funcionalidades

### Heredadas de la Sesión 1
- Contador numérico que inicia en 0.
- Botón `+` (FloatingActionButton) que incrementa el valor en 1.
- Pantalla centrada con el valor del contador en texto grande (fontSize 64).

### Nuevas en la Sesión 2

#### 1. Boton de reinicio
Un segundo `FloatingActionButton` con el icono `Icons.refresh` que restablece el contador a 0 con un solo toque. El botón aparece encima del botón principal y tiene un color distinto (rojo claro) para diferenciarse visualmente.

#### 2. Cambio dinamico de color de fondo
El `Scaffold` cambia su `backgroundColor` de acuerdo con esta regla:

| Condicion | Color de fondo |
|-----------|---------------|
| `_contador > 0` Y `_contador % 5 == 0` | `Colors.lightGreen[100]` |
| Cualquier otro valor | `Colors.white` |

Ejemplos de activacion: 5, 10, 15, 20...

---

## Requisitos previos

| Herramienta | Version minima |
|-------------|---------------|
| Flutter SDK | 3.0.0 |
| Dart SDK    | 3.0.0         |
| Android Studio / VS Code | Cualquier version reciente |

---

## Pasos para ejecutar

```bash
# 1. Clonar o copiar el proyecto en tu maquina

# 2. Instalar dependencias
flutter pub get

# 3. Verificar dispositivos disponibles
flutter devices

# 4. Ejecutar en el emulador o dispositivo conectado
flutter run

# (opcional) Ejecutar en modo web
flutter run -d chrome
```

Para aplicar cambios en caliente durante el desarrollo, presiona **r** en la terminal (hot reload) o **R** para reinicio completo (hot restart).

---

## Estructura del proyecto

```
contador_app/
├── lib/
│   └── main.dart          # Logica completa de la aplicacion
├── informe/
│   └── informe_sesion2.md # Plantilla del informe academico
├── pubspec.yaml           # Dependencias y configuracion del proyecto
└── README.md              # Este archivo
```

---

## Conceptos de Flutter aplicados

- `StatefulWidget` y `setState()` para manejo de estado local.
- `floatingActionButton` con multiples botones mediante `Column`.
- `heroTag` unico por cada `FloatingActionButton` para evitar errores de animacion.
- `AnimatedOpacity` para transicion suave del indicador de multiplo.
- `Theme` con Material 3 (`useMaterial3: true`).
