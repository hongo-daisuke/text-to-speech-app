from google.cloud import texttospeech
import streamlit as st


def synthesize_speech(text, gender='default', lang='jp'):
    gender_type = {
        'default': texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED,
        'male': texttospeech.SsmlVoiceGender.MALE,
        'female': texttospeech.SsmlVoiceGender.FEMALE,
        'neutral': texttospeech.SsmlVoiceGender.NEUTRAL
    }
    lang_type = {
        'us':'en-US',
        'jp':'ja-JP'
    }

    client = texttospeech.TextToSpeechClient()

    # 音声にするテキスト
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # 音声にする際のパラメータ
    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_type[lang], ssml_gender=gender_type[gender]
    )

    # 生成する音声の設定
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # APIを実行しresponseに格納
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config

    )
    
    return response

st.title('音声出力アプリ')
st.markdown('### データ準備')

input_option = st.selectbox(
    '入力データの選択',
    ('直接入力', 'テキストファイル')
)

input_data = None

if input_option == '直接入力':
    input_data = st.text_area('こちらにテキストを入力して下さい。', '読み上げサンプルテキスト')
else:
    upload_file = st.file_uploader('テキストファイルをアップロードして下さい。', type=['txt'])
    # テキストファイルがアップロードされたら
    if upload_file is not None:
        # ファイルを読み込み
        content = upload_file.read()
        # デコードして代入
        input_data = content.decode()

if input_data is not None:
    st.write('入力データ')
    st.write(input_data)
    st.markdown('### パラメータ設定')
    st.subheader('言語と話者の性別選択')
    lang = st.selectbox(
        '言語を選択して下さい。',
        ('us', 'jp')
    )
    gender = st.selectbox(
        '性別を選択して下さい。',
        ('default', 'male', 'female', 'neutral')
    )
    st.markdown('### 音声合成')
    st.write('こちらの文章で音声ファイルの作成を行いますか？')
    if st.button('開始'):
        comment = st.empty()
        comment.write('音声出力を開始します')
        response = synthesize_speech(input_data, lang=lang, gender=gender)
        st.audio(response.audio_content)
        comment.write('完了しました。')