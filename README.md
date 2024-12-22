# urgent2025_challenge
Official data preparation scripts for the [URGENT 2025 Challenge](https://urgent-challenge.github.io/urgent2025/).

The metadata files generated by this repo is compatible with [the baseline code](https://github.com/kohei0209/espnet/tree/urgent2025/egs2/urgent25/enh1).
See the [instruction](https://github.com/kohei0209/espnet/blob/urgent2025/egs2/urgent25/enh1/README.md) for more details about how to run the baseline code.

## Updates

❗️❗️[**2024-11-27**] We added trouble shooting for some known issues at the tail of this README. Please check it first if you encounter some problems.

❗️❗️[**2024-11-19**] We modified [ESTOI evaluation](https://github.com/urgent-challenge/urgent2025_challenge/blob/main/evaluation_metrics/calculate_intrusive_se_metrics.py) to be deterministic (it has [randomness](https://github.com/mpariente/pystoi/blob/74872b000753a7a42ff51aa0868af8c82c7f9053/pystoi/utils.py#L178)).

❗️❗️[**2024-11-18**] We have added some missing files which are necessary for data preparation in Track 2, [commonvoice_19.0_es_train_track2.json.gz](https://github.com/urgent-challenge/urgent2025_challenge/blob/main/datafiles/commonvoice/commonvoice_19.0_es_train_track2.json.gz). If you cloned the repogitory before Nov. 18, please pull the latest commit.

❗️❗️[**2024-11-16**] We have modified some data preparation and evaluation scripts. If you cloned the repogitory before Nov. 16, please pull the latest commit.

## Notes

- If you do not have the license of the WSJ corpora, please reach out to the organizers (urgent.challenge@gmail.com) for a temporary license supported by LDC. Please include your name, organization/affiliation, and the username used in the leaderboard in the email for a smooth procedure. Note that we do not accept the request unless you have registered to the challenge leaderboard (refer to this page to know how to register).

- Please check the trouble shooting at the tail of this README first if you encounter some problems. Please raise an issue when you find any other problems.

- The default generated `data/speech_train` subset is only intended for **dynamic mixing (on-the-fly simulation)** in the ESPnet framework. It has the same content in `spk1.scp` (clean reference speech) and `wav.scp` (originally intended to point noisy speech) to facilitate on-the-fly simulation of different distortions.

- The validation set made by this script is different from the official validation set used in the leaderboard, although the data source and the type of distortions do not change. **The official one is [here](https://drive.google.com/file/d/1Ip-C5tUNGCssT8KAjHUUoh99jkzRH6nm/view)**. Note that we only provide the noisy data but not the ground truth of the official validation set until the leaderboard swithces to test phase (Dec. 23) to avoid cheating in the leaderboard.

- The unofficial validation set made by this script can be used to select the best checkpoint. Participants can freely change the [configuration to generate the unofficial validation set](https://github.com/urgent-challenge/urgent2025_challenge/blob/main/conf/simulation_validation.yaml).
<!-- 
* To use a fixed simulation training set (without dynamic mixing), you could follow the [commented lines](https://github.com/urgent-challenge/urgent2024_challenge/blob/main/prepare_espnet_data.sh#L188-L210) in the [`prepare_espnet_data.sh`](https://github.com/urgent-challenge/urgent2024_challenge/blob/main/prepare_espnet_data.sh) script to generate `data/train`.
-->


## Requirements

- `>8` Cores
- At least 1.3 TB of free disk space for the track 1 and ??? TB for the track 2
- <details>

  <summary><strong>Data-size breakdown</strong></summary>

  - Note: we only counted audio files and did not include the size of archived files (e.g., .zip or .tar.gz files). You can remove the archived files once the data preparation is done.
  - Speech
    - DNS5 speech (original 131 GB + resampled 94 GB): 225 GB
    - LibriTTS (original 44 GB + resampled 7 GB): 51 GB
    - VCTK: 12 GB
    - WSJ (original sph 24GB + converted 31 GB): 55 GB
    - EARS: 61 GB
    - CommonVoice 19.0 speech
      - Track 1 (original mp3 221 GB + resampled 200 GB): 421 GB
      - Track 2 (original mp3 221 GB + resampled ??? GB): ??? GB
    - MLS (less compressed version downloaded from LibriVox)
      - Track 1 (original 60 GB + resampled 60 GB): 120 GB
      - Track 2 (original 6TB + resampled ???TB): ???TB
  - Noise
    - DNS5 noise (original 58 GB + resampled 35 GB): 93 GB
    - WHAM! noise (48 kHz): 76 GB
    - FSD50K (original 24 GB + resampled 6 GB): 30 GB
    - FMA: (original 24 GB + resampled 36 GB): 60 GB
  - RIR
    - DNS5 RIRs (48 kHz): 6 GB
  - Others
    - default simulated validation data: 2 GB
    - simulated wind noise for training (with default config): 1 GB

  </details>


## Instructions

0. After cloning this repository, run the following command to initialize the submodules:
    ```bash
    git submodule update --init --recursive
    ```

1. Install environmemnt. Python 3.10 and Torch 2.0.1+ are recommended.
   With Conda, just run

    ```bash
    conda env create -f environment.yaml
    conda activate urgent2025
    ```

    > In case of the following error
    > ```
    >   ERROR: Failed building wheel for pypesq
    > ERROR: Could not build wheels for pypesq, which is required to install pyproject.toml-based projects
    > ```
    > you could manually install [`pypesq`](https://github.com/vBaiCai/python-pesq) in advance via: 
    > (make sure you have `numpy` installed before trying this to avoid compilation errors)
    > ```bash
    > python -m pip install https://github.com/vBaiCai/python-pesq/archive/master.zip
    > ```

2. Get the download link of Commonvoice dataset v19.0 from https://commonvoice.mozilla.org/en/datasets

    For German, English, Spanish, French, and Chinese (China), please do the following.

    a. Select `Common Voice Corpus 19.0`

    b. Enter your email and check the two mandatory boxes

    c. Right-click the `Download Dataset Bundle` button and select "Copy link"

    d. Paste the link to Lines `URLs=(...)` in [utils/prepare_CommonVoice19_speech.sh](https://github.com/kohei0209/urgnet2025/blob/a2fa5ef53f9ef8eab527a37dcb8aca5aae76ac71/utils/prepare_CommonVoice19_speech.sh#L16-L19) like
    ```bash
    URLs=(
      "https://storage.googleapis.com/common-voice-prod-prod-datasets/cv-corpus-19.0-2024-09-13/cv-corpus-19.0-2024-09-13-de.tar.gz?xxxxxx"
      "https://storage.googleapis.com/common-voice-prod-prod-datasets/cv-corpus-19.0-2024-09-13/cv-corpus-19.0-2024-09-13-en.tar.gz?xxxxxx"
      "https://storage.googleapis.com/common-voice-prod-prod-datasets/cv-corpus-19.0-2024-09-13/cv-corpus-19.0-2024-09-13-es.tar.gz?xxxxxx"
      "https://storage.googleapis.com/common-voice-prod-prod-datasets/cv-corpus-19.0-2024-09-13/cv-corpus-19.0-2024-09-13-fr.tar.gz?xxxxxx"
      "https://storage.googleapis.com/common-voice-prod-prod-datasets/cv-corpus-19.0-2024-09-13/cv-corpus-19.0-2024-09-13-zh-CN.tar.gz?xxxxxx"
    )
    ```

3. Make a symbolic link to wsj0 and wsj1 data

    a. Make a directory `./wsj`

    b. Make a symbolic link to wsj0 and wsj1 under `./wsj` (`./wsj/wsj0/` and `./wsj/wsj1/`)

    > NOTE:
    > If you do not have the license of the WSJ corpora, please reach out to the organizers (urgent.challenge@gmail.com) for a temporary license supported by LDC. Please include your name, organization/affiliation, and the username used in the leaderboard in the email for a smooth procedure. Note that we do not accept the request unless you have registered to the challenge leaderboard (refer to [this page](https://urgent-challenge.github.io/urgent2025/leaderboard/) to know how to register). Note that the paticipants are allowed to train their systems using only the subset of the given dataset, and thus preliminary investigation (or even final submission) can be done without WSJ corpora.

<!--
3. Download WSJ0 and WSJ1 datasets from LDC
    > You will need a LDC license to access the data.
    >
    > For URGENT Challenge participants who want to use the data during the challenge period, please contact the organizers for a temporary LDC license.

    a. Download WSJ0 from https://catalog.ldc.upenn.edu/LDC93s6a

    b. Download WSJ1 from https://catalog.ldc.upenn.edu/LDC94S13A

    c. Uncompress and store the downloaded data to the directories `./wsj/wsj0/` and `./wsj/wsj1/`, respectively.
-->

4. FFmpeg-related

    To simulate wind noise and codec artifacts, our scripts utilize FFmpeg.

    a. Activate your python environment

    b. Get the path to FFmpeg by `which ffmpeg`
    
    c. Change `/path/to/ffmpeg` in [simulation/simulate_data_from_param.py](https://github.com/kohei0209/urgnet2025/blob/a2fa5ef53f9ef8eab527a37dcb8aca5aae76ac71/simulation/simulate_data_from_param.py#L19) to the path to your ffmpeg.

5. Run the script

    ```bash
    ./prepare_espnet_data.sh
    ```

    **NOTE**: Please do not change `output_dir` in each shell script called in `prepare_{dataset}.sh`. If you want to download datasets to somewhere else, make a symbolic link to that directory. 
    ```bash
    # example when you want to download FSD50K noise to /path/to/somewhere
    # prepare_fsd50k_noise.sh specifies ./fsd50k as output_dir, so make a symbolic link from /path/to/somewhere to ./fsd50k
    mkdir -p /path/to/somewhere
    ln -s /path/to/somewhere ./fsd50k
    ```


6. Install eSpeak-NG (used for the phoneme similarity metric computation)
   - Follow the instructions in https://github.com/espeak-ng/espeak-ng/blob/master/docs/guide.md#linux
   - NOTE: if you build `eSpeak-NG` from source (not by e.g., apt-get), it may cause an error when running `evaluation_metrics/calculate_phoneme_similarity.py`. Refer to the troubleshooting below if you encounter the issue.

<!--
## Optional: Prepare webdataset

The script `./utils/prepare_wds.py` can store the audio files in a collection
of tar files each containing a predefined number of audio files. This is useful
to reduce the number of IO operations during training. Please see the
[documentation](https://github.com/webdataset/webdataset) of `webdataset` for
more information.

```bash
OMP_NUM_THREADS=1 python ./utils/prepare_wds.py \
    /path/to/urgent_train_24k_wds \
    --files-per-tar 250 \
    --max-workers 8 \
    --scps data/tmp/commonvoice_11.0_en_resampled_filtered_train.scp \
    data/tmp/dns5_clean_read_speech_resampled_filtered_train.scp \
    data/tmp/vctk_train.scp \
    data/tmp/libritts_resampled_train.scp
```
The script can also resample the whole dataset to a unified sampling frequency
with `--sampling-rate <freq_hz>`. This option will not include samples with
sampling frequency lower than the prescribed frequency.
-->


## Trouble Shooting

<details>

  <summary><strong>Errors when unpacking MLS .tar.gz files</strong></summary>
  
  <br>

  Sometimes, an error like the following happens when unpacking .tar.gz files in `utils/prepare_MLS_speech.sh`.

  If you encounter this error, please just retry the script after deleting `./mls_segments/download_mls_${lang}_${split}_${track}.done` for the failed language, split (train or dev), and track (track1 or track2).

  In the following example, one needs to remove `./mls_segments/download_mls_spanish_train_track1.done` before rerunning the script again.

  ```sh
  === Preparing MLS data for track1 ===                                                                                                                                                                                 
  === Preparing MLS german train data ===                                                                                                                                                                               
  [MLS-german-train_track1] downloading data                                                                                                                                                                            
  === Preparing MLS german dev data ===                                                                                                                                                                                 
  [MLS-german-dev] downloading data                                                                                                                                                                                     
  === Preparing MLS french train data ===                                                                                                                                                                               
  [MLS-french-train_track1] downloading data                                                                                                                                                                            
  === Preparing MLS french dev data ===                                                                                                                                                                                 
  [MLS-french-dev] downloading data
  === Preparing MLS spanish train data ===
  [MLS-spanish-train_track1] downloading data
  tar: ./3946/3579: Cannot mkdir: No such file or directory
  tar: ./3946/8075: Cannot mkdir: No such file or directory
  tar: ./9972/10719: Cannot mkdir: No such file or directory
  tar: Exiting with failure status due to previous errors
  tar: Exiting with failure status due to previous errors
  tar: Exiting with failure status due to previous errors
  ```

</details>

<br>

<details>

  <summary><strong>Warnings when processing FMA data</strong></summary>

  <br>

  When preparing FMA data, following warnings appear but you can just ignore them.
  

  ```sh
  [FMA noise] split training and validation data
  [FMA noise] resampling to estimated audio bandwidth
    0%|                                                                                          | 0/19902 [00:00<?, ?it/s][src/libmpg123/layer3.c:INT123_do_layer3():1801] error: dequantization failed!
  [src/libmpg123/layer3.c:INT123_do_layer3():1771] error: part2_3_length (3264) too large for available bit count (3224)
  [src/libmpg123/layer3.c:INT123_do_layer3():1841] error: dequantization failed!
  [src/libmpg123/layer3.c:INT123_do_layer3():1801] error: dequantization failed!
  ...
  ```

</details>

<br>

<details>
  <summary><strong>TypeError when running calculate_phoneme_similarity.py</strong></summary>

  <br>

  The following error may happen when running `evaluation_metrics/calculate_phoneme_similarity.py`.

  This is because phoneme recognizer requires `lib` while only `bin` directory exists, depending on how you built `eSpeak-NG`.

  Adding the path to `LD_LIBRARY_PATH` solves the issue.

  ```sh
  evaluation_metrics/calculate_phoneme_similarity.py", line 58, in __init__
    self.phoneme_predictor = PhonemePredictor(device=device)
  urgent2025_challenge/evaluation_metrics/calculate_phoneme_similarity.py", line 29, in __init__
      self.processor = Wav2Vec2Processor.from_pretrained(checkpoint)

  TypeError: Received a bool for argument tokenizer, but a PreTrainedTokenizerBase was expected.
  ```
</details>