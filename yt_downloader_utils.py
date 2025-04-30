import pytubefix
import os
import traceback

def download_youtube_video(url: str, output_dir: str = ".", format: str = "mp4") -> str:
    """
    下載 YouTube 影片或音訊。
    
    :param url: YouTube 網址
    :param output_dir: 儲存目錄
    :param format: "mp4" 或 "mp3"
    :return: 下載後檔案的完整路徑
    """
    try:
        print("start to download yt:", url, flush=True)
        try:
            yt = pytubefix.YouTube(url)
        except Exception as e:
            print("[ERROR] 建立 YouTube 物件失敗", flush=True)
            traceback.print_exc()  # 顯示詳細錯誤行號
            raise RuntimeError(f"無法建立 YouTube 物件（可能是影片無效）: {e}")

        print("title:", yt.title, flush=True)

        if format == "mp4":
            print('mp4', flush=True)
            stream = yt.streams.filter(progressive=False, file_extension="mp4").order_by('resolution').asc().first()
            if not stream:
                print("no stream", flush=True)
                raise Exception("找不到合適的 MP4 影片串流")
            print("download", flush=True)
            file_path = stream.download(output_path=output_dir)
            print("filepath", file_path, flush=True)

        elif format == "mp3":
            print("mp3", flush=True)
            streams = yt.streams.filter(only_audio=True)
            print("streams mp3")
            if not streams:
                print("no stream 1", flush=True)
                raise RuntimeError("找不到可下載的音訊串流")

            print("get first", flush=True)
            stream = streams.first()              
            print("stream first", flush=True)  
            if not stream:
                print("no stream 2", flush=True)
                raise Exception("找不到合適的 MP3 音訊串流")
            print("download", flush=True)
            file_path = stream.download(output_path=output_dir)
            print("filepath", file_path, flush=True)

            base, ext = os.path.splitext(file_path)
            new_file_path = base + ".mp3"
            os.rename(file_path, new_file_path)
            file_path = new_file_path

        else:
            raise ValueError("format 必須為 'mp4' 或 'mp3'")
        
        return file_path

    except Exception as e:
        print("[ERROR] 下載過程發生例外：", flush=True)
        traceback.print_exc()  # ✅ 印出詳細錯誤堆疊
        raise RuntimeError(f"下載失敗: {str(e)}")
