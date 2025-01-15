from tkinter import *
from tkinter.simpledialog import messagebox as sd
import random

#### 함수 구현 ####

def gameStartSingle():
    global playSingle
    playSingle = True
    gameStart()
    aiTurn()

def gameStart():
    global titleLbl, singleBtn, doubleBtn, themeLbl, themeBtn1, themeBtn2
    titleLbl.destroy()
    singleBtn.destroy()
    doubleBtn.destroy()
    themeLbl.destroy()
    themeBtn1.destroy()
    themeBtn2.destroy()

    global btns, turnLbl
    btns = []    #9개의 버튼들이 저장될 리스트
    for i in range(3):
        for j in range(3):   
            btn = Button(window)
            btn['relief'] = 'solid'
            btn['bg'] = bgcolor
            btn['fg'] = fgcolor
            btn['activebackground'] = bgcolor
            btn.place(x=100+100*j,y=100+100*i,width=100,height=100)
            btns.append(btn)
            btn['font'] = ('배달의민족 주아', 40)
            btn['command'] = lambda b = btn: marking(b)
##            btn['anchor'] = 'ws'

    turnLbl = Label(window)
    turnLbl['text'] = "X's turn."
    turnLbl['bg'] = bgcolor
    turnLbl['fg'] = fgcolor
    turnLbl['font'] = ('배달의민족 주아', 30)
    turnLbl.place(x = 150, y=30, width=200, height=40)
    
    global resLbl
    resLbl = Label(window)
    resLbl['text'] = ""
    resLbl['bg'] = bgcolor
    resLbl['fg'] = fgcolor
    resLbl['font'] = ('배달의민족 주아', 50)
    resLbl['highlightthickness'] = 5
    resLbl['highlightbackground'] = 'black'

def gameFinish():
    global resLbl
    resLbl = Label(window)
    resLbl['text'] = "Winner is X!!"
    resLbl['bg'] = "#A0A0FF"
    resLbl['font'] = ('배달의민족 주아', 50)
    resLbl.place(x = 00, y=175, width=500, height=150)

def titleScene():
    global titleLbl, singleBtn, doubleBtn, themeLbl, themeBtn1, themeBtn2
    titleLbl = Label(window)
    titleLbl['text'] = 'TIC TAC TOE'
    titleLbl['bg'] = bgcolor
    titleLbl['fg'] = fgcolor
    titleLbl['font'] = ('배달의민족 주아', 50)
    titleLbl.place(x = 50, y= 50, width=400, height=100)

    singleBtn = Button(window)
    singleBtn['text'] = '1 Player'
    singleBtn['bg'] = bgcolor
    singleBtn['fg'] = fgcolor
    singleBtn['font'] = ('배달의민족 주아', 20)
##    singleBtn['state'] = DISABLED
    singleBtn.place(x = 150, y= 200, width=200, height=100)
    singleBtn['command'] = gameStartSingle

    doubleBtn = Button(window)
    doubleBtn['text'] = '2 Players'
    doubleBtn['bg'] = bgcolor
    doubleBtn['fg'] = fgcolor
    doubleBtn['font'] = ('배달의민족 주아', 20)
    doubleBtn.place(x = 150, y= 350, width=200, height=100)
    doubleBtn['command'] = gameStart

    themeLbl = Label(window)
    themeLbl['text'] = 'Theme'
    themeLbl['bg'] = bgcolor
    themeLbl['fg'] = fgcolor
    themeLbl.place(x=10,y=430, width=60, height=20)

    themeBtn1 = Button(window)
    themeBtn1['text'] = 'light'
    themeBtn1['bg'] = 'white'
    themeBtn1['fg'] = 'black'
    themeBtn1.place(x=10,y=450, width=60, height=20)
    themeBtn1['command'] = lambda: themeChange('light')

    themeBtn2 = Button(window)
    themeBtn2['text'] = 'dark'
    themeBtn2['bg'] = '#404040'
    themeBtn2['fg'] = '#FBFBF6'
    themeBtn2.place(x=10,y=470, width=60, height=20)
    themeBtn2['command'] = lambda: themeChange('dark')

