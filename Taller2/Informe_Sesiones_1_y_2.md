# Informe de Prácticas — Sesión 1 y Sesión 2
## Taller Flutter: Aplicación Multiplataforma

---

| Campo | Detalle |
|---|---|
| **Asignatura** | Nuevas Tecnologías del Desarrollo |
| **Semestre** | 2026-02 |
| **Estudiante** | [Nombre completo] |
| **Código** | [Código estudiantil] |
| **Docente** | [Nombre del docente] |
| **Fecha** | 2 de septiembre de 2026 |

---

## Introducción General

Flutter es un framework de desarrollo multiplataforma creado por Google que permite construir aplicaciones nativas para Android, iOS, Web y escritorio desde una única base de código escrita en Dart. En este taller se desarrolló progresivamente una aplicación de contador que demuestra los fundamentos del framework: la arquitectura de widgets, el manejo de estado con `StatefulWidget` y `setState()`, y la capacidad de desplegar la misma aplicación tanto en un emulador Android como en Windows Desktop sin cambiar una sola línea de código.

---

# SESIÓN 1 — Counter App Básica

## 1. Objetivo

Construir una aplicación de contador funcional en Flutter/Dart que ejecute en Android y Windows, consolidando la instalación del entorno de desarrollo y el concepto de `StatefulWidget`.

## 2. Entorno de Desarrollo

| Herramienta | Versión | Propósito |
|---|---|---|
| Flutter SDK | ≥ 3.24.0 (stable) | Framework principal |
| Dart | Incluido en SDK | Lenguaje de programación |
| Visual Studio Code | Última estable | Editor de código |
| Android Studio | Última estable | Emulador Android + SDK |
| Visual Studio | 2022 (workload C++ Desktop) | Compilación Windows |

## 3. Código: `lib/main.dart` (Sesión 1)

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const CounterApp());
}

class CounterApp extends StatelessWidget {
  const CounterApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Contador App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
      ),
      home: const CounterPage(),
    );
  }
}

class CounterPage extends StatefulWidget {
  const CounterPage({super.key});

  @override
  State<CounterPage> createState() => _CounterPageState();
}

class _CounterPageState extends State<CounterPage> {
  int _contador = 0;

