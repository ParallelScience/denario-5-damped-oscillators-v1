# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.integrate import trapezoid
from scipy.optimize import curve_fit
from step_1 import exponential_decay

if __name__ == '__main__':
    data = np.load("/home/node/data/damped_oscillators.npy", allow_pickle=False)
    corrected_energy = np.load("data/corrected_energy.npy", allow_pickle=False)
    osc_ids = np.unique(data['oscillator_id'])
    num_oscs = len(osc_ids)
    gamma_theory = np.zeros(num_oscs)
    gamma_obs = np.zeros(num_oscs)
    integrated_energy = np.zeros(num_oscs)
    for i, osc_id in enumerate(osc_ids):
        mask = data['oscillator_id'] == osc_id
        osc_data = data[mask]
        t = osc_data['time']
        m = osc_data['mass_kg'][0]
        b = osc_data['damping_coefficient'][0]
        gamma_theory[i] = b / (2.0 * m)
        e_corr = corrected_energy[mask]
        popt, _ = curve_fit(exponential_decay, t, e_corr, p0=[e_corr[0], gamma_theory[i]])
        gamma_obs[i] = popt[1]
        integrated_energy[i] = trapezoid(e_corr, t)
    residuals = gamma_obs - gamma_theory
    print("Mean Residual (gamma_obs - gamma_theory): " + str(np.mean(residuals)))
    print("Std Dev of Residuals: " + str(np.std(residuals)))
    results = np.rec.fromarrays([osc_ids, gamma_theory, gamma_obs, residuals, integrated_energy], names='osc_id,gamma_theory,gamma_obs,residuals,integrated_energy')
    np.save("data/validation_metrics.npy", results)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.scatter(gamma_theory, gamma_obs, color='blue', alpha=0.7)
    ax1.plot([min(gamma_theory), max(gamma_theory)], [min(gamma_theory), max(gamma_theory)], 'k--', label='Ideal')
    ax1.set_xlabel("Theoretical Damping Rate (rad/s)")
    ax1.set_ylabel("Observed Damping Rate (rad/s)")
    ax1.set_title("Damping Rate Comparison")
    ax1.grid(True)
    ax1.legend()
    ax2.hist(residuals, bins=10, color='green', alpha=0.7, edgecolor='black')
    ax2.set_xlabel("Residual (rad/s)")
    ax2.set_ylabel("Frequency")
    ax2.set_title("Distribution of Damping Rate Residuals")
    ax2.grid(True)
    plt.tight_layout()
    timestamp = int(time.time())
    plot_path = os.path.join("data", "validation_plots_" + str(timestamp) + ".png")
    plt.savefig(plot_path, dpi=300)
    print("Validation plots saved to " + plot_path)