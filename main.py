import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class VoiceFileHandler(FileSystemEventHandler):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def on_created(self, event):
        if event.is_directory:
            return
        if not event.src_path.lower().endswith(('.m4a', '.mp3', '.wav')):
            return
            
        print(f"新しい音声ファイルを検出: {event.src_path}")
        
        # 新しいファイルが完全に書き込まれるまで少し待つ
        time.sleep(2)
        
        try:
            # Whisperで文字起こし
            with open(event.src_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            
            # テキストファイルとして保存
            output_path = os.path.splitext(event.src_path)[0] + ".txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(transcript.text)
            
            # AppleScriptを使用してメモアプリに同期
            applescript = f'''
                tell application "Notes"
                    tell account "iCloud"
                        make new note with properties {{body:"{transcript.text}"}}
                    end tell
                end tell
            '''
            try:
                os.system(f"osascript -e '{applescript}'")
                print("メモアプリに同期完了")
            except Exception as e:
                print(f"メモアプリへの同期中にエラーが発生: {str(e)}")
            
            print(f"文字起こし完了: {output_path}")
            
        except Exception as e:
            print(f"エラーが発生しました: {str(e)}")

def main():
    # iCloudのボイスメモフォルダのパスを設定
    # macOSの場合の例
    voice_memos_path = os.path.expanduser("~/Library/Mobile Documents/com~apple~VoiceMemos/Documents")
    
    if not os.path.exists(voice_memos_path):
        print(f"ボイスメモフォルダが見つかりません: {voice_memos_path}")
        return
        
    event_handler = VoiceFileHandler()
    observer = Observer()
    observer.schedule(event_handler, voice_memos_path, recursive=False)
    observer.start()
    
    print(f"ボイスメモフォルダの監視を開始: {voice_memos_path}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n監視を停止しました")
    
    observer.join()

if __name__ == "__main__":
    main()
