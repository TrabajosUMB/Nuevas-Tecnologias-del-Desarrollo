# Guía No. 1 — Aplicaciones Multiplataforma Híbridas

**Asignatura:** Nuevas Tecnologías del Desarrollo de Software  
**Estudiante:** Santiago Rodriguez Angel  
**IDE:** Visual Studio Code  
**Framework:** React Native + Expo SDK v57  

---

## Aplicación: Conversor de Temperatura

App multiplataforma que convierte entre escalas de temperatura (Celsius, Fahrenheit, Kelvin). Corre en **Android** e **iOS** desde una única base de código en JavaScript.

### Plataformas soportadas

| Plataforma | Método de ejecución |
|---|---|
| Android | Expo Go (Play Store) |
| iOS | Expo Go (App Store) |

---

## Cómo ejecutar

### Requisitos
- Node.js v22+
- App **Expo Go** instalada en el celular
- PC y celular en la **misma red Wi-Fi**

### Pasos

```bash
cd AppMultiplataforma
npx expo start
```

Escanear el QR con Expo Go → la app carga en el celular.

---

## Estructura del proyecto

```
AppMultiplataforma/
├── App.js          ← Código principal de la app
├── app.json        ← Configuración de Expo
├── package.json    ← Dependencias
└── assets/         ← Íconos e imágenes
```

---

## Respuestas de la guía

Ver archivo [`RESPUESTAS_GUIA_1.md`](./RESPUESTAS_GUIA_1.md) con todas las actividades de trabajo autónomo resueltas.
