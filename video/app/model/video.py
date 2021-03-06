# coding:utf-8
from enum import Enum
from django.db import models


class VideoType(Enum):
    movie = 'movie'
    cartoon = 'cartoon'
    episcode = 'episcode'
    variety = 'variety'
    other = 'other'


VideoType.movie.label = '电影'
VideoType.cartoon.label = '卡通'
VideoType.episcode.label = '剧集'
VideoType.variety.label = '综艺'
VideoType.movie.label = '其他'


class FromType(Enum):
    youku = 'youku'
    custom = 'custom'


FromType.youku.lable = '优酷'
FromType.custom.label = '自制'


class Nation(Enum):
    china = 'china'
    japan = 'japan'
    korea = 'korea'
    america = 'america'
    other = 'other'


Nation.china.lable = '中国'
Nation.china.lable = '日本'
Nation.china.lable = '韩国'
Nation.china.lable = '美国'
Nation.china.lable = '其他'


class Video(models.Model):
    name = models.CharField(max_length=100, null=False)
    image = models.CharField(max_length=500, default='')
    video_type = models.CharField(max_length=50, default=VideoType.other.value)
    from_to = models.CharField(max_length=50, null=False, default=FromType.custom.value)
    nation = models.CharField(max_length=20, null=True, default='')
    into = models.TextField()
    status = models.BooleanField(default=True, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'video_type', 'from_to', 'nation')

    def __str__(self):
        return self.name


class VideoStar(models.Model):
    video = models.ForeignKey(Video,
                              related_name='video_star',
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True
                              )
    name = models.CharField(max_length=100, null=False)
    identity = models.CharField(max_length=50, default='')

    class Meta:
        unique_together = ('video', 'name', 'identity')

    def __str__(self):
        return self.name


class VideoSub(models.Model):
    video = models.ForeignKey(Video,
                              related_name='video_sub',
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True
                              )
    url = models.CharField(max_length=500, null=False)
    number = models.IntegerField(default=1)

    class Meta:
        unique_together = ('video', 'number')

    def __str__(self):
        return 'video:{},number:{}'.format(self.video.name, self.number)


class IdentityType(Enum):
    to_star = 'to_star'
    suporting_rule = 'suporting_rule'
    director = 'director'
