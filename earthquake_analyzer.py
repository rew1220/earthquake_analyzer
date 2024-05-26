import matplotlib.pyplot as plt
import numpy as np
import matplotlib
#한글폰트설정
matplotlib.rc('font', family='NanumGothic')

#결측치 여부 판단하는 함수
def MissingFinder(inputdata, type):
    global IsDataMissing
    global Mdatatype
    if(inputdata == 0): #결측치라면
        if(IsDataMissing): return True #결측치가 이미 존재한다면
        Mdatatype = type 
        IsDataMissing = True
    return False

#결측치 계산
def Finder(type, D_data):
    #거리/속력 = 시간
    if(type == 'Tp'):
        return D_data['L']/D_data['Vp']
    elif(type == 'Ts'):
        return D_data['L']/D_data['Vs']
    #거리/시간 = 속력
    elif(type == 'Vp'):
        return D_data['L']/D_data['Tp']
    elif(type == 'Vs'):
        return D_data['L']/D_data['Ts']
    #거리공식 사용
    elif(type == 'L'):
        return (D_data['Ts']-D_data['Tp'])*D_data['Vs']*D_data['Vp']/(D_data['Vp']-D_data['Vs'])

while(True):
    #변수정의
    global IsDataMissing
    global Mdatatype
    IsDataMissing = False #결측치 존재 여부
    Mdatatype = "" #결측치가 무엇인가?
    #데이터를 담을 딕셔너리
    Data_dict = {'Ts':0.0,'Tp':0.0,'Vs':0.0,'Vp':0.0,'L':0.0} 
    Tps = 0.0 #ps시 (Ts-Tp)
    print("==========================")
    print("실수 데이터를 입력해주세요(최대 1개의 결측치 허용)\n(데이터 입력이 0일때 결측치로 판단)")
    #input 구역
    try:
        Data_dict['Tp'] = float(input("P파 도달시간 입력 : "))
        if(MissingFinder(Data_dict['Tp'], 'Tp')):
            print("둘 이상의 데이터가 결측치입니다!")
            continue

        Data_dict['Ts'] = float(input("S파 도달시간 입력 : "))
        if(MissingFinder(Data_dict['Ts'], "Ts")):
            print("둘 이상의 데이터가 결측치입니다!")
            continue
        
        Data_dict['Vp'] = float(input("P파 속력 입력 : "))
        if(MissingFinder(Data_dict['Vp'], "Vp")):
            print("둘 이상의 데이터가 결측치입니다!")
            continue

        Data_dict['Vs'] = float(input("S파 속력 입력 : "))
        if(MissingFinder(Data_dict['Vs'], "Vs")):
            print("둘 이상의 데이터가 결측치입니다!")
            continue

        Data_dict['L'] = float(input("진원과의 거리 입력 : "))
        if(MissingFinder(Data_dict['L'], "L")):
            print("둘 이상의 데이터가 결측치입니다!")
            continue

    except Exception as e: #오류 발생시 실행
        print("올바른 입력값이 아닙니다!")
        print(e)
        continue

    #output 구역
    print("===========결과===========")
    if(IsDataMissing): Data_dict[Mdatatype] = Finder(Mdatatype, Data_dict)
    Tps = Data_dict['Ts']-Data_dict['Tp']
    print("P파 정보")
    print(f'P파 속력 : {Data_dict["Vp"]}km/s')
    print(f'P파 도달시간 : {Data_dict["Tp"]}s')
    print("S파 정보")
    print(f'S파 속력 : {Data_dict["Vs"]}km/s')
    print(f'S파 도달시간 : {Data_dict["Ts"]}s')
    print('그 외 정보')
    print(f"ps시 : {Tps}s")
    print(f"관측소에서 진원까지의 거리 : {Data_dict['L']}km")
    
    #이상치 표기
    if(not 5<=Data_dict['Vp']<=8):print("이상치 : P파의 속력이 일반적이지 않습니다.")
    if(3<=Data_dict['Vs']<=4):print("이상치 : S파의 속력이 일반적이지 않습니다.")
    if(Data_dict['Vp'] < Data_dict['Vs']):print("이상치 : S파의 속력이 더 빠릅니다.")
    if(Data_dict['Tp'] > Data_dict['Ts']):print("이상치 : S파가 먼저 도달했습니다.")
    if(Data_dict['L']<=0):print("이상치 : 진원과의 거리가 음수거나 0입니다.")
    
    #그래프 구역
    plt.title("지진 이동 그래프")
    plt.xlabel("이동시간(s)")
    plt.ylabel("진앙거리(km)")
    x = np.linspace(0,80,81)
    y = Data_dict['Vp']*x
    plt.plot(x,y,label = "p 파", color = "green")
    x = np.linspace(0,80,81)
    y = Data_dict['Vs']*x
    plt.plot(x,y,label = "s 파", color = "blue")
    plt.legend(loc = 'upper left')
    plt.show()

