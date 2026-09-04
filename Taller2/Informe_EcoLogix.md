# EcoLogix: Sistema de Trazabilidad para Reciclaje de Residuos Electrónicos

**Informe de Caso de Estudio — Taller de Nuevas Tecnologías del Desarrollo**

---

| Campo | Detalle |
|---|---|
| **Institución** | Universidad — Facultad de Ingeniería |
| **Asignatura** | Nuevas Tecnologías del Desarrollo |
| **Semestre** | 2026-02 |
| **Fecha de entrega** | 2 de septiembre de 2026 |
| **Estudiante** | [Nombre del Estudiante] |
| **Código** | [Código estudiantil] |

---

## 1. Introducción

El crecimiento acelerado del sector tecnológico ha generado un problema ambiental crítico: los residuos de aparatos eléctricos y electrónicos (RAEE), comúnmente llamados *e-waste*. Según el Informe Global de Residuos Electrónicos (Forti et al., 2020), en 2019 se generaron 53,6 millones de toneladas métricas de e-waste a nivel mundial, de las cuales solo el 17,4 % fue recolectado y reciclado formalmente.

En Colombia, la Resolución 1297 de 2010 del Ministerio de Ambiente establece obligaciones para gestores de RAEE, pero la trazabilidad de la cadena de recolección sigue siendo un desafío: muchas startups operan con hojas de cálculo o registros en papel, lo que impide auditorías eficientes.

**EcoLogix** es una aplicación móvil desarrollada en Flutter que permite registrar cada recolección de residuos electrónicos en tiempo real, con sincronización automática en la nube mediante Firebase Firestore.

---

## 2. Marco Teórico

### 2.1 Flutter y Dart

Flutter es un framework de código abierto de Google para construir aplicaciones nativas compiladas desde una única base de código para Android, iOS, Web y escritorio (Google, 2018). A diferencia de React Native, Flutter compila directamente a código ARM e incluye su propio motor de renderizado (Skia/Impeller), garantizando 60/120 fps independiente del sistema operativo.

### 2.2 Firebase Cloud Firestore

Cloud Firestore es una base de datos NoSQL orientada a documentos ofrecida por Google Firebase. Sus características más relevantes para EcoLogix son:

- **Sincronización en tiempo real:** Los clientes suscriben colecciones mediante `snapshots()`, que emite un evento nuevo por cada cambio en el servidor sin polling.
- **Modelo de datos flexible:** Documentos como mapas clave-valor, sin migraciones costosas.
- **SDK multiplataforma:** Las bibliotecas `firebase_core` y `cloud_firestore` para Flutter funcionan igual en Android e iOS.
- **Seguridad declarativa:** Las Security Rules de Firebase controlan quién puede leer/escribir cada colección.

### 2.3 Arquitectura y Patrón de Repositorio

EcoLogix usa arquitectura cliente-servidor simplificada con el **Patrón de Repositorio**: `FirebaseService` encapsula toda la lógica de acceso a Firestore, y las pantallas solo interactúan con esta abstracción. Esto permite reemplazar Firestore por otra fuente de datos sin afectar la UI.

### 2.4 Blockchain: Introducción

Blockchain es una estructura de datos distribuida donde la información se organiza en bloques enlazados criptográficamente mediante hashes SHA-256. Su inmutabilidad garantiza que ningún registro pueda modificarse retrospectivamente sin invalidar toda la cadena (Nakamoto, 2008).

---

## 3. Descripción de la Solución

### 3.1 Arquitectura

```
┌─────────────────────────────────────────┐
│           Aplicación Flutter            │
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌───────┐ │
│  │   Home   │  │ Registro │  │ Lista │ │
│  │  Screen  │  │  Screen  │  │Screen │ │
│  └────┬─────┘  └────┬─────┘  └───┬───┘ │
│       └──────────────┼────────────┘     │
│                      │                  │
│             ┌─────────────────┐         │
│             │ FirebaseService │         │
│             └────────┬────────┘         │
└──────────────────────┼──────────────────┘
                       │ SDK Cloud Firestore
               ┌───────▼────────┐
               │ Firebase Cloud │
               │   Firestore    │
               │  (colección:   │
               │  recolecciones)│
               └────────────────┘
```

### 3.2 Modelo de Datos en Firestore