def themeChange(select):
    global titleLbl, singleBtn, doubleBtn, themeLbl, themeBtn1, themeBtn2
    global theme, bgcolor, fgcolor

    theme = select

    if theme == 'light':
        bgcolor = 'white'
        fgcolor = 'black'
    else:
        bgcolor = '#404040'
        fgcolor = '#FBFBF6'

    window['bg'] = bgcolor
    titleLbl['bg'] = bgcolor
    titleLbl['fg'] = fgcolor
    singleBtn['bg'] = bgcolor
    singleBtn['fg'] = fgcolor
    doubleBtn['bg'] = bgcolor
    doubleBtn['fg'] = fgcolor
    themeLbl['bg'] = bgcolor
    themeLbl['fg'] = fgcolor


def marking(btn):
    global turn, gameover

    if gameover:
        return

    if btn['text'] != '':
        return
    
    if turn == 'X':
        btn['text'] = 'X'
        turn = 'O'
    else:
        btn['text'] = 'O'
        turn = 'X'
    
    turnLbl['text'] = turn+"'s turn."

    result = checkOver()
    #X의 승리: 'X', O의 승리: 'O', 무승부: '=', 끝나지 않음: '+'
##    result = '+'

    #print대신 Label 사용하여 승부결과 표기
    if result == 'X':
        resLbl['text'] = 'X is winner!!'
        resLbl.place(x = 50, y=150, width=400, height=200)
        gameover = True
        window.after(3000, notify)
    elif result == 'O':
        resLbl['text'] = 'O is winner!!'
        resLbl.place(x = 50, y=150, width=400, height=200)
        gameover = True
        window.after(3000, notify)
    elif result == '=':
        resLbl['text'] = 'Draw!!'
        resLbl.place(x = 50, y=150, width=400, height=200)
        gameover = True
        window.after(3000, notify)


def checkOver():  #누가 이겼는지 검사하는 기능
    for win in 'XO':
        for i in range(3):
            #가로 세 줄 검사
            if btns[i*3]['text'] == btns[i*3+1]['text'] == btns[i*3+2]['text'] == win:
                return win
            #세로 세 줄 검사
            if btns[i]['text'] == btns[i+3]['text'] == btns[i+6]['text'] == win:
                return win
        #대각선 검사
        if btns[0]['text'] == btns[4]['text'] == btns[8]['text'] == win:
            return win
        #대각선 검사
        if btns[2]['text'] == btns[4]['text'] == btns[6]['text'] == win:
            return win
    #아직 남은 칸 있는지 검사
    for i in range(9):
        if btns[i]['text'] == '':
            return '+'
    #남은 칸 없으면 무승
    return '='


def notify():
    select = sd.askyesno('Game Over !', 'Do you want to play again?')
    if select == False:
        window.destroy()
    else:
        global btns, turnLbl, resLbl, turn, gameover
        for i in range(9):
            btns[i].destroy()
        turnLbl.destroy()
        resLbl.destroy()
        turn = 'X'
        gameover = False
        titleScene()


