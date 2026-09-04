# Informe de Práctica - Sesión 2: Ampliación del Contador en Flutter

**Asignatura:** Nuevas Tecnologías del Desarrollo
**Institución:** [Nombre de la Universidad]
**Programa:** [Nombre del Programa]
**Estudiante:** [Nombre completo del estudiante]
**Código estudiantil:** [Código]
**Docente:** [Nombre del docente]
**Fecha de entrega:** 2 de septiembre de 2026

---

## 1. Introducción

El desarrollo de aplicaciones móviles multiplataforma ha experimentado un crecimiento significativo en los últimos años, impulsado por la necesidad de reducir costos y tiempos de desarrollo sin sacrificar la experiencia de usuario. Flutter, el framework de código abierto creado por Google, representa una de las soluciones más adoptadas en esta tendencia, al permitir compilar aplicaciones nativas para Android, iOS, Web y escritorio desde una única base de código escrita en el lenguaje Dart (Google, 2023).

La presente práctica corresponde a la **Sesión 2** del taller universitario, que constituye una evolución directa de la aplicación de contador desarrollada en la Sesión 1. El objetivo es incorporar dos funcionalidades nuevas: un botón de reinicio del contador y un cambio dinámico del color de fondo basado en la lógica del múltiplo de cinco. A través de este ejercicio, el estudiante consolida el uso del widget `StatefulWidget` y profundiza en el manejo de estado local con `setState()`.

---

## 2. Marco Teórico

### 2.1 Flutter y el desarrollo multiplataforma

Flutter utiliza un motor de renderizado propio (Skia / Impeller) que dibuja cada píxel de la interfaz directamente en el lienzo del dispositivo, sin depender de los widgets nativos del sistema operativo. Esto garantiza coherencia visual entre plataformas y un rendimiento cercano al nativo (Windmill, 2020). La arquitectura de Flutter se basa en un árbol de widgets que se reconstruye de manera eficiente ante cambios de estado.

### 2.2 StatelessWidget vs StatefulWidget

En Flutter, todo elemento de la interfaz es un **widget**. Existen dos categorías fundamentales:

| Característica | StatelessWidget | StatefulWidget |
|----------------|----------------|----------------|
| Estado interno | No tiene | Tiene (`State<T>`) |
| Reconstrucción | Solo cuando cambian sus parámetros externos | Cuando se llama `setState()` |
| Casos de uso | Textos, íconos, layouts fijos | Formularios, contadores, animaciones |
| Rendimiento | Ligeramente más eficiente | Adecuado para interactividad |

Un `StatefulWidget` se compone de dos clases: el widget inmutable que describe la configuración, y el objeto `State` que contiene los datos mutables y el método `build()` que Flutter invoca cada vez que el estado cambia (Flutter Team, 2024).

### 2.3 El método setState()

`setState()` es el mecanismo oficial de Flutter para notificar al framework que el estado interno de un widget ha cambiado y que debe reconstruirse. Su uso correcto implica:

1. Modificar la variable de estado **dentro** de la función lambda que se pasa a `setState()`.
2. No realizar operaciones costosas o asíncronas dentro de dicha lambda.
3. Evitar llamar a `setState()` después de que el widget ha sido eliminado del árbol.

### 2.4 Hot Reload y Hot Restart

Flutter ofrece dos mecanismos de actualización en tiempo de desarrollo:

- **Hot Reload (`r`):** Inyecta los cambios de código en la VM de Dart sin reiniciar la aplicación. Preserva el estado actual. Ideal para ajustes de UI.
- **Hot Restart (`R`):** Reinicia completamente la aplicación, perdiendo el estado. Necesario cuando se modifican variables iniciales o la estructura del árbol de widgets.

### 2.5 FloatingActionButton múltiple

Flutter no admite directamente más de un `floatingActionButton` en el `Scaffold`, pero sí permite asignar un widget compuesto (como una `Column` o un `Stack`) a esa propiedad. Cada `FloatingActionButton` dentro de ese composable debe declarar un `heroTag` único para evitar conflictos en las animaciones de transición de pantalla (Flutter Team, 2024).

---

## 3. Desarrollo

### 3.1 Descripción de la aplicación

La aplicación `contador_app` (Sesión 2) es una pantalla única construida con `StatefulWidget` que presenta:

- Un `AppBar` con el título "Contador App".
- Un texto grande (fontSize 64) centrado en pantalla que muestra el valor actual del contador.
- Un indicador de texto que aparece con transición suave cuando el contador alcanza un múltiplo de 5.
- Dos `FloatingActionButton` en la esquina inferior derecha: el botón `+` (incrementar) y el botón de reinicio (reiniciar a 0).
- Un fondo dinámico que cambia a `Colors.lightGreen[100]` cuando el contador es múltiplo de 5 y mayor que 0, y vuelve a blanco en los demás casos.

