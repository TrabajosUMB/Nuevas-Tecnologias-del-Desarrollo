import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../models/recoleccion.dart';
import '../services/firebase_service.dart';

/// Pantalla que muestra el historial de recolecciones en tiempo real.
///
/// Escucha un [Stream] de Firestore y actualiza la lista automáticamente.
class ListaScreen extends StatelessWidget {
  const ListaScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final colores = Theme.of(context).colorScheme;
    final servicio = FirebaseService();

    return Scaffold(
      appBar: AppBar(
        backgroundColor: colores.primary,
        foregroundColor: Colors.white,
        title: const Text('Recolecciones'),
        centerTitle: true,
      ),
      body: StreamBuilder<List<Recoleccion>>(
        stream: servicio.getRecolecciones(),
        builder: (context, snapshot) {
          // ---------------------------------------------------------------
          // Estado: cargando la primera respuesta
          // ---------------------------------------------------------------
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          // ---------------------------------------------------------------
          // Estado: error de Firestore
          // ---------------------------------------------------------------
          if (snapshot.hasError) {
            return _EstadoError(mensaje: snapshot.error.toString());
          }

          final recolecciones = snapshot.data ?? [];

          // ---------------------------------------------------------------
          // Estado: lista vacía
          // ---------------------------------------------------------------
          if (recolecciones.isEmpty) {
            return const _EstadoVacio();
          }

          // ---------------------------------------------------------------
          // Estado: lista con datos
          // ---------------------------------------------------------------
          final totalKg = recolecciones.fold<double>(
            0,
            (acumulado, r) => acumulado + r.pesoKg,
          );

          return Column(
            children: [
              _BannerTotal(totalKg: totalKg),
              Expanded(
                child: ListView.builder(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 8,
                  ),
                  itemCount: recolecciones.length,
                  itemBuilder: (context, indice) {
                    return _TarjetaRecoleccion(
                      recoleccion: recolecciones[indice],
                    );
                  },
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Banner con el total de kg reciclados
// ---------------------------------------------------------------------------

class _BannerTotal extends StatelessWidget {
  const _BannerTotal({required this.totalKg});
  final double totalKg;

  @override
  Widget build(BuildContext context) {
    final colores = Theme.of(context).colorScheme;
    final formatoKg = NumberFormat('#,##0.##', 'es');

    return Container(
      width: double.infinity,
      color: colores.primaryContainer,
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
      child: Row(
        children: [
          Icon(Icons.eco, color: colores.onPrimaryContainer, size: 28),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Total reciclado',
                  style: TextStyle(
                    color: colores.onPrimaryContainer,
                    fontSize: 12,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                Text(
                  '${formatoKg.format(totalKg)} kg',
                  style: TextStyle(
                    color: colores.onPrimaryContainer,
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Tarjeta individual de recolección
// ---------------------------------------------------------------------------

class _TarjetaRecoleccion extends StatelessWidget {
  const _TarjetaRecoleccion({required this.recoleccion});
  final Recoleccion recoleccion;

  @override
  Widget build(BuildContext context) {
    final colores = Theme.of(context).colorScheme;
    final formatoFecha = DateFormat('dd MMM yyyy', 'es');
    final formatoKg = NumberFormat('#,##0.##', 'es');

    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      child: Padding(
        padding: const EdgeInsets.all(14.0),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Ícono según tipo de material
            CircleAvatar(
              radius: 24,
              backgroundColor: colores.primaryContainer,
              child: Icon(
                _iconoParaTipo(recoleccion.tipoMaterial),
                color: colores.primary,
                size: 26,
              ),
            ),
            const SizedBox(width: 14),

            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Tipo de material
                  Text(
                    recoleccion.tipoMaterial,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),

                  // Peso
                  _InfoFila(
                    icono: Icons.scale,
                    texto: '${formatoKg.format(recoleccion.pesoKg)} kg',
                  ),
                  const SizedBox(height: 2),

                  // Ubicación
                  _InfoFila(
                    icono: Icons.location_on_outlined,
                    texto: recoleccion.ubicacion,
                  ),
                  const SizedBox(height: 2),

                  // Fecha
                  _InfoFila(
                    icono: Icons.calendar_today_outlined,
                    texto: formatoFecha.format(recoleccion.fecha),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  /// Devuelve el ícono que mejor representa cada tipo de material electrónico.
  IconData _iconoParaTipo(String tipo) {
    return switch (tipo) {
      'Celular' => Icons.smartphone,
      'Laptop' => Icons.laptop,
      'Tablet' => Icons.tablet,
      'Cable' => Icons.cable,
      'Batería' => Icons.battery_full,
      _ => Icons.devices_other,
    };
  }
}

/// Fila de información con ícono pequeño a la izquierda.
class _InfoFila extends StatelessWidget {
  const _InfoFila({required this.icono, required this.texto});
  final IconData icono;
  final String texto;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(icono, size: 14, color: Colors.grey[600]),
        const SizedBox(width: 4),
        Expanded(
          child: Text(
            texto,
            style: TextStyle(fontSize: 13, color: Colors.grey[700]),
            overflow: TextOverflow.ellipsis,
          ),
        ),
      ],
    );
  }
}

// ---------------------------------------------------------------------------
// Estado vacío
// ---------------------------------------------------------------------------

class _EstadoVacio extends StatelessWidget {
  const _EstadoVacio();

  @override
  Widget build(BuildContext context) {
    final colores = Theme.of(context).colorScheme;

    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.inbox_outlined,
              size: 80,
              color: colores.primary.withOpacity(0.4),
            ),
            const SizedBox(height: 16),
            Text(
              'No hay recolecciones registradas',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.w500,
                color: Colors.grey[600],
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Presiona el botón "Registrar Recolección" en la pantalla principal.',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 14, color: Colors.grey[500]),
            ),
          ],
        ),
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Estado de error
// ---------------------------------------------------------------------------

class _EstadoError extends StatelessWidget {
  const _EstadoError({required this.mensaje});
  final String mensaje;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.cloud_off, size: 72, color: Colors.red),
            const SizedBox(height: 16),
            const Text(
              'No se pudo cargar la información',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.w600,
                color: Colors.red,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              mensaje,
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 13, color: Colors.grey[600]),
            ),
            const SizedBox(height: 16),
            Text(
              'Verifica tu conexión a internet o revisa las reglas de '
              'seguridad de Firestore.',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 13, color: Colors.grey[500]),
            ),
          ],
        ),
      ),
    );
  }
}
