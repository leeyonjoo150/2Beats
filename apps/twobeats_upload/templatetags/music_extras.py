from django import template
from apps.twobeats_music_explore.models import MusicLike

register = template.Library()

@register.filter
def has_liked(user, music):
    """사용자가 해당 음악에 좋아요를 눌렀는지 확인"""
    if user.is_authenticated:
        return MusicLike.objects.filter(user=user, music=music).exists()
    return False