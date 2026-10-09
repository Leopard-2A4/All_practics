# TODO здесь писать код
import random
def answer(fir_team,sec_team):
    winners = []
    for i in range(20):
        if fir_team[i] > sec_team[i]:
            winners.append(fir_team[i])
        else:
            winners.append(sec_team[i])
    print('Победители тура: ',winners)
first_team = [round(random.uniform(5,11),2)
              for first in range(20)]
second_team = [round(random.uniform(5,11),2)
               for second in range(20)]
print('Первая команда: ',first_team)
print('Вторая команда: ',second_team)
answer(first_team,second_team)