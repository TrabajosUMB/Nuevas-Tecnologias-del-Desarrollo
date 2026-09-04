# EcoLogix: Sistema de Trazabilidad para Reciclaje de Residuos Electrónicos

**Informe de Caso de Estudio — Taller de Nuevas Tecnologías del Desarrollo**

---

| Campo | Detalle |
|---|---|
| **Institución** | Universidad — Facultad de Ingeniería |
| **Asignatura** | Nuevas Tecnologías del Desarrollo |
| **Semestre** | 2026-02 |
| **Fecha de entrega** | Septiembre 2026 |
| **Estudiante** | [Nombre del Estudiante] |

---

## 1. Introducción

El crecimiento acelerado del sector tecnológico ha generado un problema ambiental crítico: los residuos de aparatos eléctricos y electrónicos (RAEE), comúnmente llamados *e-waste*. Según el Informe Global de Residuos Electrónicos (Forti et al., 2020), en 2019 se generaron 53,6 millones de toneladas métricas de e-waste a nivel mundial, de las cuales solo el 17,4 % fue recolectado y reciclado formalmente. Componentes como baterías de litio, circuitos impresos y pantallas LCD contienen metales pesados (plomo, mercurio, cadmio) que, sin una gestión adecuada, contaminan suelos y aguas subterráneas durante décadas.

En Colombia, la Resolución 1297 de 2010 del Ministerio de Ambiente establece obligaciones para gestores de RAEE, pero la trazabilidad de la cadena de recolección sigue siendo un desafío: muchas startups del sector operan con hojas de cálculo o registros en papel, lo que impide auditorías eficientes y genera pérdida de información.

**EcoLogix** es una aplicación móvil desarrollada en Flutter que permite a los operadores de una startup de reciclaje registrar cada recolección de residuos electrónicos en tiempo real, con sincronización automática en la nube mediante Firebase Firestore. El objetivo es demostrar cómo las tecnologías modernas de desarrollo multiplataforma pueden resolver problemas reales de trazabilidad con bajo costo de implementación.

---

## 2. Marco Teórico

### 2.1 Flutter y Dart

Flutter es un framework de código abierto desarrollado por Google para construir aplicaciones nativas compiladas desde una única base de código para Android, iOS, web y escritorio (Google, 2018). Utiliza el lenguaje Dart, orientado a objetos con tipado estático y soporte nativo para programación asíncrona mediante `async/await` y `Future`/`Stream`.

A diferencia de frameworks híbridos como React Native —que renderizan componentes nativos de cada plataforma—, Flutter compila directamente a código ARM e incluye su propio motor de renderizado basado en Skia/Impeller. Esto proporciona un rendimiento consistente de 60/120 fps independiente del sistema operativo (Windmill, 2020).

La versión 3.x de Flutter, utilizada en este proyecto, introduce **Material 3** (también llamado Material You), el sistema de diseño visual de Google con paletas de colores dinámicas y componentes rediseñados que mejoran la accesibilidad y la coherencia visual.

### 2.2 Firebase Firestore

Cloud Firestore es una base de datos NoSQL orientada a documentos, ofrecida como servicio gestionado por Google en su plataforma Firebase (Google Firebase, 2017). Sus características principales relevantes para EcoLogix son:

- **Sincronización en tiempo real:** Los clientes suscriben a colecciones mediante `snapshots()`, que emite un nuevo evento cada vez que un documento cambia en el servidor, sin necesidad de polling.
- **Modelo de datos flexible:** Los documentos son mapas clave-valor que pueden anidar sub-colecciones, adaptándose a esquemas evolutivos sin migraciones costosas.
- **SDK multiplataforma:** Las bibliotecas `firebase_core` y `cloud_firestore` para Flutter permiten usar la misma API en Android e iOS.
- **Seguridad declarativa:** Las reglas de Firebase (Security Rules) definen quién puede leer y escribir cada colección mediante expresiones declarativas evaluadas en el servidor.

### 2.3 Arquitectura Cliente-Servidor

EcoLogix sigue una arquitectura cliente-servidor simplificada: la aplicación Flutter actúa como cliente que consume los servicios de Firestore (servidor gestionado). El patrón de diseño adoptado es el **Patrón de Repositorio** (Repository Pattern), donde `FirebaseService` encapsula toda la lógica de acceso a Firestore, y las pantallas solo interactúan con esta abstracción. Esto facilita el reemplazo de Firestore por otra fuente de datos sin afectar la interfaz de usuario.

### 2.4 Blockchain: Introducción

Blockchain es una estructura de datos distribuida donde la información se organiza en bloques enlazados criptográficamente. Cada bloque contiene: un conjunto de transacciones, un timestamp, y el hash SHA-256 del bloque anterior. Esta cadena hace que cualquier modificación retrospectiva invalide todos los bloques posteriores, garantizando la inmutabilidad del registro (Nakamoto, 2008).

