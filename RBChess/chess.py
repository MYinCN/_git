# -*- encoding:utf-8 -*-
#from flask import Flask, request
import flask as fl

global cl, board, cnt
app = fl.Flask(__name__)

def chessJudge(board):
    for row in board:
        if sum(row) == 4:
            return 1
        elif sum(row) == -4:
            return -1
    for col in range(4):
        x = sum([board[i][col] for i in range(4)])
        if x == 4:
            return 1
        elif x == -4:
            return -1
    y = sum([board[i][i] for i in range(4)])
    z = sum([board[i][3-i] for i in range(4)])
    if y == 4 or z == 4:
        return 1
    elif y == -4 or z == -4:
        return -1
    return 0

@app.route('/',methods=['GET', 'POST'])
def homepage():
    global cl, board, cnt
    cl = ['FFFFFF' for _ in range(16)]
    cl[0] = ['000000']
    cl[15] = ['000000']
    board = [[0,0,0,0] for _ in range(4)]
    cnt = 0
    return fl.render_template('homepage.html',c00=cl[0],c01=cl[1],c02=cl[2],c03=cl[3], \
                                              c10=cl[4],c11=cl[5],c12=cl[6],c13=cl[7], \
                                              c20=cl[8],c21=cl[9],c22=cl[10],c23=cl[11], \
                                              c30=cl[12],c31=cl[13],c32=cl[14],c33=cl[15],\
                                              info='目前轮到红方下棋', cside='FF0000',rsum=0, gsum=0)

@app.route('/newMove',methods=['GET', 'POST'])
def newMove():
    global cl, board, cnt
    dirs = [[-2,0],[-2,-2],[0,-2],[2,-2],[2,0],[2,2],[0,2],[-2,2]]
    mov = fl.request.form['chessLoc']
    chs = ['FF0000','FF0000','009100','009100']
    x, y = int(mov[0]), int(mov[1])
    s = '红' if cnt in [2, 3] else '绿'
    info = '目前轮到{}方下棋'.format(s)
    cs = 'FF0000' if cnt in [2, 3] else '009100'
    if board[x][y] == 0:
        cnt = 0 if cnt == 3 else cnt + 1
        cl[x*4 + y] = chs[cnt]
        board[x][y] = 1 if cnt < 2 else -1
        for d in dirs:
            if (x + d[0] in [0,1,2,3]) and (y + d[1] in [0,1,2,3]):
                if board[x][y] == board[x+d[0]][y+d[1]]:
                    mx, my = x + d[0]//2, y + d[1]//2
                    if board[x][y] != board[mx][my] and board[mx][my] != 0:
                        # board[mx][my] = 3 - board[x][y]
                        # cl[mx*4 + my] = 'FF0000' if cl[mx*4 + my] == '009100' else '009100'
                        board[mx][my] = 0
                        cl[mx * 4 + my] = 'FFFFFF'

    else:
        pass
    rsum = sum(map(lambda x: sum([1 for i in x if i == 1]), board))
    gsum = sum(map(lambda x: sum([1 for i in x if i == -1]), board))
    res = chessJudge(board)
    if res == 0:
        if rsum + gsum == 14:
            info = '双方势均力敌，不分高下！'
            cs = '000000'
            return fl.render_template('gamefinish.html', c00=cl[0], c01=cl[1], c02=cl[2], c03=cl[3], \
                              c10=cl[4], c11=cl[5], c12=cl[6], c13=cl[7], \
                              c20=cl[8], c21=cl[9], c22=cl[10], c23=cl[11], \
                              c30=cl[12], c31=cl[13], c32=cl[14], c33=cl[15], \
                              info=info, cside=cs, rsum=rsum, gsum=gsum)
        else:
            return fl.render_template('homepage.html', c00=cl[0], c01=cl[1], c02=cl[2], c03=cl[3], \
                                  c10=cl[4], c11=cl[5], c12=cl[6], c13=cl[7], \
                                  c20=cl[8], c21=cl[9], c22=cl[10], c23=cl[11], \
                                  c30=cl[12], c31=cl[13], c32=cl[14], c33=cl[15], \
                                  info=info, cside=cs, rsum=rsum, gsum=gsum)
    elif res == 1 or res == -1:
        info = '红方获得胜利！' if res == 1 else '绿方获得胜利！'
        cs = '000000'
        return fl.render_template('gamefinish.html', c00=cl[0], c01=cl[1], c02=cl[2], c03=cl[3], \
                                  c10=cl[4], c11=cl[5], c12=cl[6], c13=cl[7], \
                                  c20=cl[8], c21=cl[9], c22=cl[10], c23=cl[11], \
                                  c30=cl[12], c31=cl[13], c32=cl[14], c33=cl[15], \
                                  info=info, cside=cs, rsum=rsum, gsum=gsum)

if __name__ == '__main__':
    app.run()
