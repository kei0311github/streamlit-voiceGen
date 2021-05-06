import os
import streamlit as st
from google.cloud import texttospeech
import io
from IPython.display import Audio

gender_type = {
    'default': texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED,
    'male': texttospeech.SsmlVoiceGender.MALE,
    'female': texttospeech.SsmlVoiceGender.FEMALE,
    'neutral': texttospeech.SsmlVoiceGender.NEUTRAL
}

lang_code = {
    '英語': 'en-US',
    '日本語': 'ja-JP'
}

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secretkey.json'


def synthesis_speech(text, lang='日本語', gender='male'):

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code[lang], ssml_gender=gender_type[gender]
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response


st.title('音声出力アプリ')

st.markdown("## データ準備")

selected_input_type = st.selectbox('入力データの選択', ['直接入力', 'テキストファイル'],)

input_data = None
if selected_input_type == '直接入力':
    input_data = st.text_area(
        'こちらにテキストを入力して下さい。', 'Cloud Speech-To-Text用のサンプル文になります。')
elif selected_input_type == 'テキストファイル':
    uploaded_input_txt = st.file_uploader('テキストファイルをアップロードして下さい。', type='txt')
    if uploaded_input_txt is not None:
        content = uploaded_input_txt.read()
        input_data = content.decode()

if input_data is not None:
    st.markdown("### 入力データ")
    st.write(input_data)
    st.markdown("### パラメータ設定")
    st.markdown("#### 言語と話者の性別選択")
    selected_lang_type = st.selectbox('言語を選択してください。', list(lang_code.keys()))
    selected_gender_type = st.selectbox(
        '話者の性別を選択してください。', list(gender_type.keys()))

    st.markdown("### 音声合成")
    st.write("こちらの文章で音声ファイルの生成を行いますか？")
    if st.button('開始'):
        comment = st.empty()
        comment.write('音声出力を開始します。')
        response = synthesis_speech(
            input_data, selected_lang_type, selected_gender_type)
        st.audio(response.audio_content)
        comment.write('完了しました。')
