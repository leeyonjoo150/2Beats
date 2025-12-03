from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.twobeats_upload.models import Music, Tag
import random

'''
디버깅용 소스 생성 추후 삭제 예정 / 25.11.26 Lim
'''


User = get_user_model()

class Command(BaseCommand):
    help = '샘플 음악 데이터 생성'
    
    def handle(self, *args, **kwargs):
        # 관리자 유저 가져오기 (없으면 첫 번째 유저)
        try:
            user = User.objects.filter(is_superuser=True).first()
            if not user:
                user = User.objects.first()
            if not user:
                self.stdout.write(self.style.ERROR('유저가 없습니다. 먼저 슈퍼유저를 생성하세요.'))
                return
        except:
            self.stdout.write(self.style.ERROR('유저를 찾을 수 없습니다.'))
            return
        
        # 태그 가져오기
        tags_list = list(Tag.objects.all())
        
        # 샘플 음악 데이터
        sample_musics = [
            {
                'title': 'Dynamite',
                'singer': 'BTS',
                'type': 'pop',
                'tags': ['신남', '드라이브', '여름'],
            },
            {
                'title': 'Butter',
                'singer': 'BTS',
                'type': 'pop',
                'tags': ['신남', '파티'],
            },
            {
                'title': '봄날',
                'singer': 'BTS',
                'type': 'ballad',
                'tags': ['슬픔', '감성적', '겨울'],
            },
            {
                'title': 'Love Dive',
                'singer': 'IVE',
                'type': 'dance',
                'tags': ['신남', '활기찬'],
            },
            {
                'title': 'Hype Boy',
                'singer': 'NewJeans',
                'type': 'pop',
                'tags': ['신남', '여름', '드라이브'],
            },
            {
                'title': 'Attention',
                'singer': 'NewJeans',
                'type': 'pop',
                'tags': ['신남', '파티'],
            },
            {
                'title': '사건의 지평선',
                'singer': '윤하',
                'type': 'ballad',
                'tags': ['슬픔', '감성적', '새벽'],
            },
            {
                'title': 'Ditto',
                'singer': 'NewJeans',
                'type': 'pop',
                'tags': ['잔잔함', '겨울'],
            },
            {
                'title': 'TOMBOY',
                'singer': '(G)I-DLE',
                'type': 'hiphop',
                'tags': ['신남', '활기찬'],
            },
            {
                'title': '손이 참 곱던 그대',
                'singer': '이영지',
                'type': 'hiphop',
                'tags': ['슬픔', '감성적'],
            },
        ]
        
        created_count = 0
        for music_data in sample_musics:
            # 중복 체크
            if Music.objects.filter(
                music_title=music_data['title'],
                music_singer=music_data['singer']
            ).exists():
                continue
            
            # 음악 생성
            music = Music.objects.create(
                music_title=music_data['title'],
                music_singer=music_data['singer'],
                music_type=music_data['type'],
                uploader=user,
                music_count=random.randint(100, 10000),  # 랜덤 재생수
                music_like_count=random.randint(10, 1000),  # 랜덤 좋아요
            )
            
            # 태그 추가
            for tag_name in music_data['tags']:
                try:
                    tag = Tag.objects.get(name=tag_name)
                    music.tags.add(tag)
                except Tag.DoesNotExist:
                    pass
            
            created_count += 1
            self.stdout.write(f'✅ {music.music_title} - {music.music_singer} 생성')
        
        self.stdout.write(
            self.style.SUCCESS(f'\n총 {created_count}개의 샘플 음악 생성 완료!')
        )