### 3.2 Estructura del código

#### Widget raíz: `CounterApp`

```dart
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
      home: const PantallaContador(),
    );
  }
}
```

`CounterApp` es `StatelessWidget` porque solo configura el tema y el punto de entrada. No necesita estado propio.

#### Widget de pantalla: `PantallaContador` y `_PantallaContadorState`

La variable `_contador` se declara en el objeto `State` y su modificación siempre ocurre dentro de `setState()`:

```dart
int _contador = 0;

void _incrementar() {
  setState(() {
    _contador++;
  });
}

void _reiniciar() {
  setState(() {
    _contador = 0;
  });
}
```

#### Lógica de color de fondo (funcionalidad nueva)

```dart
Color _colorDeFondo() {
  if (_contador > 0 && _contador % 5 == 0) {
    return Colors.lightGreen[100]!;
  }
  return Colors.white;
}
```

Esta función se invoca en el `backgroundColor` del `Scaffold`. Cada vez que `setState()` es llamado, Flutter reconstruye el `build()` y evalúa de nuevo esta función, actualizando el fondo de manera reactiva.

#### Botones duales con `Column`

```dart
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
      onPressed: _incrementar,
      heroTag: 'btn_incrementar',
      child: const Icon(Icons.add),
    ),
  ],
),
```

El `heroTag` único por botón es obligatorio cuando existen múltiples `FloatingActionButton` en la misma pantalla; de lo contrario, Flutter lanza una excepción en tiempo de ejecución.

### 3.3 Diferencias respecto a la Sesión 1

| Aspecto | Sesión 1 | Sesión 2 |
|---------|----------|----------|
| Botones | 1 (incrementar) | 2 (incrementar + reiniciar) |
| Color de fondo | Fijo (blanco) | Dinámico (blanco / verde claro) |
| Indicador de multiplo | No existía | `AnimatedOpacity` con texto |
| Versión de la app | 1.0.0+1 | 2.0.0+1 |

---

## 4. Evidencias

> **Instrucción para el estudiante:** Insertar aquí las capturas de pantalla obtenidas durante la ejecución de la aplicación. Se recomienda incluir al menos las siguientes:

### 4.1 Pantalla inicial (contador = 0)

*[Insertar captura aquí]*

*Descripción:* Pantalla con fondo blanco y contador en cero. Los dos botones son visibles en la esquina inferior derecha.

### 4.2 Contador en valor no múltiplo de 5 (ejemplo: 3)

*[Insertar captura aquí]*

*Descripción:* El fondo permanece blanco. El indicador "Múltiplo de 5" no es visible.

### 4.3 Contador en múltiplo de 5 (ejemplo: 5 o 10)

*[Insertar captura aquí]*

*Descripción:* El fondo cambia a verde claro (`Colors.lightGreen[100]`). El texto "Múltiplo de 5" aparece debajo del número.

### 4.4 Acción de reinicio

*[Insertar captura antes y después de presionar el botón de reinicio]*

*Descripción:* Al presionar el botón rojo con `Icons.refresh`, el contador vuelve a 0 y el fondo retorna a blanco.

---

## 5. Conclusiones

[El estudiante debe redactar mínimo tres conclusiones basadas en la experiencia de la práctica. Se sugieren los siguientes puntos de reflexión:]

1. **Sobre el manejo de estado:** ¿Qué diferencias observaste entre el uso de `StatelessWidget` y `StatefulWidget`? ¿Por qué fue necesario usar `StatefulWidget` para esta aplicación?

2. **Sobre la reactividad de Flutter:** ¿Cómo reacciona la interfaz al cambio de estado? ¿Qué papel juega `setState()` en ese proceso?

3. **Sobre las nuevas funcionalidades:** ¿Qué dificultades encontraste al agregar el botón de reinicio y el cambio de color? ¿Cómo las resolviste?

*[Redactar aquí las conclusiones propias del estudiante]*

---

## 6. Referencias

Flutter Team. (2024). *Flutter documentation: StatefulWidget class*. Google LLC. https://api.flutter.dev/flutter/widgets/StatefulWidget-class.html

Flutter Team. (2024). *Flutter documentation: FloatingActionButton class*. Google LLC. https://api.flutter.dev/flutter/material/FloatingActionButton-class.html

Flutter Team. (2024). *Flutter documentation: Scaffold class - floatingActionButton property*. Google LLC. https://api.flutter.dev/flutter/material/Scaffold/floatingActionButton.html

Google. (2023). *Flutter: Build apps for any screen*. https://flutter.dev

Windmill, E. (2020). *Flutter in action*. Manning Publications.

---

*Formato de citación: APA 7.a edición.*
*Documento generado como plantilla para la Sesión 2 del Taller de Nuevas Tecnologías del Desarrollo.*
