from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from datetime import datetime
from .models import Account
import csv, os
from django.contrib.auth.decorators import login_required

@login_required
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
        balance = last_balance+money
    else:
        balance = last_balance-money
    record = Account(save_date = date,
                                      detail_text = request.POST['detail'],
                                      money = money,
                                      money_type = request.POST['in_type'],
                                      balance = balance)
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
            if account_list.money_type == 'income':
                tmp += account_list.money
            else:
                tmp -= account_list.money
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
    record.money = float(request.POST['money'].replace("," , ""))
    record.money_type = request.POST['in_type']
    record.save()
    update_balance(datetime.strptime("01/01/0001", "%d/%m/%Y").date())
    return HttpResponseRedirect(reverse('account:customize'))

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="account_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Detail','Money','Type','Balance'])
    for account_list in Account.objects.order_by('save_date', 'id'):
        writer.writerow([account_list.save_date,
                                        account_list.detail_text,
                                        account_list.money,
                                        account_list.money_type,
                                        account_list.balance])
    return response

def import_page(request):
    return render(request, 'account/import.html')

def import_csv(request):
    data = []
    if(request.POST.get('overwrite')):
        Account.objects.all().delete()
    
    if request.method == 'POST':
        try:
            if(str(request.FILES['file']).endswith('.csv')):
                filename = str(request.FILES['file'])
                handle_uploaded_file(request.FILES['file'], filename)
                csvfile = open('upload/' + filename,'r')
                readCSV = csv.DictReader(csvfile)
            else:
                raise
        except:
            return render(request, 'account/import.html',{'error_message':'Please Select CSV file!!!'})
        
        if(len(readCSV.fieldnames) > 5):
            return render(request, 'account/import.html',{'notsupport_message':'error'})
        
        head = readCSV.fieldnames
        all_head = check_headCSV(head)
        if("" in all_head):
            return render(request, 'account/import.html',{'notsupport_message':'error'})
        
        for row in readCSV:
            row_data = []
            if(check_repeat(data,row)):
                continue
            row_data.append(row[all_head[0]])
            row_data.append(row[all_head[1]])
            row_data.append(row[all_head[2]])
            row_data.append(row[all_head[3]])
            data.append(row_data)
            
        for d in data:
            try:
                last_balance = Account.objects.order_by('-save_date', '-id')[0].balance
                last_date = Account.objects.order_by('-save_date')[0].save_date
            except:
                last_balance = 0
                last_date = datetime.strptime("0001-01-01", "%Y-%m-%d").date()
        
            date = datetime.strptime(d[0], "%Y-%m-%d").date()
            if(d[3] == 'income'):
                balance = last_balance+float(d[2])
            else:
                balance = last_balance-float(d[2])
            record = Account(save_date = date,
                                          detail_text = d[1],
                                          money = float(d[2]),
                                          money_type = d[3],
                                          balance = balance)
            record.save()
            
            if(date < last_date):
                update_balance(date)
                
        os.remove('upload/' + filename)
            
    return HttpResponseRedirect(reverse('account:show'))

def handle_uploaded_file(file, filename):
    if not os.path.exists('upload/'):
        os.mkdir('upload/')
 
    with open('upload/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def check_repeat(data,row):
    for d in data:
        if(d[0] == row['Date'] and d[1] == row['Detail'] and \
            d[2] == row['Money'] and d[3] == row['Type']):
            return True
        
    date = datetime.strptime(row['Date'], "%Y-%m-%d").date()
    for account_list in Account.objects.order_by('save_date', 'id'):
        if(account_list.save_date == date and \
            account_list.detail_text == row['Detail'] and \
            account_list.money == float(row['Money']) and \
            account_list.money_type == row['Type'] ):
            return True
    return False

def check_headCSV(head):
    date_head = ""
    detail_head = ""
    money_head = ""
    type_head = ""
    for h in head:
        if (h != "" and h in("date","Date","วัน/เดือน/ปี")):
            date_head = h
        elif (h != "" and h in("detail","Detail","รายการ")):
            detail_head = h
        elif (h != "" and h in("money","Money","จำนวนเงิน")):
            money_head = h
        elif (h != "" and h in("type","Type","ประเภท")):
            type_head = h
    all_head = [date_head,detail_head,money_head,type_head]
    return all_head