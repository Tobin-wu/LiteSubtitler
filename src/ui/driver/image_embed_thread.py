# coding: utf8
import os
import shutil

from PyQt6.QtCore import QThread, pyqtSignal

from service.video_service import VideoService


class ImageEmbedThread(QThread):
    """图片合成子线程"""

    message_signal = pyqtSignal(str)  # 定义信号用于传递消息
    end_signal = pyqtSignal(str)  # 定义信号用于结束消息

    def __init__(self, service: VideoService, config, video_info, use_cuda: bool = False):
        super().__init__()
        self.is_running = True
        self.service = service

        self._args = config

        self.video_info = video_info
        service.reset_cuda(use_cuda)

    def run(self):
        """线程执行方法"""
        self.is_running = True
        try:
            self.message_signal.emit(f"图片合成开始：{self.video_info['file_path']}")
            video_file = self.video_info['file_path']
            out_embed_file = self.video_info['file_dir'] + '/tmp.mp4'
            is_embed = False
            if self._args['embed1_arg'].file_path or self._args['embed2_arg'].file_path:
                self.message_signal.emit("视频嵌入图片")
                embed_file = self.service.image_embed_mp4(
                    video_file=self.video_info['file_path'],
                    out_video_file=out_embed_file,
                    image_1_arg=self._args['embed1_arg'],
                    image_2_arg=self._args['embed2_arg'],
                )
                is_embed = os.path.exists(embed_file)

            if self._args['head_image']['file_path'] or self._args['end_image']['file_path']:
                self.message_signal.emit("视频拼接图片")
                bit_rate = '1M' if self.video_info['bitrate_kbps'] < 1024 else f"{self.video_info['bitrate_kbps']}K"
                self.service.image_concat_mp4(video_file=out_embed_file if is_embed else video_file,
                                              out_video_file=self._args["out_video"]["file_path"],
                                              start_image_file=self._args["head_image"]["file_path"],
                                              end_image_file=self._args["end_image"]["file_path"],
                                              start_seconds=self._args["head_image"]["seconds"],
                                              end_seconds=self._args["end_image"]["seconds"],
                                              scale=f'{self.video_info["width"]}:{self.video_info["height"]}',
                                              frame_rate=self.video_info['fps'],
                                              audio_sampling_rate=self.video_info['audio_sampling_rate'],
                                              audio_channel_layout=self.video_info['audio_channel_layout'],
                                              bit_rate=bit_rate,
                                              source_video_to_mp4=not is_embed,
                                              delete_temp=self._args['delete_temp'])
            elif is_embed:
                out_video_file = self._args["out_video"]["file_path"]
                # 把 out_embed_file 复制为 out_video_file
                shutil.copy2(out_embed_file, out_video_file)

            if self._args['delete_temp']:
                if os.path.exists(out_embed_file):
                    os.remove(out_embed_file)
                    self.message_signal.emit(f"移除中间文件：{out_embed_file}")
        except Exception as e:
            self.message_signal.emit(f"合成错误: {str(e)}\n")
        finally:
            self.end_signal.emit(f"合成结束: {self._args['out_video']['file_path']}")
            self.is_running = False

    def stop(self):
        """停止线程"""
        self.is_running = False
        self.wait()
