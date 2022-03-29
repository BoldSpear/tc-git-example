from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import PollCreateForm, VoteForm, PollUpdateForm
from .models import Topic, Vote, Option


def view_all_polls(request):  # request: an instance of http request. GET or POST or PUT or DELETE
    topics = Topic.objects.all()
    context = {
        'topics': topics
    }
    return render(request, 'pages/view_all_polls.html', context)
    # method = request.method
    # name = request.GET.get('name', 'username')
    # if method == 'GET':
    #     data = request.GET.urlencode()
    # elif method == 'POST':
    #     data = request.POST.urlencode()
    #
    # return HttpResponse("method is %s name: %s " % (method, name))


def create_poll(request):
    if request.method == 'POST':
        form = PollCreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['topic']
            options = form.cleaned_data['options'].split(',')

            topic = Topic(title=title)
            topic.save()

            for item in options:
                Option.objects.create(name=item, topic=topic)
            return HttpResponseRedirect('/polls/')
    else:
        form = PollCreateForm()
    form = PollCreateForm()
    context ={
        'create_form': form
    }
    return render(request, 'pages/create_poll.html', context)


def view_poll_by_id(request, id):
    topic = Topic.objects.get(id=id)
    options = Option.objects.filter(topic=topic).all()

    total_votes = Vote.objects.filter(topic=topic).count()

    results = {}

    for item in options:
        vote_count = Vote.objects.filter(option=item).count()
        if total_votes > 0:
            percent = vote_count / total_votes *100
            result_text = 'num of vote: %d, proportion: %.2f' % (vote_count, percent)
        else:
            result_text = 'No vote available'
        results[item.name] = result_text

    context = {
        'topic': topic,
        'results': results
    }

    #return HttpResponse('view poll ' + str(id))
    return render(request, 'pages/view_poll_by_id.html', context)


def vote_poll(request, id):
    topic = Topic.objects.get(id=id)

    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/polls/%d' % id)
    else:
        form = VoteForm()

    form.fields['topic'].initial = topic
    form.fields['option'].queryset = Option.objects.filter(topic=topic).all()

    context = {
        'form': form,
        'topic': topic
    }
    return render(request, 'pages/vote_poll.html', context)


def update_poll(request, id):
    topic = Topic.objects.get(id=id)

    if request.method == 'POST':
        form = PollUpdateForm(request.POST, instance=topic)    # update 할 instance 를 지정, not new
        if form.is_valid():
            form.save()

            # 기존 옵션을 삭제
            Option.objects.filter(topic=topic).delete()

            # 새로운 옵션을 추가
            options_new = form.cleaned_data['options'].split(',')
            for item in options_new:
                Option.objects.create(name=item, topic=topic)
            return HttpResponseRedirect('/polls/%d/' % id)
    else:
         form = PollUpdateForm(instance=topic)

    options = Option.objects.filter(topic=topic).all()
    joined = ",".join(item.name for item in options)
    form.fields['options'].initial = joined

    context = {
        'update_form': form,
        'topic': topic
    }
    return render(request, 'pages/update_poll.html', context)


def delete_poll(request, id):
    topic = Topic.objects.get(id=id)
    topic.delete()

    return HttpResponseRedirect('/polls')
