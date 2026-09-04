import 'package:flutter/material.dart';

import 'lista_screen.dart';
import 'registro_screen.dart';

/// Pantalla principal de EcoLogix.
///
/// Presenta la identidad visual de la app y los dos accesos primarios:
/// registrar una nueva recolección o consultar el historial.
class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final colores = Theme.of(context).colorScheme;
    final textos = Theme.of(context).textTheme;

    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 32.0, vertical: 24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Spacer(flex: 2),

              // ---------------------------------------------------------------
              // Logo e identidad visual
              // ---------------------------------------------------------------
              Icon(
                Icons.recycling,
                size: 100,
                color: colores.primary,
                semanticLabel: 'Icono de reciclaje EcoLogix',
              ),
              const SizedBox(height: 24),

              Text(
                'EcoLogix',
                textAlign: TextAlign.center,
                style: textos.headlineLarge?.copyWith(
                  color: colores.primary,
                  fontSize: 40,
                  letterSpacing: 1.5,
                ),
              ),
              const SizedBox(height: 8),

              Text(
                'Trazabilidad de Residuos Electrónicos',
                textAlign: TextAlign.center,
                style: textos.titleMedium?.copyWith(
                  color: Colors.grey[600],
                  fontStyle: FontStyle.italic,
                ),
              ),

              const Spacer(flex: 3),

              // ---------------------------------------------------------------
              // Acciones principales
              // ---------------------------------------------------------------
              _BotonPrincipal(
                etiqueta: 'Registrar Recolección',
                icono: Icons.add_circle_outline,
                onPressed: () => _navegarA(
                  context,
                  const RegistroScreen(),
                ),
              ),
              const SizedBox(height: 16),

              _BotonPrincipal(
                etiqueta: 'Ver Recolecciones',
                icono: Icons.list_alt,
                esSecundario: true,
                onPressed: () => _navegarA(
                  context,
                  const ListaScreen(),
                ),
              ),

              const Spacer(flex: 2),

              // ---------------------------------------------------------------
              // Pie de versión
              // ---------------------------------------------------------------
              Text(
                'v1.0.0  ·  EcoLogix © 2026',
                textAlign: TextAlign.center,
                style: textos.bodySmall?.copyWith(color: Colors.grey[400]),
              ),
              const SizedBox(height: 8),
            ],
          ),
        ),
      ),
    );
  }

  void _navegarA(BuildContext context, Widget pantalla) {
    Navigator.push(
      context,
      MaterialPageRoute<void>(builder: (_) => pantalla),
    );
  }
}

// ---------------------------------------------------------------------------
// Componente privado: botón de acción principal
// ---------------------------------------------------------------------------

class _BotonPrincipal extends StatelessWidget {
  const _BotonPrincipal({
    required this.etiqueta,
    required this.icono,
    required this.onPressed,
    this.esSecundario = false,
  });

  final String etiqueta;
  final IconData icono;
  final VoidCallback onPressed;

  /// Si es `true`, se renderiza como botón outlined en lugar de filled.
  final bool esSecundario;

  @override
  Widget build(BuildContext context) {
    final colores = Theme.of(context).colorScheme;

    final estilo = ElevatedButton.styleFrom(
      padding: const EdgeInsets.symmetric(vertical: 18),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
        side: esSecundario
            ? BorderSide(color: colores.primary, width: 2)
            : BorderSide.none,
      ),
      backgroundColor: esSecundario ? Colors.white : colores.primary,
      foregroundColor: esSecundario ? colores.primary : Colors.white,
      elevation: esSecundario ? 0 : 3,
    );

    return ElevatedButton.icon(
      style: estilo,
      onPressed: onPressed,
      icon: Icon(icono, size: 22),
      label: Text(
        etiqueta,
        style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
      ),
    );
  }
}
