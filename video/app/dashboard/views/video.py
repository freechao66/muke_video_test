# coding:utf-8

from django.views.generic import View
from django.shortcuts import reverse, redirect
from app.libs.base_rander import rander_to_response
from app.model.video import Video
from app.model.video import FromType, VideoSub, VideoStar


class ExternaVideo(View):
    TEMPLATE = 'dashboard/video/externa_video.html'

    def get(self, request):
        error = request.GET.get('error')
        data = {'error': error}
        videos = Video.objects.exclude(from_to=FromType.custom.value)
        data['videos'] = videos
        return rander_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):
        video_name = request.POST.get('video_name')
        img = request.POST.get('img')
        video_type = request.POST.get('video_type')
        from_to = request.POST.get('from_to')
        nation = request.POST.get('nation')
        into = request.POST.get('into')

        if not all([video_name, video_type, img, from_to, nation, into]):
            return redirect('{}?error={}'.format(reverse('externa_video'), '缺少必要字段'))
        Video.objects.create(name=video_name, image=img, video_type=video_type, from_to=from_to, nation=nation,
                             into=into)
        return redirect(reverse('externa_video'))


class VideoSubView(View):
    TEMPLATE = 'dashboard/video/video_sub.html'

    def get(self, request, video_id):
        data = {}
        video = Video.objects.get(pk=video_id)
        error = request.GET.get('error')
        data['video'] = video
        data['error'] = error
        return rander_to_response(request, self.TEMPLATE, data=data)

    def post(self, request, video_id):
        url = request.POST.get('url')
        video = Video.objects.get(pk=video_id)
        VideoSub.objects.create(video=video, url=url, number=video.video_sub.count() + 1)
        return redirect(reverse('videosub', kwargs={'video_id': video_id}))


class VideoStarView(View):
    def post(self, request):
        star = request.POST.get('star')
        identity = request.POST.get('identity')
        video_id = request.POST.get('video_id')
        path_format = '{}'.format(reverse('videosub', kwargs={'video_id': video_id}))

        if not all([star, identity, video_id]):
            return redirect('{}?error={}'.format(path_format, '缺少必要字段'))
        video = Video.objects.get(pk=video_id)
        VideoStar.objects.create(video=video, name=star, identity=identity)
        return redirect(reverse('videosub', kwargs={'video_id': video_id}))


class StarDeleteView(View):
    def get(self, request, star_id, video_id):
        VideoStar.objects.filter(id=star_id).delete()
        return redirect(reverse('videosub', kwargs={'video_id': video_id}))
