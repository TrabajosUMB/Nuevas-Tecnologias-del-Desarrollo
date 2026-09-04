import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';

import 'firebase_options.dart';
import 'screens/home_screen.dart';

/// Punto de entrada de la aplicación EcoLogix.
/// Inicializa Firebase antes de arrancar la interfaz.
void main() async {
  // Garantiza que los bindings de Flutter estén listos antes de inicializar Firebase.
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  runApp(const EcoLogixApp());
}

/// Widget raíz de la aplicación.
class EcoLogixApp extends StatelessWidget {
  const EcoLogixApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'EcoLogix',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.green,
          brightness: Brightness.light,
        ),
        useMaterial3: true,
        // Tipografía consistente en toda la app
        textTheme: const TextTheme(
          headlineLarge: TextStyle(fontWeight: FontWeight.bold),
          headlineMedium: TextStyle(fontWeight: FontWeight.w600),
        ),
      ),
      home: const HomeScreen(),
    );
  }
}
