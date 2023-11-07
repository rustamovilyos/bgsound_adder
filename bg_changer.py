"""Add Reverb to a voice recording."""

# import soundfile as sf
# from pedalboard import Pedalboard, Chorus, Reverb
#
# # Read in an audio file:
# audio, sample_rate = sf.read('wav/voice_c12B502.wav')
#
# # Make a Pedalboard object, containing multiple plugins:
# board = Pedalboard([Reverb(room_size=0.5)])
#
# # Run the audio through this pedalboard!
# effected = board(audio, sample_rate)
#
# # Write the audio back as a wav file:
# sf.write('wav/voice_c12B502_new.wav', effected, sample_rate)
# --------------------------------------------------------------------------------
import soundfile as sf
from pedalboard import Pedalboard, NoiseGate, Compressor, Gain, Limiter, LadderFilter, LowShelfFilter, Convolution, \
    Reverb


def add_bg_sound(voice_with_path, bg_with_path, output_path):
    audio, sample_rate = sf.read(voice_with_path)

    # Make a pretty interesting sounding guitar pedalboard:
    board = Pedalboard([
        NoiseGate(threshold_db=-20, ratio=1.5, release_ms=250),
        Compressor(threshold_db=-16, ratio=2.5),

        # Chorus(),
        LadderFilter(mode=LadderFilter.Mode.HPF12, cutoff_hz=440),
        # Phaser(),
        Convolution(bg_with_path, 0.25),
        LowShelfFilter(cutoff_frequency_hz=440, gain_db=4, q=0.5),
        Gain(gain_db=4),
        # Reverb(room_size=0.001),
    ])

    # Pedalboard objects behave like lists, so you can add plugins:
    board.append(Compressor(threshold_db=-16, ratio=1.5))
    board.append(Limiter())

    # Run the audio through this pedalboard!
    effected = board(audio, sample_rate)

    # Write the audio back as a wav file:
    sf.write(output_path, effected, sample_rate)
# --------------------------------------------------------------------------------
# import soundfile as sf
# # Don't do import *! (It just makes this example smaller)
# from pedalboard import *
#
# audio, sample_rate = sf.read('wav/voice_1hakGZ6.wav')
#
# # Make a pretty interesting sounding guitar pedalboard:
# board = Pedalboard([
#     NoiseGate(threshold_db=-40, ratio=1.5, release_ms=250),
#     Compressor(threshold_db=-16, ratio=2.5),
#     LowShelfFilter(cutoff_frequency_hz=440, gain_db=10, q=1),
#     Gain(gain_db=6)
# ])
# effected = board(audio, sample_rate)
#
# # Write the audio back as a wav file:
# sf.write('edited/voice_1hakGZ6-new.wav', effected, sample_rate)
