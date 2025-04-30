import pytubefix
import os

def download_youtube_video(url: str, output_dir: str = ".", format: str = "mp4") -> str:
    """
    下載 YouTube 影片或音訊。
    
    :param url: YouTube 網址
    :param output_dir: 儲存目錄
    :param format: "mp4" 或 "mp3"
    :return: 下載後檔案的完整路徑
    """
    try:
        print("start to download yt:", url)
        try:
            yt = pytubefix.YouTube(url)
        except Exception as e:
            raise RuntimeError(f"無法建立 YouTube 物件（可能是影片無效）: {e}")
        print("title:", yt.title)

        if format == "mp4":
            # 選擇最高解析度 mp4 非 progressive 影片
            # stream = yt.streams.filter(progressive=False, file_extension="mp4").order_by('resolution').desc().first()
            stream = yt.streams.filter(progressive=False, file_extension="mp4").order_by('resolution').asc().first()
            if not stream:
                raise Exception("找不到合適的 MP4 影片串流")
            file_path = stream.download(output_path=output_dir)
        elif format == "mp3":
            # 取得音訊流，並轉為 mp3
            stream = yt.streams.filter(only_audio=True).first()
            if not stream:
                raise Exception("找不到合適的 MP3 音訊串流")
            file_path = stream.download(output_path=output_dir)
            base, ext = os.path.splitext(file_path)
            new_file_path = base + ".mp3"
            os.rename(file_path, new_file_path)
            file_path = new_file_path
        else:
            raise ValueError("format 必須為 'mp4' 或 'mp3'")
        
        return file_path

    except Exception as e:
        raise RuntimeError(f"下載失敗: {str(e)}")


