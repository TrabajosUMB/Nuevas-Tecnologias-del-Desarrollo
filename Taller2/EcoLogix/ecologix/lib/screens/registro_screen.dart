import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:intl/intl.dart';
import 'package:uuid/uuid.dart';

import '../models/recoleccion.dart';
import '../services/firebase_service.dart';

/// Pantalla de registro de una nueva recolección de residuos electrónicos.
///
/// Valida los campos antes de persistir en Firestore mediante [FirebaseService].
class RegistroScreen extends StatefulWidget {
  const RegistroScreen({super.key});

  @override
  State<RegistroScreen> createState() => _RegistroScreenState();
}

class _RegistroScreenState extends State<RegistroScreen> {
  // ---------------------------------------------------------------------------
  // Estado del formulario
  // ---------------------------------------------------------------------------
  final _formKey = GlobalKey<FormState>();
  final _servicio = FirebaseService();
  final _uuid = const Uuid();

  String? _tipoMaterial;
  final _controladorPeso = TextEditingController();
  final _controladorUbicacion = TextEditingController();
  DateTime _fechaSeleccionada = DateTime.now();

  bool _guardando = false;

  // ---------------------------------------------------------------------------
  // Ciclo de vida
  // ---------------------------------------------------------------------------

  @override
  void dispose() {
    _controladorPeso.dispose();
    _controladorUbicacion.dispose();
    super.dispose();
  }

  // ---------------------------------------------------------------------------
  // Acciones
  // ---------------------------------------------------------------------------

  /// Abre el selector de fecha del sistema operativo.
  Future<void> _seleccionarFecha() async {
    final hoy = DateTime.now();
    final fechaElegida = await showDatePicker(
      context: context,
      initialDate: _fechaSeleccionada,
      firstDate: DateTime(2020),
      lastDate: hoy,
      helpText: 'Seleccionar fecha de recolección',
      cancelText: 'Cancelar',
      confirmText: 'Confirmar',
    );

    if (fechaElegida != null) {
      setState(() => _fechaSeleccionada = fechaElegida);
    }
  }

  /// Valida el formulario y guarda la recolección en Firestore.
  Future<void> _guardarRecoleccion() async {
    // Cierra el teclado antes de procesar.
    FocusScope.of(context).unfocus();

    if (!(_formKey.currentState?.validate() ?? false)) return;

    setState(() => _guardando = true);

    final nuevaRecoleccion = Recoleccion(
      id: _uuid.v4(),
      tipoMaterial: _tipoMaterial!,
      pesoKg: double.parse(_controladorPeso.text.trim()),
      ubicacion: _controladorUbicacion.text.trim(),
      fecha: _fechaSeleccionada,
      timestamp: DateTime.now(),
    );

    try {
      await _servicio.agregarRecoleccion(nuevaRecoleccion);

      // Verificamos que el widget siga montado antes de usar el contexto.
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Recolección guardada correctamente.'),
          backgroundColor: Colors.green,
          behavior: SnackBarBehavior.floating,
        ),
      );

