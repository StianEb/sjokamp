###
# Battleships clone, requires ezgraphics
# Improvement 1
# Improvement 2
#

from ezgraphics import GraphicsWindow
from random import randint, choice
from time import sleep
import sys


def checkIfFree(field,ship_length,x,y,vertical):
    """Sjekker om det er plass til å putte et skip et bestemt sted på et brett (field)."""

    if vertical:
        #Sjekk om det er plass til hele skipet på brettet
        if y + ship_length > 7:
            return False
        #Sjekk om det er tomt i alle ruter og naboruter der skipet skal plasseres
        for i in range(ship_length+2):
            if not(field[x][inBoard(y+i-1)] == field[inBoard(x-1)][inBoard(y+i-1)] == field[inBoard(x+1)][inBoard(y+i-1)] == 0):
                return False
    
    #Tilsvarende for horisontal plassering av skip
    else:
        if x + ship_length > 7:
            return False
        for i in range(ship_length+2):
            if not(field[inBoard(x+i-1)][y] == field[inBoard(x+i-1)][inBoard(y-1)] == field[inBoard(x+i-1)][inBoard(y+1)] == 0):
                return False
    return True

def compTurn(spillerbrett,dataskudd):
    """Utfører datamaskinens tur ved å velge et sted å skyte, og deretter oppdatere listen over skudd."""
    
    x, y = recommendMove(spillerbrett,dataskudd)
    dataskudd[x][y] = 1
    return dataskudd, (x, y)

def computeHypotenuse(x1,y1,x2,y2):
    """Regner ut avstanden mellom to punkter i et 2D-plan"""
    
    return ((x2-x1)**2 + (y2-y1)**2) ** 0.5

def drawBoard(canvas,board,alignment,shots):
    """Tegner innholdet av ett enkelt brett, enten datamaskinens eller spillerens"""

    #Finn ut hvilke variabler brettet skal tegnes med (plassering og farger)
    if alignment == "computer":
        xOffset = X_POSITION_COMPUTER_BOARD
        yOffset = Y_POSITION_COMPUTER_BOARD
        squareOutline = "darkseagreen4"
        squareFill = "darkseagreen"
    else:
        xOffset = X_POSITION_HUMAN_BOARD
        yOffset = Y_POSITION_HUMAN_BOARD
        squareOutline = "blue"
        squareFill = "slategray3"

    #Tegn hver enkelt rute i brettet.
    for x in range(len(board)):
        for y in range(len(board)):
            canvas.setFill(squareFill)
            canvas.setOutline(squareOutline)
            canvas.setLineWidth(1)
            drawSquare(canvas,board,alignment,xOffset,yOffset,x,y,shots) 

def drawLogo(canvas,xPos,yPos):
    """Tegner logoen for spillet ved de gitte koordinatene"""
    
    canvas.setLineWidth(10)
    #bakgrunns-oval
    canvas.setColor("grey80")
    canvas.drawOval(xPos,yPos,900,200)
    #S
    canvas.setColor("red3")
    canvas.drawLine(xPos+88,yPos+27,xPos+130,yPos+70)
    canvas.drawLine(xPos+16,yPos+81,xPos+108,yPos+28)
    canvas.drawLine(xPos+14,yPos+70,xPos+127,yPos+119)
    canvas.drawLine(xPos+119,yPos+106,xPos+79,yPos+170)
    canvas.drawLine(xPos+9,yPos+124,xPos+98,yPos+164)
    #J
    xPos += 125
    canvas.drawLine(xPos+24,yPos+22,xPos+135,yPos+30)
    canvas.drawLine(xPos+80,yPos+23,xPos+101,yPos+149)
    canvas.drawLine(xPos+116,yPos+141,xPos+20,yPos+113)
    #Ø
    xPos += 120
    canvas.drawLine(xPos+52,yPos+36,xPos+134,yPos+63)
    canvas.drawLine(xPos+122,yPos+50,xPos+133,yPos+148)
    canvas.drawLine(xPos+144,yPos+131,xPos+65,yPos+164)
    canvas.drawLine(xPos+86,yPos+168,xPos+18,yPos+109)
    canvas.drawLine(xPos+21,yPos+125,xPos+69,yPos+29)
    canvas.drawLine(xPos+17,yPos+155,xPos+154,yPos+63)
    #K
    xPos += 155
    canvas.drawLine(xPos+30,yPos+23,xPos+41,yPos+160)
    canvas.drawLine(xPos+24,yPos+110,xPos+116,yPos+44)
    canvas.drawLine(xPos+45,yPos+78,xPos+116,yPos+148)
    #A
    xPos += 102
    canvas.drawLine(xPos+35,yPos+173,xPos+78,yPos+41)
    canvas.drawLine(xPos+62,yPos+39,xPos+140,yPos+185)
    canvas.drawLine(xPos+40,yPos+117,xPos+118,yPos+111)
    #M
    xPos += 113
    canvas.drawLine(xPos+32,yPos+18,xPos+37,yPos+156)
    canvas.drawLine(xPos+20,yPos+24,xPos+107,yPos+84)
    canvas.drawLine(xPos+89,yPos+85,xPos+162,yPos+28)
    canvas.drawLine(xPos+148,yPos+23,xPos+152,yPos+154)
    #P
    xPos += 150
    canvas.drawLine(xPos+41,yPos+40,xPos+46,yPos+180)
    canvas.drawLine(xPos+29,yPos+51,xPos+103,yPos+55)
    canvas.drawLine(xPos+86,yPos+43,xPos+119,yPos+106)
    canvas.drawLine(xPos+33,yPos+122,xPos+124,yPos+91)

