import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import random
import redis
from django.urls import reverse
# from restcountries import RestCountryApiV2 as rapi
from FlagQuiz import settings
from Home.forms import OpiForm
from Home.models import Question, QuestionCapital

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


# Create your views here.

def main_view(request):
    user = request.user

    return render(request, 'home/main.html', {'user': user})


def end_game_view(request, num):
    profile = request.user.profile
    point = int(r.get(f'point:{profile.id}:{num}'))
    r.set(f'point:{profile.id}:{num}', 0)
    r.set(f'round:{profile.id}:{num}', 0)
    r.set(f'attempts:{profile.id}:{num}', 3)
    context = {'profile': profile, 'point': point, 'num': num}
    return render(request, 'home/end_game.html', context)


# def test_db(request):
#     all_countries = rapi.get_all()
#     for i in range(5):
#         opinions = random.sample(all_countries, k=4)
#         op1 = opinions[0].capital
#         op2 = opinions[1].capital
#         op3 = opinions[2].capital
#         op4 = opinions[3].capital
#
#         QuestionCapital.objects.create(op1=op1, op2=op2, op3=op3, op4=op4)
#     return render(request, 'home/db.html', {})


def game_view(request, num):
    profile = request.user.profile
    form = OpiForm(request.GET)
    if num == 1:
        try:
            question_num = r.get(f'question_num:{profile.id}:{num}')
            question = Question.objects.get(pk=question_num)
            # get question
        except:
            r.set(f'question_num:{profile.id}:{num}', 1)
            question_num = r.get(f'question_num:{profile.id}:{num}')
            question = Question.objects.get(pk=question_num)

    else:
        try:
            question_num = r.get(f'question_num:{profile.id}:{num}')
            question = QuestionCapital.objects.get(pk=question_num)
            # get question
        except:
            r.set(f'question_num:{profile.id}:{num}', 1)
            question_num = r.get(f'question_num:{profile.id}:{num}')
            question = QuestionCapital.objects.get(pk=question_num)
    opinions = [question.op1, question.op2, question.op3, question.op4]
    answer = opinions[question.answer - 1]  # name of answer country
    if num == 1:
        #  flag = rapi.get_countries_by_name(answer)[0].flag  # flag
        flag_json = requests.get('https://restcountries.com/v3.1/name/%s' % answer).json()
        flag = flag_json[0]['flags']['png']
    else:

        flag_json = requests.get('https://restcountries.com/v3.1/capital/%s' % answer).json()
        flag = flag_json[0]['flags']['png']
    if form.is_valid():
        obj = form.cleaned_data['opinion']
        r.incr(f'round:{profile.id}:{num}')
        if obj == question.answer:  # check answer
            r.incr(f'point:{profile.id}:{num}')
        else:
            r.decr(f'attempts:{profile.id}:{num}')
        return redirect('ins', num=num)

    try:

        point = int(r.get(f'point:{profile.id}:{num}'))
        attempts = int(r.get(f'attempts:{profile.id}:{num}'))

        round_game = int(r.get(f'round:{profile.id}:{num}'))

    except:
        r.set(f'point:{profile.id}:{num}', 0)
        r.set(f'attempts:{profile.id}:{num}', 3)
        r.set(f'round:{profile.id}:{num}', 0)
        round_game = int(r.get(f'round:{profile.id}:{num}'))
        point = int(r.get(f'point:{profile.id}:{num}'))
        attempts = int(r.get(f'attempts:{profile.id}:{num}'))

    if attempts <= 0:  # end game
        profile.computing_record(point, num)
        return HttpResponseRedirect(reverse('end_game'))
    context = {
        'profile': profile,
        'round': round_game,
        'point': point,
        'flag': flag,
        'question': question,
        'attempts': attempts,
        'num': num
    }
    return render(request, 'home/game.html', context)


def ins_view(request, num):  # view for increase point
    profile = request.user.profile
    r.incr(f'question_num:{profile.id}:{num}')
    return redirect('game', num=num)