      Navigator.of(context).pop();
    } on RecoleccionInvalidaException catch (e) {
      if (!mounted) return;
      _mostrarErrorSnackBar('Dato inválido: ${e.mensaje}');
    } on FirebaseException catch (e) {
      if (!mounted) return;
      _mostrarErrorSnackBar(
        e.message ?? 'Error de conexión con Firebase. Intenta de nuevo.',
      );
    } on Exception catch (e) {
      if (!mounted) return;
      _mostrarErrorSnackBar('Error inesperado: $e');
    } finally {
      if (mounted) setState(() => _guardando = false);
    }
  }

  void _mostrarErrorSnackBar(String mensaje) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(mensaje),
        backgroundColor: Colors.red[700],
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  // ---------------------------------------------------------------------------
  // UI
  // ---------------------------------------------------------------------------

  @override
  Widget build(BuildContext context) {
    final colores = Theme.of(context).colorScheme;
    final formatoFecha = DateFormat('dd/MM/yyyy', 'es');

    return Scaffold(
      appBar: AppBar(
        backgroundColor: colores.primary,
        foregroundColor: Colors.white,
        title: const Text('Nueva Recolección'),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // ---------------------------------------------------------------
              // Tipo de material
              // ---------------------------------------------------------------
              _EtiquetaCampo(texto: 'Tipo de material *'),
              const SizedBox(height: 8),
              DropdownButtonFormField<String>(
                value: _tipoMaterial,
                decoration: _decoracion('Selecciona el tipo'),
                items: tiposMaterial
                    .map(
                      (tipo) => DropdownMenuItem<String>(
                        value: tipo,
                        child: Text(tipo),
                      ),
                    )
                    .toList(),
                onChanged: (valor) => setState(() => _tipoMaterial = valor),
                validator: (valor) =>
                    valor == null ? 'Selecciona un tipo de material' : null,
              ),
              const SizedBox(height: 20),

              // ---------------------------------------------------------------
              // Peso en kg
              // ---------------------------------------------------------------
              _EtiquetaCampo(texto: 'Peso (kg) *'),
              const SizedBox(height: 8),
              TextFormField(
                controller: _controladorPeso,
                decoration: _decoracion('Ej. 2.5'),
                keyboardType: const TextInputType.numberWithOptions(
                  decimal: true,
                  signed: false,
                ),
                inputFormatters: [
                  // Permite solo números y un punto decimal
                  FilteringTextInputFormatter.allow(RegExp(r'^\d*\.?\d*')),
                ],
                validator: (valor) {
                  if (valor == null || valor.trim().isEmpty) {
                    return 'El peso es obligatorio';
                  }
                  final peso = double.tryParse(valor.trim());
                  if (peso == null) return 'Ingresa un número válido';
                  if (peso <= 0) return 'El peso debe ser mayor que cero';
                  if (peso >= 1000) return 'El peso no puede superar 1000 kg';
                  return null;
                },
              ),
              const SizedBox(height: 20),

              // ---------------------------------------------------------------
              // Ubicación
              // ---------------------------------------------------------------
              _EtiquetaCampo(texto: 'Ubicación *'),
              const SizedBox(height: 8),
              TextFormField(
                controller: _controladorUbicacion,
                decoration: _decoracion('Ej. Calle 10 # 5-23, Bogotá'),
                textCapitalization: TextCapitalization.sentences,
                maxLength: 200,
                validator: (valor) {
                  final texto = valor?.trim() ?? '';
                  if (texto.isEmpty) return 'La ubicación es obligatoria';
                  if (texto.length < 3) {
                    return 'La ubicación debe tener al menos 3 caracteres';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 20),

              // ---------------------------------------------------------------
              // Fecha de recolección
              // ---------------------------------------------------------------
              _EtiquetaCampo(texto: 'Fecha de recolección *'),
              const SizedBox(height: 8),
              InkWell(
                onTap: _seleccionarFecha,
                borderRadius: BorderRadius.circular(12),
                child: InputDecorator(
                  decoration: _decoracion(''),
                  child: Row(
                    children: [
                      Icon(Icons.calendar_today, color: colores.primary),
                      const SizedBox(width: 12),
                      Text(
                        formatoFecha.format(_fechaSeleccionada),
                        style: const TextStyle(fontSize: 16),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 36),

              // ---------------------------------------------------------------
              // Botón guardar / indicador de carga
              // ---------------------------------------------------------------
              _guardando
                  ? const Center(child: CircularProgressIndicator())
                  : ElevatedButton.icon(
                      onPressed: _guardarRecoleccion,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: colores.primary,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(14),
                        ),
                      ),
                      icon: const Icon(Icons.save_outlined),
                      label: const Text(
                        'Guardar Recolección',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
            ],
          ),
        ),
      ),
    );
  }

  InputDecoration _decoracion(String pista) {
    return InputDecoration(
      hintText: pista,
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
      contentPadding: const EdgeInsets.symmetric(
        horizontal: 16,
        vertical: 14,
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Componente privado: etiqueta de campo
// ---------------------------------------------------------------------------

class _EtiquetaCampo extends StatelessWidget {
  const _EtiquetaCampo({required this.texto});
  final String texto;

  @override
  Widget build(BuildContext context) {
    return Text(
      texto,
      style: const TextStyle(
        fontSize: 14,
        fontWeight: FontWeight.w600,
        color: Colors.black87,
      ),
    );
  }
}
