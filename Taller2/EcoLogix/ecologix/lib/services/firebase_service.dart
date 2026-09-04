import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:uuid/uuid.dart';

import '../models/recoleccion.dart';

/// Excepción lanzada cuando los datos de una recolección son inválidos.
class RecoleccionInvalidaException implements Exception {
  const RecoleccionInvalidaException(this.mensaje);
  final String mensaje;

  @override
  String toString() => 'RecoleccionInvalidaException: $mensaje';
}

/// Servicio de acceso a datos de Firebase Firestore.
///
/// Centraliza todas las operaciones sobre la colección 'recolecciones'.
class FirebaseService {
  FirebaseService({FirebaseFirestore? firestore})
      : _firestore = firestore ?? FirebaseFirestore.instance;

  final FirebaseFirestore _firestore;
  final _uuid = const Uuid();

  /// Nombre de la colección en Firestore.
  static const String _coleccion = 'recolecciones';

  // ---------------------------------------------------------------------------
  // Lectura en tiempo real
  // ---------------------------------------------------------------------------

  /// Devuelve un [Stream] con la lista de recolecciones ordenadas por timestamp
  /// descendente. La escucha se actualiza automáticamente cada vez que Firestore
  /// emite cambios.
  Stream<List<Recoleccion>> getRecolecciones() {
    return _firestore
        .collection(_coleccion)
        .orderBy('timestamp', descending: true)
        .snapshots()
        .map(
          (snapshot) => snapshot.docs
              .map(Recoleccion.fromFirestore)
              .toList(),
        );
  }

  // ---------------------------------------------------------------------------
  // Escritura
  // ---------------------------------------------------------------------------

  /// Valida y guarda una [Recoleccion] en Firestore.
  ///
  /// Lanza [RecoleccionInvalidaException] si los datos no cumplen las reglas
  /// de negocio. Lanza [FirebaseException] si ocurre un error de red o permisos.
  Future<void> agregarRecoleccion(Recoleccion recoleccion) async {
    _validar(recoleccion);

    // Genera un ID único si el modelo no trae uno (campo vacío o placeholder).
    final idFinal = recoleccion.id.isEmpty
        ? _uuid.v4()
        : recoleccion.id;

    final docRef = _firestore.collection(_coleccion).doc(idFinal);

    try {
      await docRef.set(recoleccion.toMap());
    } on FirebaseException catch (e) {
      // Relanzamos con contexto adicional para que la UI pueda mostrar
      // un mensaje descriptivo sin exponer detalles técnicos al usuario.
      throw FirebaseException(
        plugin: e.plugin,
        code: e.code,
        message: 'No se pudo guardar la recolección: ${e.message}',
      );
    }
  }

  // ---------------------------------------------------------------------------
  // Validación
  // ---------------------------------------------------------------------------

  /// Valida las reglas de negocio antes de persistir.
  void _validar(Recoleccion r) {
    if (!tiposMaterial.contains(r.tipoMaterial)) {
      throw const RecoleccionInvalidaException(
        'El tipo de material no es válido.',
      );
    }

    if (r.pesoKg <= 0) {
      throw const RecoleccionInvalidaException(
        'El peso debe ser mayor que cero.',
      );
    }

    if (r.pesoKg >= 1000) {
      throw const RecoleccionInvalidaException(
        'El peso no puede superar 1000 kg.',
      );
    }

    final ubicacionLimpia = r.ubicacion.trim();
    if (ubicacionLimpia.isEmpty) {
      throw const RecoleccionInvalidaException(
        'La ubicación no puede estar vacía.',
      );
    }

    if (ubicacionLimpia.length < 3) {
      throw const RecoleccionInvalidaException(
        'La ubicación debe tener al menos 3 caracteres.',
      );
    }
  }
}
