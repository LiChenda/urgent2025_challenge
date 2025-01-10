import textgrid
import glob
import os
import soundfile
import argparse


def is_overlap(current, interval_list):

    for interval in interval_list:
        if current.minTime < interval.maxTime and current.maxTime > interval.minTime:
            return True
    return False

def valid_duration(utt, minimum_duration):

    return utt.maxTime - utt.minTime > minimum_duration


def process_session_textgrid(data_path, session_name, minimum_duration):

    path = f'{data_path}/TextGrid/{session_name}.TextGrid'
    tg =  textgrid.TextGrid.fromFile(path)

    speaker_names = [s.name for s in tg]
    # filter out empty intervals
    tg = [[ utt for utt in speaker_utts if utt.mark ] for speaker_utts in tg]


    rtv = []
    for i, speaker_utts in enumerate(tg):
        non_overlaped = []
        def check_overlap(utt):
            for j in range(len(tg)):
                if i == j:
                    # skip the current speaker
                    continue
                if is_overlap(utt, tg[j]):
                    return True
                return False

        for utt in speaker_utts:
            if check_overlap(utt):
                continue
            if utt.mark and valid_duration(utt, minimum_duration):
                non_overlaped.append(utt)

        rtv.append((speaker_names[i], non_overlaped ))
    return rtv


def process_sessions(data_path, output_path, minimum_duration):
    wavs = glob.glob(data_path + '/wav/*.flac')
    audio_out = output_path + '/wavs'
    os.makedirs(audio_out, exist_ok=True)

    wav_scp = open(output_path + '/wav.scp', 'w')
    text_scp = open(output_path + '/text', 'w')

    for wav in wavs:
        session_name = os.path.basename(wav).replace('.flac', '')
        audio, sr = soundfile.read(wav)

        spk_utts = process_session_textgrid(data_path, session_name, minimum_duration)

        for spk_name, utts in spk_utts:
            for utt in utts:
                start = int(utt.minTime * sr)
                end = int(utt.maxTime * sr)
                text = utt.mark
                uid = f'{session_name}_{spk_name}_{utt.minTime:.3f}_{utt.maxTime:.3f}'
                o_wav_path = f"{audio_out}/{uid}.wav"
                wav_scp.write(f"{uid}\t{o_wav_path}\n")
                text_scp.write(f"{uid}\t{text}\n")
                soundfile.write(o_wav_path, audio[start:end], sr)


    wav_scp.close()
    text_scp.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()  
    parser.add_argument(
        "--data_path",
        type=str,
        required=True,
        help="Path to the AIshell4 dataset, e.g. /data/test ",
    )

    parser.add_argument(
        "--output_path",
        type=str,
        required=True,
        help="Path to the output folder",
    )

    parser.add_argument(
        "--minimum_duration",
        type=float,
        required=False,
        default=0.0,
        help="Filter out short utterances",
    )

    args = parser.parse_args()


    process_sessions(args.data_path, args.output_path, args.minimum_duration)

