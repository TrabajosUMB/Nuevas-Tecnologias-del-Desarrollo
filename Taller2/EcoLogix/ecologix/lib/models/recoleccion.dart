import 'package:cloud_firestore/cloud_firestore.dart';

/// Tipos de material electrónico permitidos en el sistema.
/// Se usa como valores del campo tipoMaterial en Firestore.
const List<String> tiposMaterial = [
  'Celular',
  'Laptop',
  'Tablet',
  'Cable',
  'Batería',
  'Otro',
];

/// Modelo de dominio que representa una recolección de residuos electrónicos.
///
/// Corresponde a un documento en la colección 'recolecciones' de Firestore.
class Recoleccion {
  const Recoleccion({
    required this.id,
    required this.tipoMaterial,
    required this.pesoKg,
    required this.ubicacion,
    required this.fecha,
    required this.timestamp,
  });

  /// Identificador único del documento en Firestore.
  final String id;

  /// Tipo de residuo electrónico. Debe ser uno de [tiposMaterial].
  final String tipoMaterial;

  /// Peso del material recolectado en kilogramos. Debe ser mayor que 0.
  final double pesoKg;

  /// Lugar donde se realizó la recolección. No puede estar vacío.
  final String ubicacion;

  /// Fecha en que el usuario registra la recolección (seleccionada en el form).
  final DateTime fecha;

  /// Marca de tiempo del servidor al momento de guardar en Firestore.
  final DateTime timestamp;

  // ---------------------------------------------------------------------------
  // Serialización
  // ---------------------------------------------------------------------------

  /// Convierte la instancia a un mapa compatible con Firestore.
  /// El campo 'timestamp' se guarda como FieldValue para usar el reloj del servidor.
  Map<String, dynamic> toMap() {
    return {
      'tipoMaterial': tipoMaterial,
      'pesoKg': pesoKg,
      'ubicacion': ubicacion,
      'fecha': Timestamp.fromDate(fecha),
      'timestamp': FieldValue.serverTimestamp(),
    };
  }

  /// Construye una instancia desde un mapa proveniente de Firestore.
  /// [id] debe pasarse por separado porque viene del DocumentSnapshot.
  factory Recoleccion.fromMap(String id, Map<String, dynamic> mapa) {
    return Recoleccion(
      id: id,
      tipoMaterial: mapa['tipoMaterial'] as String? ?? 'Otro',
      pesoKg: (mapa['pesoKg'] as num?)?.toDouble() ?? 0.0,
      ubicacion: mapa['ubicacion'] as String? ?? '',
      fecha: (mapa['fecha'] as Timestamp?)?.toDate() ?? DateTime.now(),
      timestamp: (mapa['timestamp'] as Timestamp?)?.toDate() ?? DateTime.now(),
    );
  }

  /// Construye una instancia directamente desde un [DocumentSnapshot] de Firestore.
  factory Recoleccion.fromFirestore(DocumentSnapshot doc) {
    final datos = doc.data() as Map<String, dynamic>? ?? {};
    return Recoleccion.fromMap(doc.id, datos);
  }

  // ---------------------------------------------------------------------------
  // Utilidades
  // ---------------------------------------------------------------------------

  /// Crea una copia de la recolección con campos modificados.
  Recoleccion copyWith({
    String? id,
    String? tipoMaterial,
    double? pesoKg,
    String? ubicacion,
    DateTime? fecha,
    DateTime? timestamp,
  }) {
    return Recoleccion(
      id: id ?? this.id,
      tipoMaterial: tipoMaterial ?? this.tipoMaterial,
      pesoKg: pesoKg ?? this.pesoKg,
      ubicacion: ubicacion ?? this.ubicacion,
      fecha: fecha ?? this.fecha,
      timestamp: timestamp ?? this.timestamp,
    );
  }

  @override
  String toString() {
    return 'Recoleccion(id: $id, tipo: $tipoMaterial, peso: ${pesoKg}kg, '
        'ubicacion: $ubicacion, fecha: $fecha)';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Recoleccion && other.id == id;
  }

  @override
  int get hashCode => id.hashCode;
}