  void _incrementarContador() {
    setState(() {
      _contador++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('Contador App'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Número de pulsaciones:'),
            Text(
              '$_contador',
              style: const TextStyle(
                fontSize: 72,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementarContador,
        heroTag: 'btn_incrementar',
        tooltip: 'Incrementar',
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

## 4. Capturas de Pantalla — Sesión 1

### 4.1 Aplicación en Emulador Android — Estado inicial (contador = 0)

```
╔══════════════════════════════════════╗
║  ←  Contador App              ⋮     ║  ← AppBar (azul/índigo)
╠══════════════════════════════════════╣
║                                      ║
║                                      ║
║                                      ║
║         Número de pulsaciones:       ║
║                                      ║
║                  0                   ║  ← Texto 72px, bold
║                                      ║
║                                      ║
║                                      ║
║                                      ║
║                                  [+] ║  ← FloatingActionButton
╚══════════════════════════════════════╝
  Fondo: blanco | Plataforma: Android
```

> **[Insertar aquí captura real del emulador Android con contador en 0]**

---

### 4.2 Aplicación en Emulador Android — Contador incrementado (contador = 7)

```
╔══════════════════════════════════════╗
║  ←  Contador App              ⋮     ║
╠══════════════════════════════════════╣
║                                      ║
║                                      ║
║         Número de pulsaciones:       ║
║                                      ║
║                  7                   ║  ← El número cambia con cada toque
║                                      ║
║                                      ║
║                                  [+] ║
╚══════════════════════════════════════╝
  Fondo: blanco | Plataforma: Android
```

> **[Insertar aquí captura real del emulador Android con contador > 0]**

---

### 4.3 Aplicación en Windows Desktop — Estado inicial

```
┌─────────────────────────────────────────────────────────┐
│  Contador App                              —  □  ✕      │  ← Ventana Windows
├─────────────────────────────────────────────────────────┤
│  ←  Contador App                                        │  ← AppBar
├─────────────────────────────────────────────────────────┤
│                                                         │
│                                                         │
│              Número de pulsaciones:                     │
│                                                         │
│                        0                               │  ← Misma UI, pantalla más grande
│                                                         │
│                                                         │
│                                                  [+]    │
└─────────────────────────────────────────────────────────┘
  Plataforma: Windows Desktop (mismo código fuente)
```

> **[Insertar aquí captura real de la app corriendo en Windows con `flutter run -d windows`]**

---

## 5. Comandos de Ejecución

```bash
# Crear el proyecto
flutter create contador_app
cd contador_app

# Verificar entorno
flutter doctor

# Ejecutar en Android (emulador activo)
flutter run

# Ejecutar en Windows Desktop
flutter run -d windows
```

---

# SESIÓN 2 — Counter App Ampliada

## 1. Objetivo

Extender la aplicación de la Sesión 1 con dos funcionalidades nuevas: un botón de reinicio y cambio dinámico del color de fondo cuando el contador es múltiplo de 5.

## 2. Nuevas Funcionalidades

| Funcionalidad | Descripción técnica |
|---|---|
| Botón de reinicio | Segundo `FloatingActionButton` con `Icons.refresh` que ejecuta `setState(() { _contador = 0; })` |
| Cambio de color de fondo | `_colorDeFondo()` devuelve `Colors.lightGreen[100]` cuando `_contador > 0 && _contador % 5 == 0` |
| Indicador animado | `AnimatedOpacity` con texto "Múltiplo de 5" que aparece suavemente |
| `heroTag` únicos | Obligatorio para múltiples FABs: `'btn_incrementar'` y `'btn_reiniciar'` |

## 3. Código Clave Añadido (Sesión 2)

```dart
// Lógica de color de fondo
Color _colorDeFondo() {
  if (_contador > 0 && _contador % 5 == 0) {
    return Colors.lightGreen[100]!;
  }
  return Colors.white;
}

// Botón de reinicio
void _reiniciar() {
  setState(() {
    _contador = 0;
  });
}

// Scaffold con fondo dinámico
Scaffold(
  backgroundColor: _colorDeFondo(),   // ← nuevo
  // ...
  floatingActionButton: Column(
    mainAxisSize: MainAxisSize.min,
    children: [
      FloatingActionButton(
        onPressed: _reiniciar,
        heroTag: 'btn_reiniciar',
        backgroundColor: Colors.redAccent[100],
        child: const Icon(Icons.refresh),
      ),
      const SizedBox(height: 16),
      FloatingActionButton(
        onPressed: _incrementarContador,
        heroTag: 'btn_incrementar',
        child: const Icon(Icons.add),
      ),
    ],
  ),
)
```

## 4. Capturas de Pantalla — Sesión 2

### 4.1 Estado inicial — Contador en 0

```
╔══════════════════════════════════════╗
║  ←  Contador App              ⋮     ║
╠══════════════════════════════════════╣
║                                      ║
║                                      ║
║         Número de pulsaciones:       ║
║                                      ║
║                  0                   ║
║                                      ║  ← Sin indicador (0 no es múltiplo activo)
║                                      ║
║                                 [↺]  ║  ← Botón reinicio (rojo)  NUEVO
║                                 [+]  ║  ← Botón incremento
╚══════════════════════════════════════╝
  Fondo: BLANCO
```

> **[Insertar aquí captura real — estado inicial con ambos botones visibles]**

---

### 4.2 Contador en valor NO múltiplo de 5 (ejemplo: 3)

```
╔══════════════════════════════════════╗
║  ←  Contador App              ⋮     ║
╠══════════════════════════════════════╣
║                                      ║
║         Número de pulsaciones:       ║
║                                      ║
║                  3                   ║
║                                      ║  ← Indicador "Múltiplo de 5" invisible
║                                      ║
║                                 [↺]  ║
║                                 [+]  ║
╚══════════════════════════════════════╝
  Fondo: BLANCO (3 % 5 ≠ 0)
```

> **[Insertar aquí captura real — contador en valor no múltiplo de 5]**

---

### 4.3 Contador en múltiplo de 5 — Fondo verde (contador = 5)

```
╔══════════════════════════════════════╗
║  ←  Contador App              ⋮     ║
╠══════════════════════════════════════╣  ← Toda la pantalla en verde claro
║                                      ║
║         Número de pulsaciones:       ║
║                                      ║
║                  5                   ║  ← Número en pantalla
║           ✓ Múltiplo de 5           ║  ← Indicador aparece con AnimatedOpacity
║                                      ║
║                                 [↺]  ║
║                                 [+]  ║
╚══════════════════════════════════════╝
  Fondo: VERDE CLARO — Colors.lightGreen[100]
```

> **[Insertar aquí captura real — fondo verde con indicador "Múltiplo de 5" visible]**

---

### 4.4 Contador en múltiplo de 5 mayor (contador = 10)

```
╔══════════════════════════════════════╗
║  ←  Contador App              ⋮     ║
╠══════════════════════════════════════╣  ← Fondo verde claro nuevamente
║                                      ║
║         Número de pulsaciones:       ║
║                                      ║
║                 10                   ║
║           ✓ Múltiplo de 5           ║
║                                      ║
║                                 [↺]  ║
║                                 [+]  ║
╚══════════════════════════════════════╝
  Fondo: VERDE CLARO — 10 % 5 == 0 ✓
```

> **[Insertar aquí captura real — contador en 10 con fondo verde]**

---

### 4.5 Después de presionar reinicio — Vuelta a 0

```
╔══════════════════════════════════════╗
║  ←  Contador App              ⋮     ║
╠══════════════════════════════════════╣
║                                      ║
║         Número de pulsaciones:       ║
║                                      ║
║                  0                   ║  ← Vuelve a 0 tras presionar [↺]
║                                      ║  ← Indicador desaparece
║                                      ║
║                                 [↺]  ║
║                                 [+]  ║
╚══════════════════════════════════════╝
  Fondo: BLANCO (reiniciado desde 10)
```

> **[Insertar aquí captura real — contador en 0 luego de presionar reinicio]**

---

## 5. Comparativa Sesión 1 vs Sesión 2

| Aspecto | Sesión 1 | Sesión 2 |
|---|---|---|
| Número de botones | 1 (incrementar) | 2 (incrementar + reiniciar) |
| Color de fondo | Siempre blanco | Dinámico (blanco / verde claro) |
| Lógica condicional | No | Sí (`% 5 == 0`) |
| Indicador visual | No | `AnimatedOpacity` |
| `heroTag` | No necesario | Obligatorio (`'btn_incrementar'`, `'btn_reiniciar'`) |
| Versión | 1.0.0+1 | 2.0.0+1 |

---

## 6. Conclusiones

1. **Desarrollo multiplataforma real:** El mismo archivo `main.dart` se ejecuta sin modificaciones en Android (ARM) y Windows (x86-64). Flutter compila a código nativo en ambas plataformas mediante el motor Dart AOT, garantizando rendimiento nativo sin puentes de JavaScript.

2. **StatefulWidget y reactividad:** `setState()` es el mecanismo que hace la interfaz reactiva. Al encapsular la mutación de `_contador` dentro de `setState()`, Flutter sabe exactamente qué widgets reconstruir, lo que es más eficiente que invalidar todo el árbol.

3. **Composición de widgets:** Añadir el segundo botón no requirió modificar la lógica existente, sino componer un `Column` con dos `FloatingActionButton`. Este principio de composición —en lugar de herencia— es la base del modelo de widgets de Flutter.

4. **Lógica declarativa:** La función `_colorDeFondo()` se evalúa en cada `build()`. No se guarda el color en una variable separada, evitando duplicación de estado. Este patrón es idiomático en Flutter: derivar valores del estado existente en lugar de guardar estado calculado.

---

## 7. Referencias

Flutter Team. (2024). *StatefulWidget class*. Google LLC. https://api.flutter.dev/flutter/widgets/StatefulWidget-class.html

Flutter Team. (2024). *FloatingActionButton class*. Google LLC. https://api.flutter.dev/flutter/material/FloatingActionButton-class.html

Google. (2023). *Flutter — Build apps for any screen*. https://flutter.dev

Windmill, E. (2020). *Flutter in action*. Manning Publications.

---

*Taller de Nuevas Tecnologías del Desarrollo — Semestre 2026-02 | Formato APA 7.ª edición*
