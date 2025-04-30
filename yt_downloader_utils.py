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
        print("start to download yt:", url, flush=True)
        try:
            yt = pytubefix.YouTube(url)
        except Exception as e:
            raise RuntimeError(f"無法建立 YouTube 物件（可能是影片無效）: {e}")
        print("title:", yt.title, flush=True)

        # if fmt == "mp4":
        #     index = self.stream_combo.current()
        #     stream = self.yt.streams.filter(progressive=False, file_extension="mp4").order_by('resolution').desc()[index]
        #     stream.download(output_path=self.folder)
        # else:
        #     audio_stream = self.yt.streams.filter(only_audio=True).first()
        #     file = audio_stream.download(output_path=self.folder)
        #     base, ext = os.path.splitext(file)
        #     new_file = base + '.mp3'
        #     os.rename(file, new_file)


        if format == "mp4":
            print('mp4', flush=True)
            # 選擇最高解析度 mp4 非 progressive 影片
            # stream = yt.streams.filter(progressive=False, file_extension="mp4").order_by('resolution').desc().first()
            stream = yt.streams.filter(progressive=False, file_extension="mp4").order_by('resolution').asc().first()
            if not stream:
                print("no stream", flush=True)
                raise Exception("找不到合適的 MP4 影片串流")
            print("download", flush=True)
            file_path = stream.download(output_path=output_dir)
            print("filepath", file_path, flush=True)

        elif format == "mp3":
            # 取得音訊流，並轉為 mp3
            print("mp3", flush=True)
            stream = yt.streams.filter(only_audio=True).first()

            if not stream:
                print("no stream", flush=True)
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
        raise RuntimeError(f"下載失敗: {str(e)}")


