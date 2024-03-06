from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import transpile, IBMQ
from qiskit_aer import Aer

# IBMQ.save_account('dc973ffdb6451d24af97665be6076fc428ae68ae37a63ac2237ff8d4bc1fa136201961ae42a5a2b1bc9e61aea332583136732cbb22df7fbccd90ca9507e65e77')
# provider = IBMQ.load_account()
# backends = provider.backends()
# print(backends)


quantum_register = QuantumRegister(3)  # Initialize qubits
classical_register = ClassicalRegister(3)  # Initialize bits for record measurements
quantum_circuit = QuantumCircuit(quantum_register, classical_register)

# We want to search two marked states
# |101> and |110>

# Apply Hadamard to all qubits
quantum_circuit.h(quantum_register)
quantum_circuit.barrier()

# Phase oracle (Marks states |101> and |110> as results)
quantum_circuit.cz(quantum_register[2], quantum_register[0])
quantum_circuit.cz(quantum_register[2], quantum_register[1])

# Inversion around the average
quantum_circuit.h(quantum_register)
quantum_circuit.x(quantum_register)
quantum_circuit.barrier()
quantum_circuit.h(quantum_register[2])
quantum_circuit.ccx(quantum_register[0], quantum_register[1], quantum_register[2])
quantum_circuit.h(quantum_register[2])
quantum_circuit.barrier()
quantum_circuit.x(quantum_register)
quantum_circuit.h(quantum_register)

# Measure
quantum_circuit.measure(quantum_register, classical_register)

# Run our circuit with local simulator
local_simulator = Aer.get_backend(name='qasm_simulator')
shots = 1024
# Transpile the circuit for the local_simulator
transpiled_circuit = transpile(quantum_circuit, local_simulator)

# Execute the transpiled circuit
execution = local_simulator.run(transpiled_circuit, shots=shots)

# Retrieve the results
results = execution.result()
answer = results.get_counts()
print(answer)

#TODO: implement IBMQ + see if there are all items implemented