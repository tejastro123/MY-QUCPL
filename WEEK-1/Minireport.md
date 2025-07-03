# What is a Qubit?
Quantum bit or also called as "qubit" in short, is analogous to clasical bit. In classical computing information is encoded in the form of bits, where each bit has a value of either 0 or 1. In Quantum computing, information is encoded in the form of qubits.It is a two-level quantum system where the two basis qubit states are written as  ∣0⟩ and ∣1⟩ ( read as ket o and ket 1).A qubit can be in state ∣0⟩, ∣1⟩ or (unlike a classical bit) in a linear combination of both states. The name of this phenomenon is superposition.
# Superposition 
It allows quantum algorithms to process information in a fraction of the time it would take even the fastest classical systems to solve certain problems.The amount of information a qubit system can represent grows exponentially. Information that 500 qubits can easily represent would not be possible with even more than 2^500 classical bits.

  A general -pure- qubit state is expressed as: ∣ψ⟩=α∣0⟩+β∣1⟩ 

where α and β are the complex probability amplitudes for each basis state. Note that the choice of basis states is arbitrary, each set of orthogonal states can be used as basis states.On the quantum level, qubit probability is measured as a wave function. The probability amplitude of a qubit can be used to encode more than one bit of data and carry out extremely complex calculations when combined with other qubits.When processing a complex problem, such as factoring a large prime number, traditional bits become bound up by holding large quantities of information. Quantum bits behave differently. Because qubits can hold a superposition, a quantum computer that uses qubits can calculate a much larger volume of data.

# Interference
A consequence of superposition is interference. Qubit states can interfere with each other because each state is described by a probability amplitude, just like the amplitudes of waves.

Constructive interference enhances amplitude, while destructive interference cancels out amplitude. These effects are used in quantum computing algorithms, which make them fundamentally different from classical algorithms. Interference is used together with entanglement to enable the quantum acceleration promised by quantum computation

# Entanglement
Multiple qubits can exhibit quantum entanglement. Entangled qubits always correlate with each other to form a single system. Even when they're infinitely far apart, measuring the state of one of the qubits allows us to know the state of the other, without needing to measure it directly.It is required for any quantum computation and it cannot be efficiently performed on a classical computer. Applications include factoring large numbers (Shor's algorithm) and solving search problems (Grover's algorithm).


As any two-level quantum system can be used to create a qubit, there are many types of qubits currently being developed by researchers—and certain qubits are better suited to certain applications.

 1) Superconducting
Made from superconducting materials operating at extremely low temperatures, superconducting qubits are manipulated by microwave pulses and are a favorite among quantum computer scientists for their relatively robust coherence.

 2) Trapped ions
Using sophisticated laser technology, trapped ion particles can also be used as qubits. Trapped ion qubits are noteworthy for long coherence times as well as high-fidelity measurements.

 3) Quantum dots
A quantum dot is a small semiconductor capable of capturing a single electron and using it as a qubit. Quantum dot qubits can be manipulated by using magnetic fields and are particularly interesting to researchers for their potential scalability and compatibility with existing semiconductor technology.

 4) Photons
By setting and measuring the directional spin states of individual light particles, photon qubits can be used to send quantum information across long distances through optical fiber cables and are currently being used in quantum communication and quantum cryptography.

 5) Neutral atoms
Commonly occurring neutral atoms are defined by a balanced positive and negative charge ionic charge. Using lasers, these atoms can be charged with energy into various excited states, any two of which can be used to create a qubit that is well suited for scaling up and performing operations.

# Challenges of Qubit
While powerful, qubits are also very temperamental. To function, qubits must be cooled to a temperature only a fraction of a degree higher than absolute zero, which is colder than outer space.Entanglement of the qubit system with its environment, including the measurement setup, could easily perturb the system and cause decoherence.

Even under the coldest conditions, qubit systems are also generally susceptible to failure caused by decoherence. Thankfully, advancements in the emerging field of algorithmic quantum error correction have the potential to stabilize previously tenuous quantum systems