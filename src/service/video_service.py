# coding: utf8
import os
import time
from typing import Literal, Optional, Dict, Callable, Any

from core.asr.asr_data import ASRData
from core.base_object import BaseObject
from core.video.ffmpeg_handler import FfmpegHandler
from core.video.image_embed_arg import ImageEmbedArg
from model.file_vo import FileVO
from utils.dict_utils import DictUtils


class VideoService(BaseObject):
    """
    视频服务类，用于处理视频文件的音频提取、字幕嵌入和视频信息获取。

    主要功能：
        1. 提取视频中的音频文件。
        2. 将字幕嵌入到视频文件中（支持硬字幕和软字幕）。
        3. 获取视频文件的详细信息。
    """

    def __init__(self, log_to_ui_func: Optional[Callable] = None):
        """
        初始化视频服务。

        Args:
            log_to_ui_func: 用于将日志输出到 UI 的函数。
        """
        super().__init__(log_to_ui_func=log_to_ui_func)

        self._args = {
            "subtitle_layout": "译文在上",  # 字幕布局
            "quality": 'medium',
            # 压制方式，支持 ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow']
            "is_embed_subtitle": False,  # 是否将字幕嵌入视频
            "is_soft_subtitle": False,  # 是否使用软字幕
            "style_str": (
                "[V4+ Styles]\n"
                "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,"
                "Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,"
                "Alignment,MarginL,MarginR,MarginV,Encoding\n"
                "Style: Default,MicrosoftYaHei-Bold,40,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,"
                "0,0,1,2,0,2,10,10,15,1\n"
                "Style: Secondary,MicrosoftYaHei-Bold,30,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,"
                "0,0,1,2,0,2,10,10,15,1"
            )  # ASS 字幕样式
        }

    def reset_args(self, the_args: Dict[str, Any]) -> None:
        """
        重置视频处理参数。

        Args:
            the_args: 包含新参数的字典。
        """
        DictUtils.update_by_key(self._args, the_args)

        if 'default_style' in the_args and 'secondary_style' in the_args:
            self._args["style_str"] = ASRData.read_ass_style(the_args)

    def reset_cuda(self, use_cuda: bool) -> None:
        self._args['use_cuda'] = use_cuda

    def image_embed_mp4(self,
                        video_file: str,
                        out_video_file: str,
                        image_1_arg: ImageEmbedArg,
                        image_2_arg: ImageEmbedArg):
        ffmpeg_handler = FfmpegHandler(log_to_ui_func=self.log_to_ui_func)
        try:
            if image_1_arg.file_path and image_2_arg.file_path:
                return ffmpeg_handler.embed_2_image(video_file_path=video_file,
                                                    out_video_path=out_video_file,
                                                    image_1_arg=image_1_arg,
                                                    image_2_arg=image_2_arg,
                                                    use_cuda=self._args['use_cuda'])
            else:
                image_arg = image_1_arg
                if not image_1_arg.file_path:
                    image_arg = image_2_arg
                if image_arg:
                    return ffmpeg_handler.embed_1_image(video_file_path=video_file,
                                                        out_video_path=out_video_file,
                                                        image_arg=image_arg,
                                                        use_cuda=self._args['use_cuda'])
            return None
        finally:
            ffmpeg_handler.stop()

    def image_concat_mp4(self,
                         video_file: str,
                         out_video_file: str,
                         start_image_file: str = None,
                         end_image_file: str = None,
                         start_seconds: int = 2,
                         end_seconds: int = 2,
                         video_width:int = 1280,
                         video_height: int = 720,
                         frame_rate: int = 30,
                         bit_rate: str = '1M',
                         audio_sampling_rate: int = 44100,
                         audio_channel_layout: str = 'mono',
                         source_video_to_mp4: bool = False,  # video_file是否需要转为MP4
                         delete_temp: bool = True):
        """
        把图片拼接到视频前后，就是在视频前或者视频后拼接图片生成的视频。

        Args:
            video_file: 视频文件。
            out_video_file: 输出视频文件。
            start_image_file(str): 加到视频头的图片文件。
            end_image_file(str): 加到视频尾的图片文件。
            start_seconds(int): 开始图片的视频时长。
            end_seconds(int): 结束图片的视频时长。
            video_width(int): 视频宽。
            video_height(int): 视频高。
            frame_rate(int): 帧率。
            bit_rate(str): 比特率。
            audio_sampling_rate(int): 音频采样率。
            audio_channel_layout(str): 音频声道。
            source_video_to_mp4(bool): video_file是否需要转为MP4。
            delete_temp(bool): 是否删除临时文件。
        """
        video_file_vo = FileVO(video_file)
        if not video_file_vo.is_file:
            raise FileNotFoundError(f"视频文件 {video_file} 不存在")

        if not start_image_file and not end_image_file:
            raise FileNotFoundError(f"必须指定一个图片文件")

        ffmpeg_handler = FfmpegHandler(log_to_ui_func=self.log_to_ui_func)
        try:
            start_image_mp4 = None
            if start_image_file:
                start_image_mp4 = ffmpeg_handler.image_to_mp4(image_file_path=start_image_file,
                                                              seconds=start_seconds,
                                                              width=video_width,
                                                              height=video_height,
                                                              frame_rate=frame_rate,
                                                              audio_sampling_rate=audio_sampling_rate)
            end_image_mp4 = None
            if end_image_file:
                end_image_mp4 = ffmpeg_handler.image_to_mp4(image_file_path=end_image_file,
                                                            seconds=end_seconds,
                                                            width=video_width,
                                                            height=video_height,
                                                            frame_rate=frame_rate,
                                                            audio_sampling_rate=audio_sampling_rate)
            tmp_file_path = None
            if source_video_to_mp4:
                tmp_file_path = os.path.join(video_file_vo.file_dir, video_file_vo.file_only_name + '_tmp.mp4')
                ffmpeg_handler.to_mp4(video_file_path=video_file,
                                      out_file_path=tmp_file_path,
                                      scale=f'{video_width}:{video_height}',
                                      frame_rate=frame_rate,
                                      bit_rate=bit_rate,
                                      use_cuda=self._args['use_cuda'])
                if os.path.exists(tmp_file_path):
                    video_file = tmp_file_path

            if os.path.exists(video_file):
                if start_image_mp4 or end_image_mp4:
                    concat_files = []
                    if start_image_mp4 and os.path.exists(start_image_mp4):
                        concat_files.append(start_image_mp4)

                    concat_files.append(video_file)

                    if end_image_mp4 and os.path.exists(end_image_mp4):
                        concat_files.append(end_image_mp4)

                    # out_mp4 = os.path.join(video_file_vo.file_dir,
                    #                        video_file_vo.file_only_name + '_' + UuidUtils.generate_time_id() + '.mp4')
                    ffmpeg_handler.concat_mp4(out_file_path=out_video_file,
                                              concat_files=concat_files,
                                              scale=f"{video_width}:{video_height}",
                                              frame_rate=frame_rate,
                                              bit_rate=bit_rate,
                                              use_cuda=self._args['use_cuda'])

                    if delete_temp:
                        if start_image_mp4 and os.path.exists(start_image_mp4):
                            os.remove(start_image_mp4)
                        if end_image_mp4 and os.path.exists(end_image_mp4):
                            os.remove(end_image_mp4)
                        if tmp_file_path and os.path.exists(tmp_file_path):
                            os.remove(tmp_file_path)

                    return out_video_file
            return None
        finally:
            ffmpeg_handler.stop()

    def extract_mp3(self, video_file_path: str) -> str | None:
        """
        从视频文件中提取 MP3 音频。

        Args:
            video_file_path: 视频文件路径。

        Returns:
            提取的 MP3 文件路径。

        Raises:
            FileNotFoundError: 如果视频文件不存在。
            RuntimeError: 如果音频提取失败。
        """
        return self._extract_audio(video_file_path, codec='libmp3lame', ext_name='mp3')

    def extract_wav(self, video_file_path: str, codec: str = 'pcm_s16le') -> str | None:
        """
        从视频文件中提取 WAV 音频。

        Args:
            video_file_path: 视频文件路径。
            codec: 音频编码格式，支持 ['pcm_s16le', 'pcm_s24le', 'pcm_s32le']。

        Returns:
            提取的 WAV 文件路径。

        Raises:
            ValueError: 如果 codec 不支持。
            FileNotFoundError: 如果视频文件不存在。
            RuntimeError: 如果音频提取失败。
        """
        if codec not in ['pcm_s16le', 'pcm_s24le', 'pcm_s32le']:
            raise ValueError(f"不支持的 codec 值: {codec}")
        return self._extract_audio(video_file_path, codec=codec, ext_name='wav')

    def _extract_audio(self, video_file_path: str, codec: str, ext_name: str) -> str | None:
        """
        使用 FFmpeg 从视频文件中提取音频。

        Args:
            video_file_path: 视频文件路径。
            codec: 音频编码格式。
            ext_name: 输出文件扩展名。

        Returns:
            提取的音频文件路径。

        Raises:
            FileNotFoundError: 如果视频文件不存在。
            RuntimeError: 如果音频提取失败。
        """
        video_file_vo = FileVO(video_file_path)
        if not video_file_vo.is_file:
            raise FileNotFoundError(f"视频文件 {video_file_path} 不存在")

        output_dir = video_file_vo.file_dir
        os.makedirs(output_dir, exist_ok=True)

        output = os.path.join(output_dir, f"{video_file_vo.file_only_name}.{ext_name}")

        ffmpeg_handler = FfmpegHandler(log_to_ui_func=self.log_to_ui_func)
        try:
            ffmpeg_handler.extract_audio(video_file_path=video_file_path, out_file_path=output)
            if os.path.exists(output):
                return output
            return None
        finally:
            ffmpeg_handler.stop()

    def embed_subtitles(self, video_file_path: str, asr_data: ASRData, vcodec: str = 'libx264') -> ASRData:
        """
        将字幕嵌入到视频文件中。

        Args:
            video_file_path: 视频文件路径。
            asr_data: 包含字幕数据的 ASRData 对象。
            vcodec: 视频编码格式。

        Returns:
            处理后的 ASRData 对象。

        Raises:
            RuntimeError: 如果视频文件不存在或字幕嵌入失败。
        """
        if not self._args['is_embed_subtitle']:
            self.log_warning("无需合成，系统配置为‘不把字幕合成到视频’")
            return asr_data

        self.log_info("开始: 嵌入字幕到视频文件")

        video_file_vo = FileVO(video_file_path)
        if not video_file_vo.is_file:
            raise FileNotFoundError(f"视频文件 {video_file_path} 不存在")

        temp_dir = os.path.join(video_file_vo.file_dir, "out")
        os.makedirs(temp_dir, exist_ok=True)

        temp_subtitle = os.path.join(temp_dir, f"temp_{int(time.time())}.ass")
        try:
            asr_data.to_ass(style_str=self._args['style_str'],
                            layout=self._args['subtitle_layout'],
                            save_path=temp_subtitle)
            if os.path.exists(temp_subtitle):
                output = os.path.join(temp_dir, f"【LS】{video_file_vo.file_only_name}.{video_file_vo.file_extension}")
                if self._args['is_soft_subtitle']:
                    self._add_soft_subtitles(video_file_path, temp_subtitle, output)
                else:
                    self._add_hard_subtitles(video_file_path, temp_subtitle, output, self._args['quality'], vcodec)
                self.log_info(f"嵌入字幕的视频文件：{output}")
            else:
                self.log_warning(f"待嵌入的字幕不存在：{temp_subtitle}")
            return asr_data
        finally:
            if os.path.exists(temp_subtitle):
                os.remove(temp_subtitle)
            self.log_info("完成：嵌入字幕到视频文件。")

    def _add_hard_subtitles(self, video_file_path: str, subtitle_file: str, output: str,
                            quality: Literal[
                                'ultrafast', 'superfast', 'veryfast', 'faster', 'fast',
                                'medium', 'slow', 'slower', 'veryslow'
                            ],
                            vcodec: str) -> str | None:
        """
        使用硬字幕将字幕嵌入到视频文件中。

        Args:
            video_file_path: 视频文件路径。
            subtitle_file: 字幕文件路径。
            output: 输出文件路径。
            quality: 压制质量。
            vcodec: 视频编码格式。

        Returns:
            嵌入字幕后的视频文件路径。

        Raises:
            RuntimeError: 如果字幕嵌入失败。
        """
        ffmpeg_handler = FfmpegHandler(log_to_ui_func=self.log_to_ui_func)
        try:
            ffmpeg_handler.add_hard_subtitles(video_file_path=video_file_path,
                                              subtitle_file=subtitle_file,
                                              out_file_path=output,
                                              quality=quality,
                                              vcodec=vcodec)
            if os.path.exists(output):
                return output
            return None
        finally:
            ffmpeg_handler.stop()

    def _add_soft_subtitles(self, video_file_path: str, subtitle_file: str, output: str) -> str | None:
        """
        使用软字幕将字幕嵌入到视频文件中。

        Args:
            video_file_path: 视频文件路径。
            subtitle_file: 字幕文件路径。
            output: 输出文件路径。

        Returns:
            嵌入字幕后的视频文件路径。

        Raises:
            RuntimeError: 如果字幕嵌入失败。
        """
        ffmpeg_handler = FfmpegHandler(log_to_ui_func=self.log_to_ui_func)
        try:
            ffmpeg_handler.add_soft_subtitles(video_file_path=video_file_path,
                                              subtitle_file=subtitle_file,
                                              out_file_path=output)
            if os.path.exists(output):
                return output
            return None
        finally:
            ffmpeg_handler.stop()

    def read_use_cuda(self) -> bool:
        if 'use_cuda' in self._args:
            if self._args['use_cuda'] is None:
                self._args['use_cuda'] = self.check_cuda_available()
        else:
            self._args['use_cuda'] = self.check_cuda_available()

        return self._args['use_cuda']

    def check_cuda_available(self) -> bool:
        """
        检查 CUDA 是否可用。

        Returns:
            CUDA 是否可用。
        """
        ffmpeg_handler = FfmpegHandler(log_to_ui_func=self.log_to_ui_func)
        try:
            return ffmpeg_handler.check_cuda_available()
        finally:
            ffmpeg_handler.stop()

    def get_video_info(self, file_path: str) -> Dict[str, Any]:
        """获取视频文件的详细信息。

        Args:
            file_path (str): 视频文件的路径。

        Returns:
            Dict[str, Any]: 包含视频信息的字典。如果发生错误，返回的字典中所有值将被初始化为空字符串或0。
        """
        ffmpeg_handler = FfmpegHandler(log_to_ui_func=self.log_to_ui_func)
        try:
            return ffmpeg_handler.get_video_info(file_path=file_path)
        finally:
            ffmpeg_handler.stop()
