import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Returns an np array of values of the fuction for each time instant in t.
def sine_signal(t):
    return (np.sin(2 * np.pi * t) * 2.5) + 2.5


def convert_to_digital(values):
    return np.round((values * 1023) / 5)


def convert_to_TTL(values):
    return (values * 5) / 1023


def ADC():
    # A very fine grain time scale (simulating an analog signal)
    t_analog = np.arange(0.0, 5.0, 0.005)

    # The frequency of the signal sin(t) is 1. We'll use a sample frequency of
    # 10 which means our period will be 1/10 of 0.1.
    t_sample = np.arange(0.0, 5.0, 0.1)

    plt.figure(1)
    # Original signal.
    plt.subplot(311)
    plt.plot(t_analog, sine_signal(t_analog), "k")
    plt.title("Original signal")

    sampled_values = sine_signal(t_sample)

    # Sampled signal.
    plt.subplot(312)
    plt.plot(t_sample, sampled_values, "ro", alpha=0.5)
    plt.vlines(t_sample, 0, sampled_values, "r")
    plt.title("Sampled signal")

    quantized_values = convert_to_digital(sampled_values)
    # We asume we use an 8 bit adc and we add a zero order hold.
    plt.subplot(313, ylim=(0, 1024))
    plt.plot(t_sample, quantized_values, "ro", alpha=0.5)
    plt.vlines(t_sample, 0, quantized_values, "r")
    plt.title("ADC output")


def DAC():
    # Our process produces data at a rate of 50Hz.
    t_process = np.arange(0.0, 2.0, 0.02)

    # We use a sawtooth signal that goes from 0 to 1023.
    process_values = np.round(
        (signal.sawtooth(2 * np.pi * t_process) * 2.5 + 2.5) * (1023 / 5)
    )

    # These are the original values from our process.
    plt.figure(2)
    plt.subplot(311)
    plt.vlines(t_process, 0, process_values, "r")
    plt.title("Process values")

    # The DAC then maps this values to a TTL voltage.
    plt.subplot(312)
    plt.vlines(t_process, 0, convert_to_TTL(process_values), "r")
    plt.title("Values in TTL")

    # Then we add a zero order hold to make the signal continuos.
    plt.subplot(313)
    plt.step(t_process, convert_to_TTL(process_values), "r", where="post")
    plt.title("DAC output")


if __name__ == "__main__":
    ADC()
    DAC()
    plt.show()
