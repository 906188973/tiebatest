from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Topic, poster, Poster_reply
from .forms import TopicForm, PosterForm, PosterReplyForm
from django.db.models import Max
# Create your views here.
def index(request):
    """贴吧主页"""
    return render(request, 'tiebas/index.html')

def topics(request):
    """显示所有帖子主题"""
    topics = Topic.objects.order_by('date_added')
    """创建新贴"""
    if request.method != 'POST':
        form_topic = TopicForm()
        form_poster = PosterForm()
    else:
        form_topic = TopicForm(request.POST)
        form_poster = PosterForm(request.POST)
        if form_topic.is_valid() and form_poster.is_valid():
            topic = form_topic.save(commit=False)
            topic.floor_many = 1
            topic.owner = request.user
            topic.save()
            new_poster = form_poster.save(commit=False)
            new_poster.owner = request.user
            new_poster.topic = topic
            new_poster.floor = 1
            new_poster.save()
            return HttpResponseRedirect(reverse('tiebas:topics'))
    context = {'topics': topics, 'form_topic': form_topic, 'form_poster': form_poster}
    return render(request, 'tiebas/topics.html', context)

def topic(request, topic_id):
    """显示帖子"""
    topic = Topic.objects.get(id=topic_id)
    posters = topic.poster_set.order_by('date_added')

    """回复帖子"""
    if request.method != 'POST':
        form = PosterForm()
    else:
        form = PosterForm(request.POST)
        if form.is_valid():
            obj = poster.objects.filter(topic_id=topic_id).aggregate(max=Max('floor'))
            new_poster = form.save(commit=False)
            new_poster.owner = request.user
            new_poster.topic = topic
            new_poster.floor = obj['max'] + 1
            new_poster.save()
            topic.floor_many += 1
            topic.save()
            return HttpResponseRedirect(reverse('tiebas:topic', args=[topic_id]))
    context = {'topic': topic, 'posters': posters, 'form': form}

    return render(request, 'tiebas/topic.html', context)

def update_comment(request):
    data = {}
    if request.method == 'POST':
            user = request.user
            text = request.POST.get('reply_text', '')
            poster_id = int(request.POST.get('poster_id', ''))
            new_poster = poster.objects.get(id=poster_id)
            reply_comment_id = int(request.POST.get('reply_comment_id'))

            comment = Poster_reply()
            comment.owner = user
            comment.text = text
            comment.poster = new_poster

            if reply_comment_id != 0:

                obj = Poster_reply.objects.get(id=reply_comment_id)
                comment.by_owner = obj.owner
                data['by_owner'] = obj.owner.username
                data['owner_status'] = True
            else:
                data['owner_status'] = False
            comment.save()

    # referer = request.META.get('HTTP_REFERER', reverse('tiebas:index'))
    # return redirect(referer)
            data['status'] = True
            data['username'] = comment.owner.username
            data['comment_time'] = comment.date_added.strftime('%Y-%m-%d %H:%M:%S')
            data['text'] = comment.text
            data['reply_id'] = comment.id
    else:
        data['status'] = False
    return JsonResponse(data)

def poster_del(request, id):
    if request.method == 'POST':
        poster_id = int(id)
        obj = poster.objects.get(id=poster_id)
        topic_obj = obj.topic
        topic_obj.floor_many = topic_obj.floor_many-1
        topic_obj.save()
        obj.delete()
        return JsonResponse({'status': 'True'})

def reply_del(request, id):
    if request.method == 'POST':
        reply_id = int(id)
        Poster_reply.objects.get(id=reply_id).delete()
        return JsonResponse({'status': 'True'})