| Campo | Tipo | Descripción |
|---|---|---|
| `tipoMaterial` | String | Celular, Laptop, Tablet, Cable, Batería, Otro |
| `pesoKg` | Number | Peso en kg (`> 0`, `< 1000`) |
| `ubicacion` | String | Dirección del lugar (`≥ 3 chars`) |
| `fecha` | Timestamp | Fecha seleccionada por el usuario |
| `timestamp` | Timestamp | Reloj del servidor (`FieldValue.serverTimestamp()`) |

---

## 4. Capturas de Pantalla de la Aplicación

### 4.1 Pantalla de Inicio (HomeScreen)

```
╔══════════════════════════════════════╗
║  ←  EcoLogix                  ⋮     ║  ← AppBar verde
╠══════════════════════════════════════╣
║                                      ║
║                  ♻️                  ║  ← Icons.recycling (grande, verde)
║                                      ║
║            E c o L o g i x          ║  ← Título estilizado
║   Trazabilidad de Residuos           ║
║       Electrónicos                   ║  ← Subtítulo
║                                      ║
║  ┌──────────────────────────────┐    ║
║  │  📝  Registrar Recolección   │    ║  ← Botón primario
║  └──────────────────────────────┘    ║
║  ┌──────────────────────────────┐    ║
║  │  📋  Ver Recolecciones       │    ║  ← Botón secundario
║  └──────────────────────────────┘    ║
║                                      ║
╚══════════════════════════════════════╝
```

> **[Insertar aquí captura real de la HomeScreen en el emulador]**

---

### 4.2 Módulo de Registro Completado (RegistroScreen)

A continuación se muestra cómo se ve el formulario con datos reales ingresados:

```
╔══════════════════════════════════════╗
║  ←  Registrar Recolección     ⋮     ║  ← AppBar verde
╠══════════════════════════════════════╣
║                                      ║
║  Tipo de Material                    ║
║  ┌──────────────────────────────┐    ║
║  │  Laptop                   ▼ │    ║  ← DropdownButtonFormField
║  └──────────────────────────────┘    ║     Opciones: Celular | Laptop |
║                                      ║     Tablet | Cable | Batería | Otro
║  Peso (kg)                           ║
║  ┌──────────────────────────────┐    ║
║  │  2.5                         │    ║  ← TextFormField numérico
║  └──────────────────────────────┘    ║     Validación: > 0 y < 1000
║                                      ║
║  Ubicación                           ║
║  ┌──────────────────────────────┐    ║
║  │  Calle 45 # 23-10, Bogotá    │    ║  ← TextFormField texto
║  └──────────────────────────────┘    ║     Validación: ≥ 3 caracteres
║                                      ║
║  Fecha de recolección                ║
║  ┌──────────────────────────────┐    ║
║  │  📅  2 de septiembre de 2026 │    ║  ← DatePicker nativo
║  └──────────────────────────────┘    ║
║                                      ║
║  ┌──────────────────────────────┐    ║
║  │     💾 Guardar Recolección   │    ║  ← Botón de guardado
║  └──────────────────────────────┘    ║
║                                      ║
╚══════════════════════════════════════╝
  Datos ingresados: Laptop | 2.5 kg | Calle 45 #23-10 | 02/09/2026
```

> **[Insertar aquí captura real del formulario con datos ingresados antes de guardar]**

---

### 4.3 Captura del Backend — Firebase Console (Firestore)

Después de presionar "Guardar Recolección", el documento queda almacenado en Firestore. Así se ve la consola de Firebase:

```
┌──────────────────────────────────────────────────────────────────────┐
│  🔥 Firebase Console — Proyecto: ecologix-xxxxx                     │
│  Firestore Database > recolecciones                                  │
├──────────────────────────────────────────────────────────────────────┤
│  📁 recolecciones                                                    │
│  ├── 📄 LkP9xQr2mNvTaBcDeFgH                                        │
│  │        tipoMaterial: "Laptop"                                     │
│  │        pesoKg: 2.5                                                │
│  │        ubicacion: "Calle 45 # 23-10, Bogotá"                     │
│  │        fecha: 2 de septiembre de 2026, 0:00:00 a.m. UTC-5        │
│  │        timestamp: 2 de septiembre de 2026, 14:32:05 UTC-5        │
│  │                                                                    │
│  ├── 📄 MnO8yPs3rQuVwXyZaB  (segundo registro)                      │
│  │        tipoMaterial: "Celular"                                    │
│  │        pesoKg: 0.18                                               │
│  │        ubicacion: "Carrera 7 # 12-45, Bogotá"                    │
│  │        fecha: 2 de septiembre de 2026, 0:00:00 a.m.              │
│  │        timestamp: 2 de septiembre de 2026, 14:45:22 UTC-5        │
│  │                                                                    │
│  └── 📄 RsT4uVw5xYzAbCdEfG  (tercer registro)                       │
│           tipoMaterial: "Cable"                                      │
│           pesoKg: 1.2                                                │
│           ubicacion: "Av. El Dorado # 68-70"                        │
│           fecha: 2 de septiembre de 2026, 0:00:00 a.m.              │
│           timestamp: 2 de septiembre de 2026, 15:10:08 UTC-5        │
└──────────────────────────────────────────────────────────────────────┘
  Total en Firestore: 3 documentos | Total acumulado: 3.88 kg
```

