import mscl

def sample_rate_mapping(sample_rate_str):
    sample_rates = {
        '104170': mscl.WirelessTypes.sampleRate_104170Hz,
        '78125': mscl.WirelessTypes.sampleRate_78125Hz,
        '62500': mscl.WirelessTypes.sampleRate_62500Hz,
        '25000': mscl.WirelessTypes.sampleRate_25000Hz,
        '12500': mscl.WirelessTypes.sampleRate_12500Hz,
        '8192': mscl.WirelessTypes.sampleRate_8192Hz,
        '4096': mscl.WirelessTypes.sampleRate_4096Hz,
        '2048': mscl.WirelessTypes.sampleRate_2048Hz,
        '1024': mscl.WirelessTypes.sampleRate_1024Hz,
        '512': mscl.WirelessTypes.sampleRate_512Hz,
        '256': mscl.WirelessTypes.sampleRate_256Hz,
        '128': mscl.WirelessTypes.sampleRate_128Hz,
        '64': mscl.WirelessTypes.sampleRate_64Hz,
        '32': mscl.WirelessTypes.sampleRate_32Hz,
        '16': mscl.WirelessTypes.sampleRate_16Hz,
        '8': mscl.WirelessTypes.sampleRate_8Hz,
        '4': mscl.WirelessTypes.sampleRate_4Hz,
        '2': mscl.WirelessTypes.sampleRate_2Hz,
        '1': mscl.WirelessTypes.sampleRate_1Hz
    }

    if sample_rate_str in sample_rates:
        return sample_rates[sample_rate_str]
    else:
        return None