def drawPregame(canvas,board):
    """Tegner skjermbildet i før-spillet, hvor spilleren velger spillebrett"""
    
    #Definer variabler som trengs for å tegne brettet
    shots = [[0 for x in range(8)] for y in range(8)]
    xOffset = 250
    yOffset = 300

    #Sett bakgrunn, tegn logo og undertekst
    canvas.setBackground("grey60")
    drawLogo(canvas,50,20)

    canvas.setColor("red3")
    canvas.setTextFont("courier","normal",14)
    canvas.drawText(350, 240, "- Velg ditt spillebrett -")

    #Tegn en avslutt-knapp oppe til høyre
    canvas.setLineWidth(2)
    canvas.setColor("red")
    canvas.drawOval(SCREEN_WIDTH-25,5,20,20)
    canvas.setColor("white")
    canvas.setLineWidth(4)
    canvas.drawLine(SCREEN_WIDTH-20,20,SCREEN_WIDTH-10,10)
    canvas.drawLine(SCREEN_WIDTH-20,10,SCREEN_WIDTH-10,20)

    #Tegn brettet. Dette er en litt uelegant copypaste fra drawBoard, som kunne vært designet mer dynamisk.
    for x in range(len(board)):
        for y in range(len(board)):
            canvas.setFill("lightblue")
            canvas.setOutline("blue")
            canvas.setLineWidth(1)
            drawSquare(canvas,board,"player",xOffset,yOffset,x,y,shots)

    #Tegn knappene
    canvas.setFill("grey80")
    canvas.setOutline("grey40")
    canvas.drawRectangle(xOffset+BOARD_SQUARE_SIZE*10,yOffset+50,160,20)
    canvas.drawRectangle(xOffset+BOARD_SQUARE_SIZE*10,yOffset+150,100,20)
    canvas.setColor("red3")
    canvas.setTextFont("arial","italic",12)
    canvas.drawText(xOffset+BOARD_SQUARE_SIZE*10+10,yOffset+51,"Gi meg et nytt brett")
    canvas.drawText(xOffset+BOARD_SQUARE_SIZE*10+10,yOffset+151,"Start spillet!")

