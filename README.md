# Nuevas Tecnologías del Desarrollo

**Estudiante:** Santiago Rodriguez Angel  
**Semestre:** 2026-02  
**Asignatura:** Nuevas Tecnologías del Desarrollo de Software

---

## Estructura del repositorio

```
Nuevas-Tecnologias-del-Desarrollo/
├── Guia 1/        ← Trabajo autónomo: app React Native
├── Lab1/          ← Laboratorio 1: app Ionic + Angular
└── Taller2/       ← Taller 2: apps Flutter (3 sesiones)
```

---

## Guia 1 — Aplicación Multiplataforma con React Native

**Framework:** React Native + Expo SDK v57  
**Documento:** `Informe_Trabajo_Autonomo_Guia1_Multiplataforma.docx`

App de **conversor de temperatura** (Celsius, Fahrenheit, Kelvin) que corre en Android e iOS desde una única base de código en JavaScript.

| Carpeta | Contenido |
|---|---|
| `AppMultiplataforma/` | Código fuente de la app (Expo) |

**Cómo ejecutar:**
```bash
cd "Guia 1/AppMultiplataforma"
npx expo start
```
Escanear el QR con la app **Expo Go** en el celular (misma red Wi-Fi).

---

## Lab1 — Comparador de Tecnologías con Ionic + Angular

**Framework:** Ionic + Angular + Capacitor  
**Documento:** `Lab1_Multiplataforma_Grupo6.docx`

App multiplataforma **TechCompareApp** que permite comparar tecnologías de desarrollo (React Native, Flutter, Ionic, Xamarin, etc.) con información detallada de cada una, organizada en pestañas.

| Carpeta | Contenido |
|---|---|
| `TechCompareApp/` | Código fuente de la app (Ionic + Angular) |

**Cómo ejecutar:**
```bash
cd Lab1/TechCompareApp
npm install
ionic serve
```

---

## Taller 2 — Desarrollo con Flutter

El taller cubre tres sesiones progresivas, todas en Flutter/Dart.

### Sesion 1 — Contador básico

**Carpeta:** `Taller2/Sesion1/contador_app/`  
**Informe:** `Taller2/Informe_Sesiones_1_y_2.md`

App `StatefulWidget` simple con un `FloatingActionButton` que incrementa un contador numérico. Introducción al ciclo de vida de widgets y `setState()`.

```bash
cd Taller2/Sesion1/contador_app
flutter run
```

---

### Sesion 2 — Contador ampliado

**Carpeta:** `Taller2/Sesion2/contador_app/`  
**Informe:** `Taller2/Sesion2/contador_app/informe/informe_sesion2.md`  
**Presentación:** `Taller2/Sesion2_Taller_Flutter_Entregable-1.pptx`

Versión extendida del contador con:
- Botón de **reinicio** (icono refresh, color rojo).
- **Cambio dinámico de color** de fondo (verde claro en múltiplos de 5).
- `AnimatedOpacity` para transición suave del indicador.

```bash
cd Taller2/Sesion2/contador_app
flutter run
```

---

### EcoLogix — Sistema de trazabilidad de residuos electrónicos

**Carpeta:** `Taller2/EcoLogix/ecologix/`  
**Informe:** `Taller2/Informe_EcoLogix.md`  
**Presentación:** `Taller2/Sesion1_Taller_Flutter_App_Multiplataforma-1.pptx`  
**Caso de estudio:** `Taller2/📑 2 Caso de Estudio.docx`

App Flutter conectada a **Firebase Cloud Firestore** para registrar y consultar recolecciones de e-waste en tiempo real.

**Funcionalidades principales:**
- Registro de recolecciones (tipo de material, peso, ubicación, fecha).
- Validación en dos capas: formulario UI + servicio `FirebaseService`.
- Lista en tiempo real mediante `StreamBuilder` con total acumulado en kg.
- Timestamps del servidor (`FieldValue.serverTimestamp()`) para garantizar orden cronológico.

**Arquitectura:**
```
HomeScreen / RegistroScreen / ListaScreen
              ↓
         FirebaseService   (Patrón Repositorio)
              ↓
       Firebase Cloud Firestore
```

```bash
cd Taller2/EcoLogix/ecologix
flutter pub get
flutter run
```

> Requiere un archivo `google-services.json` válido del proyecto Firebase configurado.

---

## Requisitos generales

| Herramienta | Versión mínima |
|---|---|
| Node.js | 22+ |
| Flutter SDK | 3.0.0 |
| Dart SDK | 3.0.0 |
| Expo Go (celular) | Cualquier versión reciente |
| Ionic CLI | 7+ |
