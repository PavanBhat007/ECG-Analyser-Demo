import adi
import numpy as np
import EntropyHub as EH
import biosppy as bp
from scipy.signal import welch
from scipy.signal import butter, filtfilt
from scipy.integrate import trapezoid

def bandpass_filter(sig, lowcut, highcut, fs, order=1):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, sig)

def extract_ecg_features(adi_file_path):
    data, file_info, params = [], {}, {}
    print(adi_file_path)
    
    try:
        f = adi.read_file(adi_file_path)
        ecg_channel = f.channels[1]
        fs = int(ecg_channel.fs[0])
        
        file_info = {
            'Number of record': ecg_channel.n_records,
            'Number of Rested ECG samples': ecg_channel.n_samples[0],
            'Number of Tilted ECG samples': sum(ecg_channel.n_samples[1:-1]),
            'Tick Rate': ecg_channel.tick_dt[0],
            'Sampling Frequency': fs,
            'Unit': ecg_channel.units[0]
        }
        
        data = np.array(ecg_channel.get_data(1)[:300000]) # 5 minutes of data
    except:
        print("Unable to read file")

    if len(data) != 0:
        ecg_signal = data.flatten()
        ecg_signal = bandpass_filter(ecg_signal, lowcut=0.5, highcut=45, fs=fs, order=4)
        try:
            rpeaks = bp.signals.ecg.engzee_segmenter(signal=ecg_signal, sampling_rate=fs)
            rr = np.diff(rpeaks) / fs

            # HRV Parameters
            if len(rr) > 0:
                heart_rate = 60 / rr
                avg_hr = np.mean(heart_rate)
                mean_rr = np.mean(rr)
                sdrr = np.std(rr)
            else: heart_rate = avg_hr = mean_rr = sdrr = np.nan
            
            hr_diff = np.mean(max(heart_rate) - min(heart_rate))
            hr_diff_percent = np.mean((hr_diff / np.mean(heart_rate)) * 100)

            # Time-domain features
            sdnni = np.mean([np.std(rr[i:i + fs * 5 * 60]) for i in range(0, len(rr), fs * 5 * 60)])
            rmssd = np.sqrt(np.mean(np.square(np.diff(rr))))
            pnn50 = np.sum(np.abs(np.diff(rr)) > 50) / len(rr) * 100

            segment_length = 5 * 60 * fs  # 5-minute segments in samples
            rr_segments = [np.mean(rr[i:i + segment_length]) for i in range(0, len(rr), segment_length)]
            sdann = np.std(rr_segments)

            hrv_triangular_index = len(rr) / np.max(np.histogram(rr, bins=256)[0])
            hist, bin_edges = np.histogram(rr, bins=256)
            max_bin = np.argmax(hist)
            tinn = bin_edges[max_bin + np.argmax(hist[max_bin:] < 0.15 * np.max(hist))] - bin_edges[max_bin]

            # Frequency-domain features using Welch method
            nperseg = min(256, len(rr) // 2)
            if len(rr) > 1:
                f, psd = welch(rr, fs=1.0, nperseg=nperseg) # fs=1.0 => 1Hz

                ulf_power = trapezoid(psd[(f <= 0.003)], f[(f <= 0.003)])
                vlf_power = trapezoid(psd[(f >= 0.0033) & (f <= 0.04)], f[(f >= 0.0033) & (f <= 0.04)])
                lf_power = trapezoid(psd[(f >= 0.04) & (f <= 0.15)], f[(f >= 0.04) & (f <= 0.15)])
                hf_power = trapezoid(psd[(f >= 0.15) & (f <= 0.4)], f[(f >= 0.15) & (f <= 0.4)])
                lf_hf_ratio = lf_power / hf_power

            else:
                ulf_power = vlf_power = lf_power = hf_power = lf_hf_ratio = np.nan

            # Nonlinear features
            sd1 = np.sqrt(np.var(rr) / 2)
            sd2 = np.sqrt(2 * np.var(rr) - sd1 ** 2)

            apen, phi = EH.ApEn(rr, m=2)
            sampen, a, b = EH.SampEn(rr, m=4)

            apen = np.mean(apen)
            sampen = np.mean(sampen)

            params = {
                'avg_heart_rate': avg_hr,
                'mean_rr': mean_rr,
                'std_rr': sdrr,
                # 'hr_diff': hr_diff,
                # 'hr_diff_percent': hr_diff_percent,
                'sdnn': sdrr,
                'sdnni': sdnni,
                'rmssd': rmssd,
                # 'pnn50': pnn50,
                # 'sdann': sdann,
                'hrv_triangular_index': hrv_triangular_index,
                'tinn': tinn,
                # 'ulf_power': ulf_power,
                # 'vlf_power': vlf_power,
                'lf_power': lf_power,
                'hf_power': hf_power,
                'lf_hf_ratio': lf_hf_ratio,
                'sd1': sd1,
                'sd2': sd2,
                # 'apen': apen,
                # 'sampen': sampen,
            }

        except Exception as e:
            print(f"Error: {str(e)}")
        
        return file_info, params 

if __name__ == "__main__":
    fi, p = extract_ecg_features('./static/uploads/Balaji-31-M-Oct 7 2015.adicht')
    print(fi, "\n-----------------\n", p)