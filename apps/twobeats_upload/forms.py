# apps/twobeats_upload/forms.py

import os
from django import forms
from django.core.exceptions import ValidationError
from .models import Music, Video, Tag


# 🔥 음악 파일 검증 함수
def validate_audio_file(file):
    """음악 파일만 허용"""
    # 허용 확장자
    valid_extensions = ['.mp3', '.wav', '.flac', '.aiff', '.alac', '.m4a', '.ogg', '.wma', '.aac']
    
    # 파일 확장자 추출
    ext = os.path.splitext(file.name)[1].lower()
    
    if ext not in valid_extensions:
        raise ValidationError(
            f'음악 파일만 업로드 가능합니다. (허용: {", ".join(valid_extensions)})'
        )
    
    # 파일 크기 제한 (예: 100MB)
    max_size = 100 * 1024 * 1024  # 100MB
    if file.size > max_size:
        raise ValidationError(f'파일 크기는 100MB를 초과할 수 없습니다.')
    
    # MIME 타입 검증 (더 엄격)
    valid_mime_types = [
        'audio/mpeg',      # MP3
        'audio/wav',       # WAV
        'audio/x-wav',     # WAV
        'audio/flac',      # FLAC
        'audio/x-flac',    # FLAC
        'audio/aiff',      # AIFF
        'audio/x-aiff',    # AIFF
        'audio/mp4',       # M4A/AAC
        'audio/x-m4a',     # M4A
        'audio/ogg',       # OGG
        'audio/x-ms-wma',  # WMA
    ]
    
    # content_type 체크 (있으면)
    if hasattr(file, 'content_type') and file.content_type:
        if file.content_type not in valid_mime_types:
            raise ValidationError(
                f'올바른 음악 파일이 아닙니다. (MIME 타입: {file.content_type})'
            )


# 🔥 비디오 파일 검증 함수
def validate_video_file(file):
    """비디오 파일만 허용"""
    valid_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv', '.wmv', '.m4v']
    
    ext = os.path.splitext(file.name)[1].lower()
    
    if ext not in valid_extensions:
        raise ValidationError(
            f'비디오 파일만 업로드 가능합니다. (허용: {", ".join(valid_extensions)})'
        )
    
    # 파일 크기 제한 (예: 500MB)
    max_size = 500 * 1024 * 1024  # 500MB
    if file.size > max_size:
        raise ValidationError(f'파일 크기는 500MB를 초과할 수 없습니다.')
    
    valid_mime_types = [
        'video/mp4',
        'video/quicktime',  # MOV
        'video/x-msvideo',  # AVI
        'video/x-matroska', # MKV
        'video/webm',
        'video/x-flv',
        'video/x-ms-wmv',
    ]
    
    if hasattr(file, 'content_type') and file.content_type:
        if file.content_type not in valid_mime_types:
            raise ValidationError(
                f'올바른 비디오 파일이 아닙니다. (MIME 타입: {file.content_type})'
            )


# 🔥 이미지 파일 검증 함수
def validate_image_file(file):
    """이미지 파일만 허용"""
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    
    ext = os.path.splitext(file.name)[1].lower()
    
    if ext not in valid_extensions:
        raise ValidationError(
            f'이미지 파일만 업로드 가능합니다. (허용: {", ".join(valid_extensions)})'
        )
    
    # 파일 크기 제한 (예: 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    if file.size > max_size:
        raise ValidationError(f'이미지 크기는 10MB를 초과할 수 없습니다.')


# Forms

class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = [
            'music_title',
            'music_singer',
            'music_type',
            'music_root',
            'music_thumbnail',
            'tags',
        ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple,
            'music_thumbnail': forms.FileInput(attrs={
                'accept': 'image/*',
            }),
            'music_root': forms.FileInput(attrs={
                'accept': 'audio/*,.mp3,.wav,.flac,.aiff,.alac,.m4a,.ogg',
            }),
        }
    
    # 🔥 필드별 검증 추가
    def clean_music_root(self):
        file = self.cleaned_data.get('music_root')
        if file:
            validate_audio_file(file)
        return file
    
    def clean_music_thumbnail(self):
        file = self.cleaned_data.get('music_thumbnail')
        if file:
            validate_image_file(file)
        return file


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = [
            'video_title',
            'video_singer',
            'video_type',
            'video_root',
            'video_thumbnail',
            'video_detail',
            'tags',
        ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple,
            'video_thumbnail': forms.FileInput(attrs={
                'accept': 'image/*',
            }),
            'video_root': forms.FileInput(attrs={
                'accept': 'video/*,.mp4,.mov,.avi,.mkv,.webm,.flv',
            }),
        }
    
    def clean_video_root(self):
        file = self.cleaned_data.get('video_root')
        if file:
            validate_video_file(file)
        return file
    
    def clean_video_thumbnail(self):
        file = self.cleaned_data.get('video_thumbnail')
        if file:
            validate_image_file(file)
        return file


class MusicFileForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['music_root']
        widgets = {
            'music_root': forms.FileInput(attrs={
                'accept': 'audio/*,.mp3,.wav,.flac,.aiff,.alac,.m4a,.ogg',
            }),
        }
    
    def clean_music_root(self):
        file = self.cleaned_data.get('music_root')
        if file:
            validate_audio_file(file)
        return file


class VideoFileForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video_root']
        widgets = {
            'video_root': forms.FileInput(attrs={
                'accept': 'video/*,.mp4,.mov,.avi,.mkv,.webm,.flv',
            }),
        }
    
    def clean_video_root(self):
        file = self.cleaned_data.get('video_root')
        if file:
            validate_video_file(file)
        return file