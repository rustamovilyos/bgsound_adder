import csv
import os
import time
from concurrent.futures import ThreadPoolExecutor

from bg_changer import add_bg_sound


class AudioProcessor:
    def __init__(self):
        self.processed_files = set()

    def file_already_processed(self, filename, metadata_csv):
        if not os.path.exists(metadata_csv):
            return False

        with open(metadata_csv, 'r') as metadata:
            metadata_reader = csv.DictReader(metadata, delimiter=';')
            for row in metadata_reader:
                if row['path'] == filename:
                    return True

        return False

    def process_audio(self, bg_folder, metadata_file, output_folder, edited_metadata_file):
        bg_files = os.listdir(bg_folder)
        os.makedirs(output_folder, exist_ok=True)

        for bg in bg_files:
            bg_title = os.path.basename(bg[:-4])
            with open(metadata_file, 'r') as metadata:
                wavs = csv.DictReader(metadata, delimiter=';')
                for wav in wavs:
                    wav_title = os.path.basename(wav['path'][:-4])
                    output_filename = output_folder + wav_title + '_' + bg_title + '.wav'

                    if not self.file_already_processed(output_filename, edited_metadata_file):
                        add_bg_sound(wav['path'], os.path.join(bg_folder, bg), output_filename)
                        print(f"File {wav_title} with background {bg_title} was edited to {output_filename}")

                        if not os.path.exists(edited_metadata_file):
                            with open(edited_metadata_file, 'a') as metadata_edited:
                                metadata_writer = csv.DictWriter(metadata_edited, fieldnames=wavs.fieldnames,
                                                                 delimiter=';')
                                metadata_writer.writeheader()
                                metadata_writer.writerow(
                                    {'path': output_filename, 'text': wav['text'],
                                     'voice': os.path.basename(output_filename)[:-4]})
                        else:
                            with open(edited_metadata_file, 'a') as metadata_edited:
                                metadata_writer = csv.DictWriter(metadata_edited, fieldnames=wavs.fieldnames,
                                                                 delimiter=';')
                                metadata_writer.writerow(
                                    {'path': output_filename, 'text': wav['text'],
                                     'voice': os.path.basename(output_filename)[:-4]})


if __name__ == '__main__':
    audio_processor = AudioProcessor()

    # Укажите пути к папкам и файлам
    backgrounds_folder = "backgrounds/"
    original_metadata = "metadata.csv"
    output_folder_path = "edited/"
    edited_metadata = "metadata_edited.csv"
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(audio_processor.process_audio, backgrounds_folder, original_metadata, output_folder_path,
                        edited_metadata)
        time.sleep(1)
    # audio_processor.process_audio(bg_folder, metadata_file, output_folder, edited_metadata_file)
