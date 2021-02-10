import pandas as pd
import numpy as np
import jdatetime
import orders as do
initial_info = pd.read_excel('data1.xlsx')
saved = pd.read_excel('data3.xlsx')
del saved['Unnamed: 0']
for i in range(len(saved.index[:])):   # using a for loop to convert date of each row to jdatetime object
    date = list(map(lambda x: int(x), saved.loc[i, 'Time'].split('-')))
    saved.loc[i, 'Time'] = jdatetime.date(date[0], date[1], date[2])
saved = saved.sort_values(by='Time').reset_index()
del saved['index']
main_info = pd.read_excel('data2.xlsx')
del main_info['Unnamed: 0']
for i in range(len(main_info.index[:])):  # using a for loop to convert date of each row to jdatetime object
    date = list(map(lambda x: int(x), main_info.loc[i, 'Time'].split('-')))
    main_info.loc[i, 'Time'] = jdatetime.date(date[0], date[1], date[2])
main_info = main_info.sort_values(by='Time').reset_index()
del main_info['index']
while True:
    ord = input('please type your order!')  # getting input for order of user
    try:
        if ord == 'exit':
            break
        elif ord == 'append':   # getting data from user
            a = ['enter date (you can put now!)', 'Category?', 'SubCategory?(type none if there isnt any!)', 'Total Amount?',
                 'please type the units that are related with space!(like : id1 id2 id3)']
            newrow = {'id': len(main_info.index[:])}
            for i in range(1, len(main_info.columns[:])):
                b = input(a[i-1])
                newrow[main_info.columns[i]] = b
                if a[i-1] == 'enter date (you can put now!)':
                    if b == 'now':
                        newrow[main_info.columns[i]] = jdatetime.date.today()
                    else:
                        b = list(map(lambda x: int(x), b.split('-')))
                        newrow[main_info.columns[i]] = jdatetime.date(*b)
                if b == 'none':
                    newrow[main_info.columns[i]] = np.nan
                if i == len(main_info.columns[:])-1:
                    newrow[main_info.columns[i]] = b.split()
                if a[i-1] == 'Total Amount?':
                    newrow[main_info.columns[i]] = int(b)
            div = input('kind of div?(--d , --a , --p , --r , --e)')
            main_info = main_info.append(newrow, ignore_index=True)  # adding new row to main info
            newrow['Amount'] = do.DIV(newrow, div, initial_info)
            newrow['Unit'] = newrow['Units']
            del newrow['Units']
            saved = saved.append(pd.DataFrame(newrow).explode('Unit'), ignore_index=True)  # adding new rows to saved
            main_info = main_info.sort_values(by='Time').reset_index()
            del main_info['index']
            saved = saved.sort_values(by='Time').reset_index()
            del saved['index']
            m1 = main_info.sort_values(by='id').reset_index()  # sorting main_info by id for saving it in data2
            del m1['index']
            s1 = saved.sort_values(by='id').reset_index()  # sorting saved by id for saving it in data3
            del s1['index']
            # saving new rows to data2 and data3
            m1.to_excel('data2.xlsx', index=True)
            s1.to_excel('data3.xlsx', index=True)
        elif ord.split()[0] == 'plot':
            ord = ord.split()
            if ord[1] == 'units':
                ord = ord[1:]
                do.plot(ord, saved)
            else:
                do.plot(ord, main_info)
        elif ord.split()[0] == 'bill':
            ord = ord.split()
            do.Bills(ord[1], ord[2], saved)
        elif ord.split()[0] == 'report':
            do.report(main_info)
        elif ord.split()[0] == 'balancesheet':
            do.balancesheet(ord.split()[1], ord.split()[2], saved)
        elif ord.split()[0] == 'constantprices':
            do.constantprices(ord.split()[1], ord.split()[2], saved)
        else:   # error if the order that was typed wasn't defined
            print('Please type your order in the right format!')
    except:  # error if the elements that user typed wasn't in right format
        print('Oops... ! Please type your order in the right format!')
