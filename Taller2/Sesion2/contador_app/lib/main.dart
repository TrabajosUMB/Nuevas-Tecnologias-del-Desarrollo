import 'package:flutter/material.dart';

/// Punto de entrada de la aplicación.
void main() {
  runApp(const CounterApp());
}

/// Widget raíz de la aplicación.
/// Configura el tema global con Material 3 y lanza la pantalla principal.
class CounterApp extends StatelessWidget {
  const CounterApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Contador App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
      ),
      home: const PantallaContador(),
    );
  }
}

/// Pantalla principal con estado mutable.
///
/// Funcionalidades:
/// - Incrementa el contador con el botón principal (+).
/// - Reinicia el contador a 0 con el botón de reinicio.
/// - Cambia el fondo a verde claro cuando el contador es múltiplo de 5 y > 0.
class PantallaContador extends StatefulWidget {
  const PantallaContador({super.key});

  @override
  State<PantallaContador> createState() => _PantallaContadorState();
}

class _PantallaContadorState extends State<PantallaContador> {
  /// Valor actual del contador. Siempre empieza en 0.
  int _contador = 0;

  /// Incrementa el contador en 1 y solicita a Flutter que redibuje el widget.
  void _incrementar() {
    setState(() {
      _contador++;
    });
  }

  /// Reinicia el contador a 0 (funcionalidad nueva de la Sesión 2).
  void _reiniciar() {
    setState(() {
      _contador = 0;
    });
  }

  /// Devuelve el color de fondo según el valor actual del contador.
  ///
  /// Regla: si el contador es múltiplo de 5 Y mayor que 0 → verde claro.
  /// En cualquier otro caso → blanco.
  Color _colorDeFondo() {
    if (_contador > 0 && _contador % 5 == 0) {
      return Colors.lightGreen[100]!;
    }
    return Colors.white;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // El color de fondo cambia dinámicamente según la regla del múltiplo de 5.
      backgroundColor: _colorDeFondo(),

      appBar: AppBar(
        title: const Text('Contador App'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),

      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Etiqueta descriptiva
            const Text(
              'Valor actual del contador:',
              style: TextStyle(fontSize: 20),
            ),
            const SizedBox(height: 12),

            // Número grande que muestra el contador
            Text(
              '$_contador',
              style: const TextStyle(
                fontSize: 64,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 24),

            // Indicador visual del estado especial (múltiplo de 5)
            AnimatedOpacity(
              opacity: (_contador > 0 && _contador % 5 == 0) ? 1.0 : 0.0,
              duration: const Duration(milliseconds: 400),
              child: const Text(
                'Multiplo de 5',
                style: TextStyle(
                  fontSize: 16,
                  color: Colors.green,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ],
        ),
      ),

      // Dos FloatingActionButtons apilados verticalmente con separación.
      // Se usa Column dentro de floatingActionButton para mostrarlos juntos.
      floatingActionButton: Column(
        mainAxisSize: MainAxisSize.min, // ocupa solo el espacio necesario
        children: [
          // Botón de reinicio (NUEVO en Sesión 2)
          FloatingActionButton(
            onPressed: _reiniciar,
            tooltip: 'Reiniciar contador',
            heroTag: 'btn_reiniciar', // heroTag único evita conflictos de animación
            backgroundColor: Colors.redAccent[100],
            child: const Icon(Icons.refresh),
          ),
          const SizedBox(height: 16), // separación visual entre botones

          // Botón principal de incremento
          FloatingActionButton(
            onPressed: _incrementar,
            tooltip: 'Incrementar contador',
            heroTag: 'btn_incrementar',
            child: const Icon(Icons.add),
          ),
        ],
      ),
    );
  }
}
