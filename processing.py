import numpy as np


def is_system_settled(times, setpoint_1, setpoint_2, settling_time):
    levels = np.stack([setpoint_1.mean(axis=1), setpoint_2.mean(axis=1)], axis=1)

    is_switch = np.any(np.diff(levels, axis=0) != 0, axis=1)
    switching_times = times[1:][is_switch]

    time_after_switch = times[:, None] - switching_times
    return np.all((time_after_switch < 0) | (time_after_switch > settling_time), axis=1)


def center_spectra(spectra):
    return spectra - spectra.mean(axis=1, keepdims=True)


def broaden_spectrum(
    wavenumber,
    spectrum,
    spectral_range,
    spectral_resolution,
    window_type,
):
    number_delays = int(np.ceil(2 * np.max(spectral_range) / spectral_resolution))
    maximum_delay = 1.0 / (2.0 * spectral_resolution)

    delay_step = 2.0 * maximum_delay / number_delays
    delay = (np.arange(number_delays) - (number_delays - 1) / 2) * delay_step

    if window_type == "happ-genzel":
        apodization = np.hamming(number_delays)
    elif window_type == "boxcar":
        apodization = np.ones(number_delays)
    else:
        raise ValueError(f"Unknown window type: {window_type}.")

    wavenumber_step = np.mean(np.diff(wavenumber))

    kernel_half_width = 4.0 * spectral_resolution
    number_half_kernel_points = int(np.ceil(kernel_half_width / wavenumber_step))
    wavenumber_kernel = (
        np.arange(-number_half_kernel_points, number_half_kernel_points + 1)
        * wavenumber_step
    )

    phase_cycles = np.outer(wavenumber_kernel, delay)
    lineshape = np.cos(2.0 * np.pi * phase_cycles) @ apodization

    lineshape /= lineshape.sum()

    return np.convolve(
        spectrum,
        lineshape,
        mode="same",
    )


def concentration_from_flowrate(flowrate, concentration_per_flowrate):
    return concentration_per_flowrate * flowrate


def voltage_from_concentration(
    concentration,
    characteristic_concentration,
    baseline_voltage,
    saturation_voltage,
):
    return baseline_voltage + (saturation_voltage - baseline_voltage) * (
        1 - np.exp(-concentration / characteristic_concentration)
    )


def concentration_from_voltage(
    voltage,
    characteristic_concentration,
    baseline_voltage,
    saturation_voltage,
):
    return -characteristic_concentration * np.log(
        (saturation_voltage - voltage) / (saturation_voltage - baseline_voltage)
    )


def scaling_from_pid_to_cell(flowrates, split_ratio, channel):
    channel_split_ratio = split_ratio if channel == 1 else 1 - split_ratio
    scaling = (flowrates[:, channel] + channel_split_ratio * flowrates[:, 0]) / np.sum(
        flowrates, axis=1
    )

    return scaling


def scaling_from_cell_to_pid(flowrates, split_ratio, channel):
    channel_split_ratio = split_ratio if channel == 1 else 1 - split_ratio
    scaling = np.sum(flowrates, axis=1) / (
        flowrates[:, channel] + channel_split_ratio * flowrates[:, 0]
    )

    return scaling


def segment_settled_array(array, are_settled):
    segment = []
    segments = []
    for index, value in enumerate(are_settled):
        if value:
            segment.append(array[index, :])
        elif segment:
            segments.append(segment)
            segment = []
    if segment:
        segments.append(segment)

    minimum_segment_length = min(len(segment) for segment in segments)
    array = np.stack(
        [np.stack(segment[:minimum_segment_length]) for segment in segments], axis=-1
    )

    return array


def crossing_time_slope(time, signal, threshold):
    idx = np.flatnonzero((signal[:-1] < threshold) & (signal[1:] >= threshold))[0]

    t0, t1 = time[idx : idx + 2]
    y0, y1 = signal[idx : idx + 2]

    slope = (y1 - y0) / (t1 - t0)
    t_cross = t0 + (threshold - y0) / slope

    return t_cross, slope


def cm2inch(values_cm):
    return np.divide(values_cm, 2.54)


def annotate(ax, text):
    ax.text(
        0.05,
        0.95,
        text,
        transform=ax.transAxes,
        verticalalignment="top",
        horizontalalignment="left",
        zorder=20,
    )


def format_number(value, error, significant=2):
    if value != 0 and (abs(value) < 0.01 or abs(value) >= 10_000):
        exponent = int(np.floor(np.log10(abs(value))))

        mantissa = value / 10**exponent
        mantissa_error = error / 10**exponent

        decimals = int(significant - 1 - np.floor(np.log10(abs(mantissa_error))))

        if decimals >= 0:
            return rf"{mantissa:.{decimals}f}\cdot10^{{{exponent}}}"
        else:
            mantissa = round(mantissa, decimals)
            return rf"{mantissa:.0f}\cdot10^{{{exponent}}}"

    decimals = int(significant - 1 - np.floor(np.log10(abs(error))))

    if decimals >= 0:
        return f"{value:.{decimals}f}"
    else:
        return f"{round(value, decimals):.0f}"