> **[Insertar aquí captura real de la consola de Firebase mostrando los documentos guardados en la colección `recolecciones`]**

---

### 4.4 Lista de Recolecciones en Tiempo Real (ListaScreen)

```
╔══════════════════════════════════════╗
║  ←  Recolecciones             ⋮     ║
╠══════════════════════════════════════╣
║  ┌────────────────────────────────┐  ║
║  │ ♻️  Total reciclado: 3.88 kg   │  ║  ← Banner con total acumulado
║  └────────────────────────────────┘  ║
║                                      ║
║  ┌────────────────────────────────┐  ║
║  │ 💻 Laptop              2.5 kg  │  ║
║  │    Calle 45 # 23-10            │  ║  ← Card recolección 1
║  │    02/09/2026                  │  ║
║  └────────────────────────────────┘  ║
║                                      ║
║  ┌────────────────────────────────┐  ║
║  │ 📱 Celular            0.18 kg  │  ║
║  │    Carrera 7 # 12-45           │  ║  ← Card recolección 2
║  │    02/09/2026                  │  ║
║  └────────────────────────────────┘  ║
║                                      ║
║  ┌────────────────────────────────┐  ║
║  │ 🔌 Cable               1.2 kg  │  ║
║  │    Av. El Dorado # 68-70       │  ║  ← Card recolección 3
║  │    02/09/2026                  │  ║
║  └────────────────────────────────┘  ║
╚══════════════════════════════════════╝
  StreamBuilder: escucha en tiempo real sin polling
```

> **[Insertar aquí captura real de la ListaScreen con los registros cargados desde Firestore]**

---

## 5. Análisis de Integridad

### Pregunta 1: ¿Cómo se aseguró que los datos lleguen correctamente a la base de datos?

EcoLogix implementa **tres capas independientes de protección** para garantizar que solo datos válidos lleguen a Firestore:

#### Capa 1 — Validación en el formulario (UI)

El formulario de registro utiliza `Form` con `GlobalKey<FormState>` y `validator` en cada campo. Antes de que cualquier dato salga hacia el servicio, se ejecuta `_formKey.currentState!.validate()`. Las reglas aplicadas son:

| Campo | Regla de validación |
|---|---|
| `tipoMaterial` | Debe ser uno de los 6 valores del catálogo (Celular, Laptop, Tablet, Cable, Batería, Otro). No puede estar vacío. |
| `pesoKg` | Debe ser un número válido, mayor que 0 y menor que 1000 kg. Rechaza texto, ceros y valores negativos. |
| `ubicacion` | Mínimo 3 caracteres no vacíos. Rechaza espacios en blanco y campos vacíos. |
| `fecha` | Seleccionada mediante `DatePicker` nativo — garantiza siempre una fecha válida. |

Si cualquier campo falla, el formulario muestra el mensaje de error debajo del campo correspondiente y **bloquea el envío** sin mostrar ninguna pantalla de carga.

#### Capa 2 — Validación en el servicio (`FirebaseService._validar`)

Aunque el formulario ya validó, `FirebaseService` repite las mismas reglas de forma **completamente independiente** antes de llamar a Firestore. Esto es una práctica de defensa en profundidad: si en el futuro alguien usa el servicio desde una prueba automatizada, un script o una segunda pantalla que no pase por el formulario, la integridad de los datos sigue garantizada.

```dart
void _validar(Recoleccion r) {
  final materialesValidos = ['Celular', 'Laptop', 'Tablet', 'Cable', 'Batería', 'Otro'];
  if (!materialesValidos.contains(r.tipoMaterial)) {
    throw RecoleccionInvalidaException('Tipo de material no válido.');
  }
  if (r.pesoKg <= 0 || r.pesoKg >= 1000) {
    throw RecoleccionInvalidaException('El peso debe estar entre 0 y 1000 kg.');
  }
  if (r.ubicacion.trim().length < 3) {
    throw RecoleccionInvalidaException('La ubicación es demasiado corta.');
  }
}
```

