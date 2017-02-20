from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from datetime import datetime
from .models import Account

def show(request):
    return render(request, 'account/home.html',
                  {'all_list':Account.objects.order_by('save_date')})
    
def save_list(request):
    money = float(request.POST['money'].replace("," , ""))
    try:
        last_balance = Account.objects.order_by('-save_date', '-id')[0].balance
        last_date = Account.objects.order_by('-save_date')[0].save_date
    except:
        last_balance = 0
        last_date = datetime.strptime("01/01/0001", "%d/%m/%Y").date()
    
    date = datetime.strptime(request.POST['date'], "%d/%m/%Y").date()
    if(request.POST['in_type'] == 'income'):
        record = Account(save_date = date,
                                            detail_text = request.POST['detail'],
                                            income = money,
                                            balance = last_balance+money)
        record.save()
    else:
        record = Account(save_date = date,
                                            detail_text = request.POST['detail'],
                                            expenses = money,
                                            balance = last_balance-money)
        record.save()
        
    if(date < last_date):
        update_balance(date)
            
    return HttpResponseRedirect(reverse('account:show'))

def update_balance(date_insert):
    tmp = 0
    for account_list in Account.objects.order_by('save_date', 'id'):
        if account_list.save_date < date_insert:
            tmp = account_list.balance
        else:
            if account_list.income > 0:
                tmp += account_list.income
                account_list.balance = tmp
            else:
                tmp -= account_list.expenses
                account_list.balance = tmp
            account_list.save()
            
def custom(request):
    return render(request, 'account/custom.html',
                  {'all_list':Account.objects.order_by('save_date')})

def remove(request,remove_id):
    return render(request, 'account/custom.html',
                  {'all_list':Account.objects.order_by('save_date'),
                   'remove_id':int(remove_id)})
                  
def remove_confirm(request,remove_id):
    record = Account.objects.get(pk=remove_id)
    record.delete()
    update_balance(datetime.strptime("01/01/0001", "%d/%m/%Y").date())    
    return HttpResponseRedirect(reverse('account:customize'))

def edit(request,edit_id):
    return render(request, 'account/custom.html',
                  {'all_list':Account.objects.order_by('save_date'),
                   'edit_id':int(edit_id)})

def edit_save(request,edit_id):
    record = Account.objects.get(pk=edit_id)
    record.save_date = datetime.strptime(request.POST['date'], "%d/%m/%Y").date()
    record.detail_text = request.POST['detail']
    if(request.POST['in_type'] == 'income'):
        record.income = float(request.POST['money'].replace("," , ""))
        record.expenses = 0
    else:
        record.income = 0
        record.expenses = float(request.POST['money'].replace("," , ""))
    record.save()
    update_balance(datetime.strptime("01/01/0001", "%d/%m/%Y").date())
    return HttpResponseRedirect(reverse('account:customize'))
