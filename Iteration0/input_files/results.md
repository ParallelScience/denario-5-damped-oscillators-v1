# Results: Analytical Deconvolution of Noise-Induced Bias in Energy Decay Dynamics

## 1. Introduction
The accurate characterization of energy dissipation in damped harmonic oscillators is frequently confounded by the presence of stochastic measurement noise. In experimental settings, the observed total energy $E_{total}(t)$ often fails to decay to zero, instead reaching a non-zero noise floor dictated by the variance of the displacement and velocity sensors. This study implemented a deconvolution framework to isolate this noise-induced bias, $\Delta E_{noise}$, and recover the underlying physical dissipation rate $\gamma$.

## 2. Noise Floor Characterization and Bias Correction
The noise floor was characterized by analyzing the late-time signal ($t > 15s$) for each of the 20 oscillators. By performing local linear detrending, we isolated the Gaussian noise components $\sigma_x^2$ and $\sigma_v^2$. The calculated energy bias, $\Delta E_{noise} = 0.5(k\sigma_x^2 + m\sigma_v^2)$, represents the systematic inflation of the energy measurement.

The Signal-to-Noise Ratio (SNR), defined as the ratio of initial energy $E(0)$ to the bias $\Delta E_{noise}$, varied significantly across the oscillator population. Oscillators with low SNR (e.g., Oscillator 3 with SNR $\approx 2.11$ and Oscillator 19 with SNR $\approx 2.32$) exhibited the most pronounced noise-floor effects, where the raw energy signal was dominated by measurement residuals at late times. Conversely, high-SNR oscillators (e.g., Oscillator 11 with SNR $\approx 2616.0$) showed minimal impact from the noise floor, confirming that the correction framework is most critical for low-energy or high-noise regimes.

## 3. Validation of Dissipation Rates
The effectiveness of the deconvolution was assessed by comparing the observed damping rate $\gamma_{obs}$, derived from non-linear least-squares fitting of the corrected energy $E_{corrected}(t)$, against the theoretical damping rate $\gamma_{theory} = b / (2m)$.

### 3.1 Quantitative Summary
The statistical aggregation of the residuals ($\gamma_{obs} - \gamma_{theory}$) across all 20 oscillators yielded the following metrics:

| Metric | Value |
| :--- | :--- |
| Mean Residual | $0.0082 \text{ rad/s}$ |
| Standard Deviation of Residuals | $0.0197 \text{ rad/s}$ |

The distribution of residuals, as visualized in the diagnostic histogram, is centered near zero, indicating that the deconvolution framework successfully removes the systematic bias without introducing significant skew into the damping rate estimation.

## 4. Discussion and Interpretation
The comparison between $\gamma_{obs}$ and $\gamma_{theory}$ demonstrates a strong linear correlation, with the majority of oscillators falling along the ideal identity line. The slight positive mean residual ($0.0082 \text{ rad/s}$) suggests a minor overestimation of the damping rate, likely attributable to the sensitivity of the exponential fit to the clipping function $\max(0, E_{corrected}(t))$ at very low energy levels.

The diagnostic plots for Oscillators 1, 10, and 20 confirm that the raw energy signal exhibits a persistent plateau at late times, which is effectively eliminated by the bias correction. The corrected energy trajectories show a clean exponential decay toward zero, consistent with the theoretical model of an underdamped system.

## 5. Conclusion
The proposed framework provides a robust and computationally efficient method for decoupling physical energy dissipation from measurement-induced noise. By utilizing late-time signal statistics to derive an oscillator-specific bias term, we have demonstrated that it is possible to recover accurate damping rates even in systems with low SNR. This methodology is highly scalable and provides a rigorous diagnostic tool for validating energy conservation models in experimental physics, ensuring that observed energy residuals are correctly attributed to measurement limitations rather than physical anomalies. Future work could extend this approach to non-Gaussian noise environments or systems with time-varying damping coefficients.