Si esta validación falla, se lanza `RecoleccionInvalidaException` — un tipo propio que permite distinguir errores de negocio de errores de red.

#### Capa 3 — Manejo explícito de errores de red

La escritura en Firestore se ejecuta dentro de un bloque `try/on FirebaseException`:

```dart
try {
  await docRef.set(recoleccion.toMap());
} on FirebaseException catch (e) {
  throw Exception('Error al guardar: ${e.message}');
}
```

Ningún error se silencia. Los errores de red (sin conexión, token expirado, reglas de seguridad rechazadas) llegan a la UI como un `SnackBar` rojo con el mensaje contextualizado.

#### Garantía adicional: timestamp del servidor

El campo `timestamp` usa `FieldValue.serverTimestamp()` en lugar del reloj del dispositivo:

```dart
'timestamp': FieldValue.serverTimestamp(),
```

Esto garantiza que el orden cronológico de los registros sea correcto aunque el dispositivo tenga la hora mal configurada. El servidor de Firestore siempre es la fuente de verdad para la hora de guardado.

#### Resultado

Un dato llega a Firestore únicamente si:
1. Pasó el `validator` del formulario (UI).
2. Pasó la validación del `FirebaseService` (servicio).
3. La escritura a Firestore no lanzó una excepción de red.

Cualquier falla en cualquiera de los tres pasos cancela la operación y notifica al usuario con un mensaje claro.

---

### Pregunta 2: ¿Por qué una base de datos centralizada es vulnerable si un actor malicioso hackea el acceso?

Una base de datos centralizada como Firebase Firestore concentra **todos los datos en un solo punto de control**. Cuando ese control es comprometido, las consecuencias son graves e irreversibles. Las vulnerabilidades estructurales son:

#### 2.1 Acceso con privilegios absolutos (root)

La cuenta de administrador del proyecto Firebase tiene permisos irrestrictos sobre todos los datos. Si un atacante obtiene las credenciales del administrador —mediante phishing, fuga de claves de API o compromiso del correo corporativo— puede:

- **Leer** todo el historial de recolecciones, incluyendo ubicaciones y fechas.
- **Modificar** los pesos registrados para falsificar estadísticas de reciclaje.
- **Eliminar** registros completos sin dejar rastro auditable en la base de datos misma.
- **Crear** registros falsos que inflen artificialmente los reportes ambientales.

Firestore **no implementa** un log de auditoría inmutable de quién modificó un documento y cuándo — esa información puede ser eliminada con los mismos permisos de administrador.

#### 2.2 Sin inmutabilidad de los registros

En una base de datos relacional o NoSQL tradicional, cualquier usuario con permisos `UPDATE` o `DELETE` puede alterar un registro sin que el sistema registre la versión original. En el contexto de trazabilidad ambiental, esto significa que:

- Un operador deshonesto puede cambiar `pesoKg: 2.5` a `pesoKg: 25.0` para inflar las métricas de reciclaje y recibir más compensación económica.
- Un regulador externo que audite los datos solo ve el valor actual, sin saber que fue modificado.
- La empresa no puede probar ante una autoridad que el registro original no fue alterado.

#### 2.3 Single Point of Failure (SPOF)

Al depender de un único proveedor (Google Firebase), toda la aplicación deja de funcionar si:

- Firebase presenta una interrupción del servicio (ha ocurrido históricamente).
- Google decide descontinuar el servicio (como ocurrió con Google+, Stadia, etc.).
- La cuenta del proyecto es suspendida por violación de términos de servicio.

No existe una réplica independiente fuera del control del proveedor.

#### 2.4 Reglas de seguridad mal configuradas

Si las Security Rules de Firestore quedan en estado permisivo durante el desarrollo:

```javascript
// Regla INSEGURA — permite acceso total
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true; // ← Cualquiera puede leer/escribir
    }
  }
}
```

Cualquier persona que tenga la API key (que está embebida en el archivo `google-services.json` de la app) puede leer y escribir todos los datos sin autenticación. Esta clave es técnicamente visible si alguien descompila el APK.

#### 2.5 Dependencia de terceros y privacidad

