""" представления Объявлений """
import time
import django.dispatch
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.http import HttpResponseNotFound
from .models import Advert, Comment
from .forms import AdvertForm, CommentForm, UserPageFilterForm


# сигнал об удалении комментария автором объявления
comment_not_accepted = django.dispatch.Signal()

class MainPage(TemplateView):
    template_name = 'advert/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Advert.CATEGORY_CHOICES
        if 'category_id' in self.kwargs:
            context['current_category_title'] = Advert.CATEGORY_CHOICES[self.kwargs['category_id']][1]
            context['current_category_key'] = Advert.CATEGORY_CHOICES[self.kwargs['category_id']][0]
        return (context)


# обработка AJAX запроса выдачи блоков объявлений
# размер блока определяется константой внутри фугкции
def get_adverts(request):
    """ обработка AJAX запроса выдачи блока объявлений """

    BLOCK_SIZE = 4 # количество единовременно загружаемых объявлений

    new_last_date = None
    adverts = Advert.objects.all() 
    if 'category' in request.GET and request.GET.get('category'):
        adverts = adverts.filter(category=request.GET.get('category'))
    if 'last_date' in request.GET and request.GET.get('last_date'):
        time.sleep(1) # имитируем напряженную работу сервера
        last_date = request.GET.get('last_date')
        adverts = Advert.objects.filter(created_at__lt=last_date)
    if adverts:
        if adverts.count()>BLOCK_SIZE:
            adverts = adverts[:BLOCK_SIZE]
            new_last_date = adverts[-1].created_at.strftime('%Y-%m-%d %H:%M:%S.%f')
    return render(request, 'advert/get_adverts.html', {
                                                        'adverts': adverts,
                                                        'last_date': new_last_date,
                                                        'user': request.user
                                                        })


class OneAdvert(DetailView):
    """ представления единичного  объявления """
    model = Advert
    template_name = 'advert/one_advert.html'
    context_object_name = 'advert'


class EditAdvert(LoginRequiredMixin):
    """ редактирование оьщий класс """
    template_name = 'advert/edit_advert.html'
    form_class = AdvertForm 

    def form_invalid(self, form, **kwargs):
        if 'errors' not in form.errors:
            messages.error(self.request, form.errors)
        return super().form_invalid(form)
    
    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class CreateAdver(EditAdvert, CreateView):
    """ Добавление объявления """
    extra_context = {'title': 'Добавоение объявления'}
    success_message = 'Объявление успешно добавлено !'

    def get_form_kwargs(self):
        """ инициализация поля -автор- формы  """
        kwargs = super().get_form_kwargs()
        kwargs['author'] = self.request.user
        return kwargs


class UpdateAdvert(EditAdvert, UserPassesTestMixin, UpdateView):
    """ редактирование объявления """
    extra_context = {'title': 'Редактирование объявления'}
    success_message = 'Объявление успешно изменено !'

    def get_object(self, **kwargs):
        return get_object_or_404(Advert, pk=self.kwargs.get('pk'))
    
    def test_func(self):
        return self.request.user == self.get_object().author

   
class DeleteAdvert(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'advert/delete_advert.html'
    queryset = Advert.objects.all()
    success_url = reverse_lazy('main')

    def test_func(self):
        return self.request.user == self.get_object().author    


#-----------------------  обработка AJAX запросов работы с комментариями --------------------------------

def comment_accept(request):
    """ обработка AJAX запроса изменения статуса комментария """

    if request.method == 'POST' and 'pk' in request.POST and request.POST.get('pk'):
        comment = get_object_or_404(Comment, pk=int(request.POST.get('pk')))
        if comment.advert.author == request.user:
            comment.accepted = True
            comment.save(update_fields=['accepted'])
            return HttpResponse('success')
    return HttpResponseNotFound()


def comment_delete(request):
    """ обработка AJAX запроса удаления комментария """

    if request.method == 'POST' and 'pk' in request.POST and request.POST.get('pk'):
        comment = get_object_or_404(Comment, pk=request.POST.get('pk'))
        if comment.advert.author == request.user or comment.author == request.user:
            if comment.advert.author == request.user:
                comment_not_accepted.send(sender=Comment, instance=comment)
            comment.delete()
            return HttpResponse('success')
    return HttpResponseNotFound()


@login_required()
def comment_get_update_form(request):
    """ обработка AJAX запроса получения заполненной формы """
 
    if request.method == 'GET' and 'pk' in request.GET and request.GET.get('pk'):
        comment = get_object_or_404(Comment, pk=request.GET.get('pk'))
        form = CommentForm(instance=comment)
        return render(request, 'advert/get_comment_form.html', {'form' : form, })
    return HttpResponseNotFound()


def comment_update(request, pk):
    """ обработка AJAX запроса обработки формы обновления комментария """

    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=pk)
        if comment.author == request.user:
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
            else:
                messages.error(request, form.errors)
            return HttpResponseRedirect(reverse('one_advert',
                                                args=[request.POST.get('advert')]) 
                                                + f'#comment_div_{pk}')
    return HttpResponseNotFound()


@login_required()
def comment_get_add_form(request):
    """ обработка AJAX запроса получения пустой формы """
  
    if request.method == 'GET' and 'advert' in request.GET and request.GET.get('advert'):
        advert = get_object_or_404(Advert, pk=request.GET.get('advert'))
        form = CommentForm(advert=advert, author=request.user)
        return render(request, 'advert/get_comment_form.html', {'form' : form, })
    return HttpResponseNotFound()


def comment_add(request):
    """ обработка AJAX запроса обработки формы добавления комментария """

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, form.errors)
        return HttpResponseRedirect(reverse('one_advert', 
                                            args=[request.POST.get('advert')]) 
                                            + '#comments')
    return HttpResponseNotFound()


#----------------------------------------------------------------------------------------------------------

class UserPage(LoginRequiredMixin, ListView):
    """ представление всех новостей и комментариев пользователя """

    model = Advert
    context_object_name = 'adverts'
    extra_context = {'title': 'Моя страница'}
    template_name = 'advert/user_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Advert.CATEGORY_CHOICES
        if 'category' in self.request.GET:
            context['current_category_title'] = Advert.get_category_title(self.request.GET['category'])
        context['filter_form'] = UserPageFilterForm(self.request.GET)
        return (context)

    def get_queryset(self):
        adverts = Advert.objects.filter(author=self.request.user)
        if 'category' in self.request.GET and self.request.GET['category']:
            adverts = adverts.filter(category=self.request.GET['category'])
        if 'with_new_comment_only' in self.request.GET:
            adverts = adverts.filter(comment__accepted=False)
        return adverts