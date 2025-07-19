import matplotlib.pyplot as plt
from qiskit.visualization import plot_bloch_multivector

def generate_plots(qc, statevector):
    # Quantum Circuit Figure (drawn on our own Figure)
    fig_circuit = plt.figure(figsize=(4, 2))
    ax_circuit = fig_circuit.add_subplot(111)
    qc.draw(output='mpl', ax=ax_circuit)

    # Bloch Sphere Figure (direct from Qiskit)
    fig_bloch = plot_bloch_multivector(statevector, title="Bloch Sphere")
    fig_bloch.set_size_inches(4, 4)  # set size directly

    return fig_circuit, fig_bloch
