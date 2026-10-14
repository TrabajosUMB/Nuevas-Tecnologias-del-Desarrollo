// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;  // version del compilador

contract MiPrimerContrato {

    // Variable de estado: se guarda en la blockchain
    string public mensaje;
    address public propietario;
    uint public contador;

    // Constructor: se ejecuta UNA sola vez al desplegarse
    constructor(string memory _mensajeInicial) {
        mensaje = _mensajeInicial;
        propietario = msg.sender;  // quien despliega el contrato
        contador = 0;
    }

    // Funcion para cambiar el mensaje
    function cambiarMensaje(string memory _nuevoMensaje) public {
        mensaje = _nuevoMensaje;
        contador++;
    }

    // Funcion de solo lectura (no gasta gas)
    function obtenerContador() public view returns (uint) {
        return contador;
    }
}