En el contexto de trazabilidad de residuos, Blockchain permite crear un registro de cadena de custodia verificable por terceros sin depender de una autoridad central. Plataformas como Hyperledger Fabric (Linux Foundation, 2016) están diseñadas para casos de uso empresariales con privacidad selectiva y alto rendimiento.

---

## 3. Descripción de la Solución

### 3.1 Arquitectura de EcoLogix

```
┌─────────────────────────────────────────┐
│           Aplicación Flutter            │
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌───────┐ │
│  │   Home   │  │ Registro │  │ Lista │ │
│  │  Screen  │  │  Screen  │  │Screen │ │
│  └────┬─────┘  └────┬─────┘  └───┬───┘ │
│       │              │             │     │
│       └──────────────┼─────────────┘    │
│                      │                  │
│             ┌─────────────────┐         │
│             │ FirebaseService │         │
│             └────────┬────────┘         │
│                      │                  │
└──────────────────────┼──────────────────┘
                       │ SDK Cloud Firestore
               ┌───────▼────────┐
               │ Firebase Cloud │
               │   Firestore    │
               │  (colección:   │
               │  recolecciones)│
               └────────────────┘
```

### 3.2 Modelo de Datos

Cada documento en la colección `recolecciones` de Firestore tiene la siguiente estructura:

| Campo | Tipo Firestore | Descripción |
|---|---|---|
| `tipoMaterial` | `String` | Uno de: Celular, Laptop, Tablet, Cable, Batería, Otro |
| `pesoKg` | `Number` | Peso en kilogramos (`> 0`, `< 1000`) |
| `ubicacion` | `String` | Dirección o descripción del lugar (`>= 3 chars`) |
| `fecha` | `Timestamp` | Fecha seleccionada por el usuario en el formulario |
| `timestamp` | `Timestamp` | Fecha/hora del servidor al momento de guardar (FieldValue.serverTimestamp()) |

El campo `timestamp` usa `FieldValue.serverTimestamp()` en lugar del reloj del dispositivo, lo que garantiza consistencia aunque el dispositivo tenga la hora incorrecta.

### 3.3 Pantallas

**HomeScreen** — Pantalla de bienvenida con el logo de reciclaje, el nombre de la app y dos botones de navegación. Diseño minimalista sobre fondo blanco para transmitir limpieza y profesionalismo.

**RegistroScreen** — Formulario de captura con cuatro campos: `DropdownButtonFormField` para el tipo de material (enum de 6 opciones), `TextFormField` numérico para el peso, `TextFormField` de texto para la ubicación, y un selector de fecha nativo. El formulario usa `GlobalKey<FormState>` para validación centralizada.

**ListaScreen** — Vista de lista en tiempo real usando `StreamBuilder`. Al tope muestra un banner con el total acumulado de kilogramos reciclados. Cada recolección se renderiza en una `Card` con ícono según el tipo de material, peso, ubicación y fecha formateada. Maneja explícitamente tres estados: carga, vacío y error.

---

## 4. Implementación

### 4.1 Módulo de Modelo (`lib/models/recoleccion.dart`)

La clase `Recoleccion` es inmutable (todos los campos son `final`). Implementa los métodos `toMap()` para serialización, `fromMap()` para deserialización desde un `Map<String, dynamic>`, y `fromFirestore()` como factory constructor que recibe un `DocumentSnapshot`. El método `copyWith()` permite crear instancias modificadas sin mutar el original, siguiendo el principio de inmutabilidad del proyecto.

### 4.2 Módulo de Servicio (`lib/services/firebase_service.dart`)

`FirebaseService` encapsula toda la interacción con Firestore. El método `getRecolecciones()` devuelve un `Stream<List<Recoleccion>>` mapeando los `QuerySnapshot` de Firestore. El método `agregarRecoleccion()` primero invoca `_validar()` —que lanza `RecoleccionInvalidaException` si alguna regla falla— y luego ejecuta `docRef.set()` dentro de un bloque `try/on FirebaseException`. La validación en el servicio es independiente de la validación del formulario para garantizar integridad incluso si el servicio se consume desde otras capas.

### 4.3 Módulo de Pantallas (`lib/screens/`)

Cada pantalla sigue el principio de responsabilidad única. `HomeScreen` es un `StatelessWidget` que solo navega. `RegistroScreen` es un `StatefulWidget` que mantiene el estado del formulario y del indicador de carga. `ListaScreen` es `StatelessWidget` porque delega el estado al `StreamBuilder`. Los subwidgets privados (`_BotonPrincipal`, `_TarjetaRecoleccion`, `_EstadoVacio`, `_EstadoError`, `_BannerTotal`) se extraen como clases separadas para mantener el método `build` de cada pantalla legible y bajo el límite de 50 líneas por función.

### 4.4 Inicialización de Firebase (`lib/main.dart` y `lib/firebase_options.dart`)