def aiTurn():
    global playSingle, turn, gameover
    if not playSingle:
        return

    if gameover:
        playSingle = False
        return

    if turn == 'O':
        #규칙1의 케이스
        if btns[4]['text'] == '':
            marking(btns[4])
        #규칙2의 케이스
        #가로 세 줄 검사
        elif sorted([btns[0]['text'], btns[1]['text'], btns[2]['text']]) == ['','O','O']:
            for i in range(3):
                if btns[i]['text'] == '':
                    marking(btns[i])
                    break
        elif sorted([btns[3]['text'], btns[4]['text'], btns[5]['text']]) == ['','O','O']:
            for i in range(3,6):
                if btns[i]['text'] == '':
                    marking(btns[i])
                    break
        elif sorted([btns[6]['text'], btns[7]['text'], btns[8]['text']]) == ['','O','O']:
            for i in range(6,9):
                if btns[i]['text'] == '':
                    marking(btns[i])
                    break
        #세로 세 줄 검사
        elif sorted([btns[0]['text'], btns[3]['text'], btns[6]['text']]) == ['','O','O']:
            for i in range(0,9,3):
                if btns[i]['text'] == '':
                    marking(btns[i])
                    break
        elif sorted([btns[1]['text'], btns[4]['text'], btns[7]['text']]) == ['','O','O']:
            for i in range(1,9,3):
                if btns[i]['text'] == '':
                    marking(btns[i])
                    break
        elif sorted([btns[2]['text'], btns[5]['text'], btns[8]['text']]) == ['','O','O']:
            for i in range(2,9,3):
                if btns[i]['text'] == '':
                    marking(btns[i])
                    break
        #대각선 검사
        elif sorted([btns[0]['text'], btns[4]['text'], btns[8]['text']]) == ['','X','X']:
            for i in range(0,9,4):
                if btns[i]['text'] == '':
                    marking(btns[i])
                    break
        elif sorted([btns[2]['text'], btns[4]['text'], btns[6]['text']]) == ['','X','X']:
            for i in range(2,7,2):
                if btns[i]['text'] == '':
                    marking(btns[i])
                    break      
        #규칙3의 케이스
        #가로 세 줄 검사
        elif sorted([btns[0]['text'], btns[1]['text'], btns[2]['text']]) == ['','X','X']:
            for i in range(3):
                if btns[i]['text'] == '':
                    marking(btns[i])
                    break
        elif sorted([btns[3]['text'], btns[4]['text'], btns[5]['text']]) == ['','X','X']:
            for i in range(3,6):
                if btns[i]['text'] == '':
                    marking(btns[i])
                    break
        elif sorted([btns[6]['text'], btns[7]['text'], btns[8]['text']]) == ['','X','X']:
            for i in range(6,9):
                if btns[i]['text'] == '':
                    marking(btns[i])
                    break
        #세로 세 줄 검사
        elif sorted([btns[0]['text'], btns[3]['text'], btns[6]['text']]) == ['','X','X']:
            for i in range(0,9,3):
                if btns[i]['text'] == '':
                    marking(btns[i])
                    break
        elif sorted([btns[1]['text'], btns[4]['text'], btns[7]['text']]) == ['','X','X']:
            for i in range(1,9,3):
                if btns[i]['text'] == '':
                    marking(btns[i])
                    break
        elif sorted([btns[2]['text'], btns[5]['text'], btns[8]['text']]) == ['','X','X']:
            for i in range(2,9,3):
                if btns[i]['text'] == '':
                    marking(btns[i])
                    break
        #대각선 검사
        elif sorted([btns[0]['text'], btns[4]['text'], btns[8]['text']]) == ['','X','X']:
            for i in range(0,9,4):
                if btns[i]['text'] == '':
                    marking(btns[i])
                    break
        elif sorted([btns[2]['text'], btns[4]['text'], btns[6]['text']]) == ['','X','X']:
            for i in range(2,7,2):
                if btns[i]['text'] == '':
                    marking(btns[i])
                    break           
        else:
            marking(random.choice(btns))

    window.after(200, aiTurn)
        


#### 데이터 및 변수 구현 ####

theme = 'light'
bgcolor = 'white'
fgcolor = 'black'

turn = 'X'

gameover = False

playSingle = False


#### GUI 구현 ####
window = Tk()
window.title('Tic Tac Toe Game')
window.geometry('500x500')
window['bg'] = 'white'



#sd.askyesno('Game Over !', 'Do you want to play again?')

#### 실행 코드 ####
titleScene()

window.mainloop()



