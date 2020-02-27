from datetime import date, timedelta

'''
현재날짜로부터 예정월급일까지 남은 일수를 계산
지급일이 주말이면, 다음평일로 계산

지급일이 주말이면서 다음평일이 익월일 경우의 예외반영
오늘이 12월일경우 예외 반영

디버깅시 반복문돌리다가
예정월급일이 매 월말일경우(28,29,30,31), 에러날 수도 있음
'''

def count(payday):
    target = date(date.today().year, date.today().month, payday)

    while target.weekday() in [5,6]:    #주말보정
        target = target + timedelta(days=1)

    if date.today() > target:   #다음달급여일
        try:
            target = date(date.today().year, date.today().month+1, payday)
        except ValueError:
            target = date(date.today().year+1, 1, payday)   #12월예외

        while target.weekday() in [5,6]:
            target = target + timedelta(days=1)
    return int((target-date.today())/timedelta(days=1)) #timedelta자료형을 일단위 정수형으로보정

if __name__ == '__main__':
    for i in range(1, 29):
        print(f'예정일: {i}, 남은일수: {count(i)}')