`main()` es `async` y llama `WidgetsFlutterBinding.ensureInitialized()` antes de `Firebase.initializeApp()`. Las credenciales se referencian desde `firebase_options.dart`, que es un archivo placeholder con instrucciones para el estudiante. El archivo real debe generarse con `flutterfire configure` y nunca debe subirse a un repositorio público.

---

## 5. Resultados

### 5.1 Capturas de Pantalla del Backend (Firebase Console)

*(Insertar aquí capturas de pantalla de la consola de Firebase mostrando:)*

1. **Colección `recolecciones`** en Firestore con al menos 3 documentos de prueba.
2. **Detalle de un documento** mostrando los campos `tipoMaterial`, `pesoKg`, `ubicacion`, `fecha` y `timestamp`.
3. **Reglas de Seguridad** de Firestore configuradas.

### 5.2 Capturas de Pantalla de la Aplicación

*(Insertar aquí capturas del emulador Android o dispositivo físico mostrando:)*

1. **HomeScreen** con el logo y los botones de navegación.
2. **RegistroScreen** con el formulario completado.
3. **ListaScreen** con el banner de total y al menos 3 tarjetas de recolección.
4. **ListaScreen** en estado vacío (sin registros).

---

## 6. Análisis de Seguridad

El análisis completo de seguridad se desarrolla en el documento adjunto `pitch_seguridad.md`. A continuación se presenta un resumen ejecutivo:

**Medidas implementadas en EcoLogix:**
- Validación de datos en dos capas independientes (formulario y servicio).
- Manejo explícito de `FirebaseException` con mensajes amigables para el usuario.
- Verificación de `context.mounted` para evitar fugas de memoria tras operaciones asíncronas.
- Credenciales de Firebase en archivo separado no incluido en control de versiones.

**Vulnerabilidades de la arquitectura centralizada:**
- Dependencia en la disponibilidad de Google Firebase (single point of failure).
- El administrador del proyecto tiene acceso irrestricto a los datos.
- No existe auditoría inmutable integrada.

**Ventaja de Blockchain:**
- Inmutabilidad criptográfica del historial de recolecciones.
- Trazabilidad verificable por terceros sin acceso administrativo.
- Eliminación del riesgo de alteración de registros por actores internos.

**Recomendación:** Firebase es adecuado para la etapa actual de la startup. Para cumplimiento regulatorio futuro, se recomienda implementar un ancla de hash (hash anchoring) periódica en una red pública como Ethereum o Polygon, donde el hash raíz del historial de Firestore se registra en la cadena sin necesidad de migrar toda la arquitectura.

---

## 7. Conclusiones

1. Flutter con Firebase Firestore permite construir una aplicación de trazabilidad funcional con sincronización en tiempo real en menos de 5 archivos de código, lo que demuestra la productividad del stack para startups con recursos limitados.

2. La arquitectura en capas (modelo → servicio → pantalla) facilita el mantenimiento y la evolución del sistema. Agregar nuevos tipos de material o campos al modelo requiere cambios mínimos y localizados.

3. La validación en múltiples capas (cliente + servicio) es una práctica esencial: el formulario mejora la experiencia del usuario con retroalimentación inmediata, mientras que la validación del servicio garantiza integridad en caso de consumo programático.

4. Las bases de datos centralizadas como Firestore son idóneas para MVPs y aplicaciones de consumo masivo, pero presentan limitaciones en contextos que requieren auditoría inmutable e independiente, como el reporte de gestión ambiental ante reguladores.

5. Blockchain no es una solución universal; su adopción debe evaluarse frente al costo operativo y la complejidad de implementación. Para EcoLogix, un enfoque híbrido (Firestore + hash anchoring periódico en Blockchain) ofrece el mejor balance entre costo y garantías de integridad.

---

## 8. Referencias

Forti, V., Baldé, C. P., Kuehr, R., & Bel, G. (2020). *The global e-waste monitor 2020: Quantities, flows and the circular economy potential*. United Nations University / United Nations Institute for Training and Research. https://www.itu.int/en/ITU-D/Environment/Pages/Spotlight/Global-Ewaste-Monitor-2020.aspx

Google. (2018). *Flutter — Build apps for any screen*. https://flutter.dev

Google Firebase. (2017). *Cloud Firestore documentation*. https://firebase.google.com/docs/firestore

Linux Foundation. (2016). *Hyperledger Fabric*. https://www.hyperledger.org/use/fabric

Ministerio de Ambiente, Vivienda y Desarrollo Territorial de Colombia. (2010). *Resolución 1297 de 2010: Por la cual se establecen los Sistemas de Recolección Selectiva y Gestión Ambiental de Residuos de Pilas y/o Acumuladores y se adoptan otras disposiciones*. Diario Oficial de Colombia.

Nakamoto, S. (2008). *Bitcoin: A peer-to-peer electronic cash system*. https://bitcoin.org/bitcoin.pdf

Windmill, E. (2020). *Flutter in action*. Manning Publications.

---

*Documento generado como parte del Taller de Nuevas Tecnologías del Desarrollo — Semestre 2026-02*
