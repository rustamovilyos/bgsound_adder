import soundfile as sf
from pedalboard import Pedalboard, NoiseGate, Compressor, Gain, LowShelfFilter, Reverb


def add_bg_sound(voice_with_path, output_path):
    audio, sample_rate = sf.read(voice_with_path)

    # Make a pretty interesting sounding guitar pedalboard:
    board = Pedalboard([
        NoiseGate(threshold_db=-40, ratio=1.5, release_ms=250),
        Compressor(threshold_db=-16, ratio=2.5),
        LowShelfFilter(cutoff_frequency_hz=440, gain_db=3, q=1),
        Gain(gain_db=3),
        # PitchShift(semitones=-2),

        # Reverb(room_size=0.1),
    ])

    effected = board(audio, sample_rate)

    # Write the audio back as a wav file:
    sf.write(output_path, effected, sample_rate)


if __name__ == '__main__':
    add_bg_sound('wav/voice_ac7dQIo_slow.wav', 'edited/voice_ac7dQIo_slow.wav')
