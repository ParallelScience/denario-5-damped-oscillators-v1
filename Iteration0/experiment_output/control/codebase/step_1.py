# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time
import os

def exponential_decay(t, e0, gamma_obs):
    return e0 * np.exp(-2 * gamma_obs * t)

if __name__ == '__main__':
    data = np.load("/home/node/data/damped_oscillators.npy", allow_pickle=False)
    osc_ids = np.unique(data['oscillator_id'])
    num_oscs = len(osc_ids)
    corrected_energy = np.zeros_like(data['total_energy'])
    gamma_obs_list = np.zeros(num_oscs)
    snr_list = np.zeros(num_oscs)
    for i, osc_id in enumerate(osc_ids):
        mask = data['oscillator_id'] == osc_id
        osc_data = data[mask]
        t = osc_data['time']
        x = osc_data['displacement']
        v = osc_data['velocity']
        m = osc_data['mass_kg'][0]
        k = osc_data['spring_constant'][0]
        e_total = osc_data['total_energy']
        late_mask = t > 15.0
        x_late = x[late_mask]
        v_late = v[late_mask]
        p_x = np.polyfit(t[late_mask], x_late, 1)
        p_v = np.polyfit(t[late_mask], v_late, 1)
        sigma_x2 = np.var(x_late - np.polyval(p_x, t[late_mask]))
        sigma_v2 = np.var(v_late - np.polyval(p_v, t[late_mask]))
        delta_e = 0.5 * (k * sigma_x2 + m * sigma_v2)
        e_corr = np.maximum(0, e_total - delta_e)
        corrected_energy[mask] = e_corr
        snr = e_total[0] / delta_e if delta_e > 0 else np.inf
        snr_list[i] = snr
        popt, _ = curve_fit(exponential_decay, t, e_corr, p0=[e_total[0], 0.1])
        gamma_obs_list[i] = popt[1]
        print("Oscillator " + str(osc_id) + ": SNR = " + str(round(snr, 2)) + ", Gamma_obs = " + str(round(popt[1], 4)))
    np.save("data/corrected_energy.npy", corrected_energy)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for idx, osc_id in enumerate([1, 10, 20]):
        mask = data['oscillator_id'] == osc_id
        ax = axes[idx]
        ax.plot(data['time'][mask], data['total_energy'][mask], label='Raw Energy', alpha=0.5)
        ax.plot(data['time'][mask], corrected_energy[mask], label='Corrected Energy', color='red')
        ax.set_title("Oscillator " + str(osc_id))
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Energy (J)")
        ax.legend()
        ax.grid(True)
    plt.tight_layout()
    timestamp = int(time.time())
    plot_path = os.path.join("data", "energy_correction_summary_" + str(timestamp) + ".png")
    plt.savefig(plot_path, dpi=300)
    print("Summary plot saved to " + plot_path)