// INSTRUCCIONES PARA EL ESTUDIANTE:
// ============================================================
// Este archivo es un PLACEHOLDER. Para ejecutar la aplicación:
//
// 1. Crea un proyecto en Firebase Console (https://console.firebase.google.com)
// 2. Agrega una app Android con el package name: com.example.ecologix
// 3. Descarga el archivo google-services.json y colócalo en:
//    android/app/google-services.json
// 4. Instala la CLI de Firebase: npm install -g firebase-tools
// 5. Ejecuta: dart pub global activate flutterfire_cli
// 6. Ejecuta: flutterfire configure
//    Este comando regenerará este archivo automáticamente con tus credenciales.
//
// NUNCA subas las credenciales reales a un repositorio público.
// ============================================================

import 'package:firebase_core/firebase_core.dart' show FirebaseOptions;
import 'package:flutter/foundation.dart'
    show defaultTargetPlatform, kIsWeb, TargetPlatform;

/// Opciones de Firebase generadas por FlutterFire CLI.
/// Ejecuta: flutterfire configure
class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    if (kIsWeb) {
      throw UnsupportedError(
        'DefaultFirebaseOptions no está configurado para web. '
        'Ejecuta flutterfire configure para generar este archivo.',
      );
    }
    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return android;
      case TargetPlatform.iOS:
        throw UnsupportedError(
          'DefaultFirebaseOptions no está configurado para iOS. '
          'Ejecuta flutterfire configure para generar este archivo.',
        );
      default:
        throw UnsupportedError(
          'DefaultFirebaseOptions no está disponible para esta plataforma.',
        );
    }
  }

  /// REEMPLAZA estos valores con los de tu proyecto Firebase.
  /// Los obtienes ejecutando: flutterfire configure
  static const FirebaseOptions android = FirebaseOptions(
    apiKey: 'TU_API_KEY_AQUI',
    appId: 'TU_APP_ID_AQUI',
    messagingSenderId: 'TU_SENDER_ID_AQUI',
    projectId: 'TU_PROJECT_ID_AQUI',
    storageBucket: 'TU_STORAGE_BUCKET_AQUI',
  );
}
