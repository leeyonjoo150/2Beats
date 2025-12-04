from django.core.management.base import BaseCommand
from django.db.models import Count
from apps.twobeats_upload.models import Video

class Command(BaseCommand):
    help = '기존 영상들의 좋아요 수를 video_like_count 필드에 동기화'

    def handle(self, *args, **kwargs):
        # 모든 영상의 실제 좋아요 수 집계
        videos = Video.objects.annotate(
            actual_like_count=Count('videolike')
        )

        updated_count = 0
        for video in videos:
            # video_like_count 필드 업데이트
            if video.video_like_count != video.actual_like_count:
                video.video_like_count = video.actual_like_count
                video.save(update_fields=['video_like_count'])
                updated_count += 1
                self.stdout.write(
                    f'[OK] {video.video_title}: {video.actual_like_count}개'
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n총 {updated_count}개 영상의 좋아요 수 동기화 완료!')
        )