Al usar Firebase, los datos de las recolecciones —incluyendo ubicaciones geográficas de los puntos de recolección— residen en servidores de Google en jurisdicciones que pueden estar sujetas a legislaciones de vigilancia (como la CLOUD Act de EE. UU.). Una empresa colombiana con datos ambientales sensibles pierde el control soberano sobre esa información.

#### Resumen de vulnerabilidades

| Vulnerabilidad | Impacto si se explota |
|---|---|
| Credenciales de admin comprometidas | Modificación o eliminación total de registros sin rastro |
| Sin auditoría inmutable | Imposible demostrar integridad ante un regulador |
| SPOF | Pérdida de acceso operacional completa |
| Reglas permisivas | Cualquier usuario puede leer/escribir todos los datos |
| Dependencia de tercero | Pérdida de soberanía sobre los datos ambientales |

---

### Recomendación: Base de Datos Tradicional vs. Blockchain

| Criterio | Firebase (BD Centralizada) | Blockchain (Ej: Hyperledger) |
|---|---|---|
| **Costo operativo** | Bajo (capa gratuita disponible) | Alto (infraestructura de nodos, gas fees) |
| **Velocidad de desarrollo** | Rápida (SDK listo en horas) | Lenta (curva de aprendizaje alta) |
| **Inmutabilidad** | No — los datos pueden modificarse | Sí — criptográficamente garantizada |
| **Auditoría externa** | Requiere acceso de admin | Cualquier nodo puede verificar |
| **Escalabilidad** | Millones de ops/segundo | Cientos a miles por segundo |
| **Adecuado para** | MVPs, validación de producto | Compliance regulatorio, cadena de custodia |

**Recomendación para EcoLogix:** Firebase es la elección correcta para la etapa de startup. A medida que la empresa deba cumplir regulaciones ambientales que exijan auditorías independientes, se recomienda un enfoque **híbrido**: Firestore como capa operacional (rápida y económica) + hash anchoring periódico en Blockchain (Polygon o Hyperledger Fabric) donde el hash raíz del historial se registra en la cadena de forma inmutable. Esto añade garantías regulatorias sin reemplazar toda la arquitectura.

---

## 6. Conclusiones

1. Flutter con Firebase Firestore permite construir una aplicación de trazabilidad funcional con sincronización en tiempo real con menos de 8 archivos de código, demostrando la productividad del stack para startups con recursos limitados.

2. La validación en múltiples capas (formulario + servicio) es esencial: la validación en UI mejora la experiencia del usuario, mientras que la validación en el servicio garantiza integridad independientemente de cómo se llame la capa de negocio.

3. Las bases de datos centralizadas presentan vulnerabilidades estructurales reales en contextos de trazabilidad regulada: ausencia de inmutabilidad, dependencia de un único proveedor, y riesgo de alteración de registros sin auditoría.

4. Blockchain no es una solución universal — su adopción debe evaluarse frente al costo y complejidad. Un enfoque híbrido (BD + hash anchoring en Blockchain) ofrece el mejor balance entre agilidad operacional y garantías de integridad para una startup en crecimiento.

5. El campo `timestamp` con `FieldValue.serverTimestamp()` es un detalle técnico crítico: garantiza la integridad del orden cronológico de los registros independientemente del reloj del dispositivo, un requisito esencial para trazabilidad regulada.

---

## 7. Referencias

Forti, V., Baldé, C. P., Kuehr, R., & Bel, G. (2020). *The global e-waste monitor 2020*. United Nations University. https://www.itu.int/en/ITU-D/Environment/Pages/Spotlight/Global-Ewaste-Monitor-2020.aspx

Google. (2018). *Flutter — Build apps for any screen*. https://flutter.dev

Google Firebase. (2017). *Cloud Firestore documentation*. https://firebase.google.com/docs/firestore

Linux Foundation. (2016). *Hyperledger Fabric*. https://www.hyperledger.org/use/fabric

Ministerio de Ambiente, Vivienda y Desarrollo Territorial de Colombia. (2010). *Resolución 1297 de 2010: Sistemas de Recolección Selectiva y Gestión Ambiental de Residuos de Pilas y/o Acumuladores*. Diario Oficial de Colombia.

Nakamoto, S. (2008). *Bitcoin: A peer-to-peer electronic cash system*. https://bitcoin.org/bitcoin.pdf

Windmill, E. (2020). *Flutter in action*. Manning Publications.

---

*Taller de Nuevas Tecnologías del Desarrollo — Semestre 2026-02 | Formato APA 7.ª edición*