def drawScreen(canvas,compboard,humanboard,playershots,compshots,turn,shotMessage=""):
    """Tegner alt på skjermen når spillet pågår"""

    canvas.clear()

    #Tegn bakgrunnen for motstanderens brett
    canvas.setColor("lightgreen")
    canvas.drawPoly((0,0),(0,SCREEN_HEIGHT),(SCREEN_WIDTH//7*3,SCREEN_HEIGHT),(SCREEN_WIDTH//7*4,0))

    #Tegn logoen
    drawLogo(canvas,50,20)

    #Tegn bakgrunn for tur-indikatortekst
    canvas.setLineWidth(2)
    canvas.setOutline("black")
    canvas.setFill("grey80")
    canvas.drawRectangle(SCREEN_WIDTH//2-210,max(Y_POSITION_HUMAN_BOARD,Y_POSITION_COMPUTER_BOARD)+BOARD_SQUARE_SIZE*9-7,430,35)

    #Tegn turindikatortekst og kommentar til forrige trekk
    canvas.setColor("black")
    if turn == "spillerTur":
        canvas.setTextFont("courier","normal",12)
        canvas.drawText(SCREEN_WIDTH//2-200,max(Y_POSITION_HUMAN_BOARD,Y_POSITION_COMPUTER_BOARD)+BOARD_SQUARE_SIZE*9,"Din tur! Klikk på en rute for å angripe.")
        canvas.setColor("red")
        canvas.drawText(X_POSITION_HUMAN_BOARD+5,Y_POSITION_HUMAN_BOARD-25,shotMessage)
    elif turn == "dataTur":
        canvas.setTextFont("courier","normal",12)
        canvas.drawText(SCREEN_WIDTH//2-200,max(Y_POSITION_HUMAN_BOARD,Y_POSITION_COMPUTER_BOARD)+BOARD_SQUARE_SIZE*9,"Motstanderens tur. Klikk for å fortsette.")
        canvas.setColor("red")
        canvas.drawText(X_POSITION_COMPUTER_BOARD+5,Y_POSITION_COMPUTER_BOARD-25,shotMessage)

    #Tegn en avslutt-knapp oppe til høyre
    canvas.setColor("red")
    canvas.drawOval(SCREEN_WIDTH-25,5,20,20)
    canvas.setColor("white")
    canvas.setLineWidth(4)
    canvas.drawLine(SCREEN_WIDTH-20,20,SCREEN_WIDTH-10,10)
    canvas.drawLine(SCREEN_WIDTH-20,10,SCREEN_WIDTH-10,20)

    #Tegn de to brettene
    drawBoard(canvas,compboard,"computer",playershots)
    drawBoard(canvas,humanboard,"player",compshots)

def drawShipSegment(canvas,piece,xPos,yPos):
    """Tegner ett segment (en rute) av et skip.
    Oversetter tekstkoden på brettet til geometriske figurer, og tegner dem."""
    
    direction = piece[2]
    piece = piece[:2]
    if piece == "P1": #Pram, det eneste 'skipet' som bare er èn rute langt
        canvas.drawOval(xPos+5,yPos+5,BOARD_SQUARE_SIZE-10,BOARD_SQUARE_SIZE-10)
    elif direction == "v":
        if piece in ("B2","B3","B4","L2","L3","J2","K2"):
            canvas.drawRectangle(xPos+5,yPos,BOARD_SQUARE_SIZE-10,BOARD_SQUARE_SIZE)
        elif piece in ("B1","L1","J1","K1","S1"):
            canvas.drawRectangle(xPos+5,yPos+BOARD_SQUARE_SIZE/2,BOARD_SQUARE_SIZE-10,BOARD_SQUARE_SIZE/2) # er det et problem at det kan bli en float her hvis square size er oddetall?
            canvas.drawArc(xPos+5,yPos+5,BOARD_SQUARE_SIZE-10,0,180)
        elif piece in ("B5","L4","J3","K3","S2"):
            canvas.drawRectangle(xPos+5,yPos,BOARD_SQUARE_SIZE-10,BOARD_SQUARE_SIZE/2) # float
            canvas.drawArc(xPos+5,yPos+5,BOARD_SQUARE_SIZE-10,180,180)
    else:
        if piece in ("B2","B3","B4","L2","L3","J2","K2"):
            canvas.drawRectangle(xPos,yPos+5,BOARD_SQUARE_SIZE,BOARD_SQUARE_SIZE-10)
        elif piece in ("B1","L1","J1","K1","S1"):
            canvas.drawRectangle(xPos+BOARD_SQUARE_SIZE/2,yPos+5,BOARD_SQUARE_SIZE/2,BOARD_SQUARE_SIZE-10) # float
            canvas.drawArc(xPos+5,yPos+5,BOARD_SQUARE_SIZE-10,90,180)
        elif piece in ("B5","L4","J3","K3","S2"):
            canvas.drawRectangle(xPos,yPos+5,BOARD_SQUARE_SIZE/2,BOARD_SQUARE_SIZE-10) # float
            canvas.drawArc(xPos+5,yPos+5,BOARD_SQUARE_SIZE-10,270,180)  

def drawSquare(canvas,board,alignment,xOffset,yOffset,x,y,shots):
    """Tegner innholdet av en enkelt rute av enten datamaskinens eller spillerens brett"""
    
    xPos = xOffset + x*BOARD_SQUARE_SIZE
    yPos = yOffset + y*BOARD_SQUARE_SIZE

    #Tegn selve ruta uansett
    canvas.drawRectangle(xPos + 1, yPos + 1, BOARD_SQUARE_SIZE-2, BOARD_SQUARE_SIZE-2)
    
    if alignment == "computer":
        if board[x][y] != 0 and shots[x][y] != 0:
            #Tegn beskutte (synlige) skipsdeler i denne ruta
            canvas.setColor("black")
            drawShipSegment(canvas,board[x][y],xPos,yPos)
        if shots[x][y] != 0:
            #Tegn et kryss i denne ruta hvis den har blitt beskutt i løpet av spillet
            canvas.setColor("red")
            canvas.setLineWidth(2)
            canvas.drawLine(xPos + 5, yPos + 5, xPos + BOARD_SQUARE_SIZE-5, yPos + BOARD_SQUARE_SIZE-5)
            canvas.drawLine(xPos + 5, yPos + BOARD_SQUARE_SIZE-5, xPos + BOARD_SQUARE_SIZE-5, yPos + 5)

    #Tilsvarende for spillerens brett
    else:
        if board[x][y] != 0:
            canvas.setColor("grey30")
            drawShipSegment(canvas,board[x][y],xPos,yPos)
        if shots[x][y] != 0:
            canvas.setColor("orangered")
            canvas.setLineWidth(2)
            canvas.drawLine(xPos + 5, yPos + 5, xPos + BOARD_SQUARE_SIZE-5, yPos + BOARD_SQUARE_SIZE-5)
            canvas.drawLine(xPos + 5, yPos + BOARD_SQUARE_SIZE-5, xPos + BOARD_SQUARE_SIZE-5, yPos + 5)

def evaluatePregameClick(win, mouseClick):
    """Sjekker om de oppgitte koordinatene faller innenfor området til en av de to knappene på skjermen"""
    
    mouseX, mouseY = mouseClick
    
    #Plassering av knappene er ikke bundet til brettets plassering
    xOffset = 250
    yOffset = 300

    #Avslutt - knappen
    if computeHypotenuse(mouseX,mouseY,SCREEN_WIDTH-15,15) <= 10:
        win.close()
        sys.exit(0)

    #Nytt brett - knappen
    if xOffset+BOARD_SQUARE_SIZE*10 < mouseX < xOffset+BOARD_SQUARE_SIZE*10+160 and yOffset+50 < mouseY < yOffset+70:
        return (False, True)

    #Start spillet - knappen
    elif xOffset+BOARD_SQUARE_SIZE*10 < mouseX < xOffset+BOARD_SQUARE_SIZE*10+100 and yOffset+150 < mouseY < yOffset+170:
        return (True, False)

    #Hvor som helst ellers på skjermen
    else:
        return (False, False)

def generateMessage(moveTuple, board, isPlayer):
    """Returnerer en beskjed som kan printes til skjermen, en kommentar til trekket moveTuple på brettet board."""
    
    x, y = moveTuple
    if board[x][y] != 0: #Hvis en skipsdel nettopp ble truffet
        shipName = shipsRev[board[x][y][0]] #Henter skipsnavn fra en separat ordbok for å slippe å iterere over listen "ships"
        if isPlayer:
            return "Treff i %s!" % shipName
        else:
            return "Treff i %s! Å nei!" % shipName
    return ""

def inBoard(x):
    """Hindrer IndexError når vi referer til indekser på spillebrettet. Modulo er ikke ønskelig fordi det gir wraparound."""
    
    if x < 0:
        return 0
    if x > 7:
        return 7
    else:
        return x

def initiatePreGame(win,canvas):
    """Viser et skjermbilde som lar spilleren velge brett før spiller starter"""

    #Initialiser spillebrettet
    hjemmebane = [[0 for x in range(8)] for y in range(8)]
    hjemmebane = placeShipsRandomly(hjemmebane)

    #Tegn skjermen og la spilleren velge nye spillebrett til han blir fornøyd
    hjemmebane = runPregame(win,canvas,hjemmebane)
    
    return hjemmebane

def interpretMouseClick(win, mouseX,mouseY):
    """Hvis spilleren klikket på krysset oppe til høyre, avslutt spillet
    Hvis spilleren klikket på motstanderbrettet, returner koordinatene til listeindeksen for ruta de klikket på"""
    
    if computeHypotenuse(mouseX,mouseY,SCREEN_WIDTH-15,15) <= 10:
        win.close()
        sys.exit(0)
    
    if X_POSITION_COMPUTER_BOARD < mouseX < X_POSITION_COMPUTER_BOARD+BOARD_SQUARE_SIZE*8 and Y_POSITION_COMPUTER_BOARD < mouseY < Y_POSITION_COMPUTER_BOARD+BOARD_SQUARE_SIZE*8:
        xClick = (mouseX - X_POSITION_COMPUTER_BOARD) // BOARD_SQUARE_SIZE
        yClick = (mouseY - Y_POSITION_COMPUTER_BOARD) // BOARD_SQUARE_SIZE
        return (xClick,yClick)
    return -1

def isVictorious(shotBoard,boatBoard):
    """Sjekker om alle skipsdelene på det gitte brettet har blitt skutt på"""
    
    for x in range(len(shotBoard)):
        for y in range(len(shotBoard[0])):
            if boatBoard[x][y] != 0 and shotBoard[x][y] == 0:
                return False
    return True

def main():
    """Gangen i spillet"""
    
    #Initialiser vindu og lerret
    win = GraphicsWindow(SCREEN_WIDTH,SCREEN_HEIGHT)
    canvas = win.canvas()

    #La spilleren velge spillebrett på en egen skjerm før spillet
    hjemmebane = initiatePreGame(win,canvas)

    #Spill spillet
    mainGame(hjemmebane,win,canvas)

def mainGame(hjemmebane,win,canvas):
    """Kjører selve spillet. Litt forberedelser, deretter hovedløkka"""
    
    #Opprett brettene (unntatt spillerens brett)
    bortebane = [[0 for x in range(8)] for y in range(8)]
    spillerskudd = [[0 for x in range(8)] for y in range(8)]
    dataskudd = [[0 for x in range(8)] for y in range(8)]
    
    #fyll motstanderens brett med skip
    bortebane = placeShipsRandomly(bortebane)

    #diverse
    canvas.setBackground("lightblue2")
    shotMessage=""

    #hovedløkka for spillet
    while True:
        
        #tegn skjermen
        drawScreen(canvas,bortebane,hjemmebane,spillerskudd,dataskudd,"spillerTur",shotMessage)

        #spillerens tur, vent på gyldig input fra musa og utfør trekk
        playerMove = -1
        while playerMove == -1:
            mouse_x, mouse_y = win.getMouse()
            playerMove = interpretMouseClick(win, mouse_x, mouse_y)
        spillerskudd = makePlayerMove(spillerskudd,playerMove)
        shotMessage = generateMessage(playerMove,bortebane,True)

        #sjekk om spilleren har vunnet
        if isVictorious(spillerskudd,bortebane):
            postGame(win,canvas,True)
        
        #tegn skjermen, vent til spiller klikker med å fortsette
        drawScreen(canvas,bortebane,hjemmebane,spillerskudd,dataskudd,"dataTur",shotMessage)
        win.getMouse()
        
        #datamaskinens tur
        dataskudd,compMove = compTurn(hjemmebane,dataskudd)
        shotMessage = generateMessage(compMove,hjemmebane,False)
        
        #sjekk om spilleren har tapt
        if isVictorious(dataskudd,hjemmebane):
            postGame(win,canvas,False)

def makePlayerMove(spillerskudd,playerMove):
    """Oppdaterer det skjulte brettet som holder styr på spillerens tidligere skudd"""
    
    xShot, yShot = playerMove
    spillerskudd[xShot][yShot] = 1
    return spillerskudd

def placeShip(board,ship,x,y,vertical):
    """Plasserer et skip på et bestemt sted."""
    
    ship_length = len(ships[ship])
    if vertical:
        for i in range(ship_length):
            board[x][y+i] = ships[ship][i]+"v"
    else:
        for i in range(ship_length):
            board[x+i][y] = ships[ship][i]+"h"
    return board

def placeShipsRandomly(board):
    """Plasserer skip fra den globale skipslista på et gitt brett"""
    
    for ship in ships: #ships er en global, konstant ordbok
        ship_length = len(ships[ship])
        free_spot = False 
        attempts = 0
        while not free_spot:
            x = randint(0,7)
            y = randint(0,7)
            vertical = choice([True,False])
            free_spot = checkIfFree(board,ship_length,x,y,vertical)
            attempts += 1
            if attempts > 100: #Safeguard mot tilfeller der det blir umulig å plassere de siste skipene.
                board = [[0 for x in range(8)] for y in range(8)]
                return placeShipsRandomly(board)
        board = placeShip(board,ship,x,y,vertical)
    return board

def postGame(win,canvas,playerWon):
    """Roser eller skjeller ut spilleren, alt ettersom han vant eller tapte"""

    canvas.clear()

    #Sett parametere basert på om spilleren vant eller ikke
    if playerWon:
        canvas.setBackground("darkslategray4")
        messages = ["Du vant!","Hurra!","Tjo-ho!","Du er best!","Jippi!","Alle elsker deg!","Sjette sans for skip?","Hvordan klarte du det?","Et geni uten like!",
                    "Verden er reddet!","Fryd!","Gammen!","Mesterstratèg","Ikke dårlig!","Imponerende!","Gratulerer!","Alle skip er senket!","Fantastisk!",
                    "Ingen over, ingen ved siden", "Nei, nå har jeg aldri","Hipp hipp!","Du seirer!"]
        messageColor = "green"
    else:
        canvas.setBackground("bisque2")
        messages = ["Du tapte!","Bu-hu!","Krigen er tapt!","Det var din feil!","Elendig strategi!","Fysj!","Skam deg!","Slått av en AI?","Gratulerer med ingenting..",
                    "Alt var forgjeves!","Ditt land utviser deg","Gå og legg deg!","Du rykker ned til kadett","En skam for marinen!","En skam for familien din!",
                    "Alle mann er døde","Du er bekjempet","Enden er nær!","Vær trist!","Forferdelig!"]
        messageColor = "red"

    canvas.setColor(messageColor)

    #Ros eller skjell ut spilleren i ca 8 sekunder
    for i in range(40):
        canvas.setTextFont("arial","bold",randint(4,50))
        canvas.drawText(randint(0,SCREEN_WIDTH-50),randint(0,SCREEN_HEIGHT-10),choice(messages))
        sleep(0.2)

    #Avslutt spillet
    win.close()
    sys.exit(0)

def recommendMove(board,shots):
    """Anbefaler et trekk basert på hva som er synlig (beskutt) på brettet, uten å jukse med skjulte verdier.
    Prioriterer å senke delvis senkede skip, gjetter deretter tilfeldig men tar hensyn til at skip ikke kan ligge innat hverandre."""
    
    #Først, se etter eksponerte skipsdeler av skip som ikke er fullstendig senket ennå
    for x in range(len(board)):
        for y in range(len(board[0])):
            if shots[x][y] == 1:
                square = board[x][y]
                if square in ("B2v","B3v","B4v","B5v","L2v","L3v","L4v","J2v","J3v","K2v","K3v","S2v"): #Disse skipsdelene er aldri øverst
                    if shots[x][y-1] == 0:
                        return (x,y-1) #Anbefal å skyte en rute over den eksponerte delen
                    elif shots[x][y+1] == 0 and square not in ("B5v","L4v","J3v","K3v","S2v"): #Midtdeler betyr flere skipsdeler på begge sider.
                        return (x,y+1)
                elif square in ("B1v","L1v","J1v","K1v","S1v") and shots[x][y+1] == 0:
                    return (x,y+1)
                elif square in ("B2h","B3h","B4h","B5h","L2h","L3h","L4h","J2h","J3h","K2h","K3h","S2h"): #(Tilsvarende for horisontalt plasserte skip)
                    if shots[x-1][y] == 0:
                        return (x-1,y)
                    elif shots[x+1][y] == 0 and square not in ("B5h","L4h","J3h","K3h","S2h"):
                        return (x+1,y)
                elif square in ("B1h","L1h","J1h","K1h","S1h") and shots[x+1][y] == 0:
                    return (x+1,y)
                
    #Hvis det ikke er noen delvis senkede skip å se, velg et tilfeldig sted hvor det ikke har blitt skutt før,
    #men ikke en nabo av en beskutt skipsdel (pga logikken bak plassering av skipene).
    squareFree = False
    while not squareFree:
        xGuess = randint(0,7)
        yGuess = randint(0,7)
        #Hvis vi ikke har skutt her før..
        if shots[xGuess][yGuess] == 0:
            #Hvis det ikke ligger noen eksponerte skipsdeler i en av de fire naborutene..
            if shots[inBoard(xGuess-1)][yGuess] == 0 or board[inBoard(xGuess-1)][yGuess] == 0:
                if shots[inBoard(xGuess+1)][yGuess] == 0 or board[inBoard(xGuess+1)][yGuess] == 0:
                    if shots[xGuess][inBoard(yGuess-1)] == 0 or board[xGuess][inBoard(yGuess-1)] == 0:
                        if shots[xGuess][inBoard(yGuess+1)] == 0 or board[xGuess][inBoard(yGuess+1)] == 0:
                            #Og hvis det ikke ligger noen eksponerte skipsdeler i en av de fire hjørnerutene..
                            if shots[inBoard(xGuess-1)][inBoard(yGuess-1)] == 0 or board[inBoard(xGuess-1)][inBoard(yGuess-1)] == 0:
                                if shots[inBoard(xGuess-1)][inBoard(yGuess+1)] == 0 or board[inBoard(xGuess-1)][inBoard(yGuess+1)] == 0:
                                    if shots[inBoard(xGuess+1)][inBoard(yGuess-1)] == 0 or board[inBoard(xGuess+1)][inBoard(yGuess-1)] == 0:
                                        if shots[inBoard(xGuess+1)][inBoard(yGuess+1)] == 0 or board[inBoard(xGuess+1)][inBoard(yGuess+1)] == 0:
                                            squareFree = True
    return (xGuess, yGuess)

def runPregame(win,canvas,hjemmebane):
    """Hovedløkka i skjermen før spillet. Tegner skjermen og lar spilleren velge spillebrett"""

    playerHappy = False
    while not playerHappy:
        
        #Tegn alt som skal være på skjermen
        canvas.clear()
        drawPregame(canvas,hjemmebane)

        #Følg med på om spilleren trykker på en av de to knappene
        mouseClick = win.getMouse()
        playerHappy, rerollNow = evaluatePregameClick(win, mouseClick)
        if rerollNow:
            hjemmebane = [[0 for x in range(8)] for y in range(8)]
            hjemmebane = placeShipsRandomly(hjemmebane)

    return hjemmebane


###HER STARTER PROGRAMMET

#Definer globale konstanter
X_POSITION_COMPUTER_BOARD = 100
Y_POSITION_COMPUTER_BOARD = 280
X_POSITION_HUMAN_BOARD = 650
Y_POSITION_HUMAN_BOARD = 280
BOARD_SQUARE_SIZE = 32
SCREEN_HEIGHT = 640
SCREEN_WIDTH = 1024
ships = {"Busse": ["B1","B2","B3","B4","B5"], "Langskip": ["L1","L2","L3","L4"], "Jager": ["J1","J2","J3"], "Knarr": ["K1","K2","K3"], "Snekke": ["S1","S2"], "Pram": ["P1"]}
shipsRev = {"B": "busse", "L": "langskip", "J": "jager", "K": "knarr", "S": "snekke", "P": "pram"}

#Snurr film
main()
