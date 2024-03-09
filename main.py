# Importăm modulele necesare
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import transpile
from qiskit_aer import Aer
from qiskit.tools.visualization import plot_histogram
from matplotlib import pyplot as plt

# Definim numarul pe care îl cautam
search_number = 5

# Initializam registrele cuantice și clasice
quantum_register = QuantumRegister(3)
classical_register = ClassicalRegister(3)
quantum_circuit = QuantumCircuit(quantum_register, classical_register)

# cautam doua stari marcate: |101> și |110>

# Aplicam operaaia Hadamard pe toate qubiturile
quantum_circuit.h(quantum_register)
quantum_circuit.barrier()

# Definim oracle-ul pe baza nr căutat
# Presupunand o secventa binara, oracle-ul marchează starea |101> pentru search_number = 5
if search_number == 5:
    quantum_circuit.cz(quantum_register[2], quantum_register[0])
    quantum_circuit.cz(quantum_register[2], quantum_register[1])

# Inversare in jurul mediei
quantum_circuit.h(quantum_register)
quantum_circuit.x(quantum_register)
quantum_circuit.barrier()
quantum_circuit.h(quantum_register[2])
quantum_circuit.ccx(quantum_register[0], quantum_register[1], quantum_register[2])
quantum_circuit.h(quantum_register[2])
quantum_circuit.barrier()
quantum_circuit.x(quantum_register)
quantum_circuit.h(quantum_register)

# Implementam operatorul Grover
grover_iterations = 3
for _ in range(grover_iterations):
    # Aplicam oracle-ul
    if search_number == 5:
        quantum_circuit.cz(quantum_register[2], quantum_register[0])
        quantum_circuit.cz(quantum_register[2], quantum_register[1])

    # Aplicam operatorul de difuzie
    quantum_circuit.h(quantum_register)
    quantum_circuit.x(quantum_register)
    quantum_circuit.barrier()
    quantum_circuit.h(quantum_register[2])
    quantum_circuit.ccx(quantum_register[0], quantum_register[1], quantum_register[2])
    quantum_circuit.h(quantum_register[2])
    quantum_circuit.barrier()
    quantum_circuit.x(quantum_register)
    quantum_circuit.h(quantum_register)

# Masurare
quantum_circuit.measure(quantum_register, classical_register)

# Rulam circuitul cu un simulator local
local_simulator = Aer.get_backend(name='qasm_simulator')
shots = 1024

# Transpilam circuitul pentru simulatorul local
transpiled_circuit = transpile(quantum_circuit, local_simulator)

# Executam circuitul transpilat
execution = local_simulator.run(transpiled_circuit, shots=shots)

# Obtinem rezultatele
results = execution.result()
answer = results.get_counts(quantum_circuit)

print(answer)

plot_histogram(answer)
plt.show()

import qiskit.providers.ibmq as ibmq

# Salvam contul pentru IBMQ
ibmq.IBMQ.save_account(
    'dc973ffdb6451d24af97665be6076fc428ae68ae37a63ac2237ff8d4bc1fa136201961ae42a5a2b1bc9e61aea332583136732cbb22df7fbccd90ca9507e65e77')
ibmq.IBMQ.load_account()
provider = ibmq.IBMQ.get_provider('ibm-q')
qcomp = provider.get_backend('ibmq_16_melbourne')
job = transpile(quantum_circuit, qcomp)

# Obtinem rezultatele din IBMQ
rez = job.result()
plot_histogram(rez.get_counts(quantum_circuit))
plt.show()
