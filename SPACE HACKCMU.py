from cmu_graphics import *
import math

class Button:
    def __init__(self, app, left, top, sizeX, sizeY, color, *function, label='', labelColor=None, labelSize=20, shape='square', radius=None):
        self.left = left
        self.top = top
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.color = color
        self.label = label
        self.labelColor = labelColor
        self.function = function
        self.labelSize = labelSize
        self.shape = shape
        self.radius = radius
        if radius != None:
            self.maxRadius = radius + 10
            self.minRadius = radius
    def __repr__(self):
        return f"Starts at {self.left},{self.top}, dimensions {self.sizeX}x{self.sizeY}"
    def __eq__(self, other):
        return isinstance(other, Button) and self.left == other.left and self.top == other.top and self.sizeX == other.sizeX and self.sizeY == other.sizeY and self.function == other.function
    def __hash__(self):
        return hash(str(self))
    def checkClick(self, app):
        if self.shape == 'square':
            if self.left < app.mouseX < self.left + self.sizeX and self.top < app.mouseY < self.top + self.sizeY:
                for function in self.function:
                    function()
        elif self.shape == 'circle':
            if distance(app.mouseX, app.mouseY, self.left + self.sizeX/2, self.top + self.sizeY/2) < self.radius:
                for function in self.function:
                    function()
    def checkHover(self, app):
        if self.shape == 'square':
            return self.left < app.mouseX < self.left + self.sizeX and self.top < app.mouseY < self.top + self.sizeY
        elif self.shape == 'circle':
            return distance(app.mouseX, app.mouseY, self.left + self.sizeX/2, self.top + self.sizeY/2) < self.radius
    def draw(self):
        if self.shape == 'square':
            drawRect(self.left, self.top, self.sizeX, self.sizeY, fill=self.color)
        elif self.shape == 'circle':
            drawCircle(self.left + self.sizeX/2, self.top + self.sizeY/2, self.radius, fill=self.color)
        drawLabel(self.label, self.left+(self.sizeX/2), self.top+(self.sizeY/2), fill=self.labelColor, size=self.labelSize)
    def hovering(self):
        self.radius = min(self.radius+5, self.maxRadius)
    def normalize(self):
        self.radius = max(self.radius-5, self.minRadius)

class AppButton(Button):
    def __init__(self, app, left, top, sizeX, sizeY, color, *function, label='', labelColor=None, labelSize=50, shape='square', radius=None):
        self.left = left
        self.top = top
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.color = color
        self.label = label
        self.labelColor = labelColor
        self.function = function
        self.labelSize = labelSize
        self.shape = shape
        self.radius = radius
        if radius != None:
            self.maxRadius = radius + 10
            self.minRadius = radius
    def checkClick(self, app):
        if self.shape == 'square':
            if self.left < app.mouseX < self.left + self.sizeX and self.top < app.mouseY < self.top + self.sizeY:
                for function in self.function:
                    function(app)
        elif self.shape == 'circle':
            if distance(app.mouseX, app.mouseY, self.left + self.sizeX/2, self.top + self.sizeY/2) < self.radius:
                for function in self.function:
                    function(app)

class ScreenButton(Button):
    def __init__(self, app, left, top, sizeX, sizeY, color, screen, *function, label='', labelColor=None, labelSize=30, shape='square', radius=None):
        self.left = left
        self.top = top
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.color = color
        self.label = label
        self.labelColor = labelColor
        self.function = function
        self.screen = screen
        self.labelSize = labelSize
        self.shape = shape
        self.radius = radius
        if radius != None:
            self.maxRadius = radius + 10
            self.minRadius = radius
    def checkClick(self, app):
        if self.shape == 'square':
            if self.left < app.mouseX < self.left + self.sizeX and self.top < app.mouseY < self.top + self.sizeY:
                for function in self.function:
                    function(self.screen)
                #if self.screen == 'title':
                    #app.menuTheme.play(loop = True)
        elif self.shape == 'circle':
            if distance(app.mouseX, app.mouseY, self.left + self.sizeX/2, self.top + self.sizeY/2) < self.radius:
                #app.clickCircleButtonSound.play(restart = True)
                for function in self.function:
                    function(self.screen)
                #if self.screen == 'timed' or self.screen == 'limitless':
                    #app.menuTheme.pause()
# BUTTONS TAKEN FROM JPIDHERN TP IN 15-112

class Question():
    def __init__(self, app, question, answers, function=None, font=''):
        self.question = question   
        self.answers = answers
        self.font = font
        self.function = function
    def draw(self, app):
        drawLabel(self.question, app.width/2, app.height*(1/8),size=60)
        i=1
        for answer in self.answers:
            if app.selectedChoice == answer:
                drawLabel(answer, app.width/2, app.height*(1/8)+(i*(app.height/8)), fill="green", size=50)
            else:
                drawLabel(answer, app.width/2, app.height*(1/8)+(i*(app.height/8)), fill="black", size=50)
            i+=1
    def checkClick(self, app):
        for choice in range(0,len(self.answers)):
            if (app.height*(11/64)+((choice*4+1)*(app.height*(1/32))) < app.mouseY < app.height*(11/64)+((choice*4+4)*(app.height*(1/32))) and (app.width/8 < app.mouseX < 7*(app.width/8))):
                app.selectedChoice = self.answers[choice]
                if self.function != None:
                    self.function(app)

class OrbitAroundStarQuestion(Question):
    def enterAnswer(self, app):
        indexOfAns = app.orbitAroundStarAnswerList[app.questionNumber].index(app.selectedChoice)
        answer = app.orbitAroundStarAnswerToValueList[app.questionNumber][indexOfAns]
        app.orbitAroundStarUserAnswerList.append(answer)

class SpecialQuestion(OrbitAroundStarQuestion):
    def checkClick(self, app):
        for choice in range(0,len(self.answers)):
            if (app.height*(11/64)+((choice*4+1)*(app.height*(1/32))) < app.mouseY < app.height*(11/64)+((choice*4+4)*(app.height*(1/32))) and (app.width/8 < app.mouseX < 7*(app.width/8))
                 and (self.answers[choice] not in app.selectedChoiceList)):
                    app.selectedChoiceList.append(self.answers[choice])
            elif (app.height*(11/64)+((choice*4+1)*(app.height*(1/32))) < app.mouseY < app.height*(11/64)+((choice*4+4)*(app.height*(1/32))) and (app.width/8 < app.mouseX < 7*(app.width/8))
                 and self.answers[choice] in app.selectedChoiceList):
                    app.selectedChoiceList.pop(app.selectedChoiceList.index(self.answers[choice]))
            if self.function != None:
               self.function(app)
    def draw(self, app):
        drawLabel(self.question, app.width/2, app.height*(1/8),size=60)
        i=1
        for answer in self.answers:
            if answer in app.selectedChoiceList:
                drawLabel(answer, app.width/2, app.height*(1/8)+(i*(app.height/8)), fill="green", size=50)
            else:
                drawLabel(answer, app.width/2, app.height*(1/8)+(i*(app.height/8)), fill="black", size=50)
            i+=1
    def enterAnswer(self,app):
        tempList = []
        for choice in range(0,len(app.selectedChoiceList)):
            indexOfAns = app.orbitAroundStarAnswerList[app.questionNumber].index(app.selectedChoiceList[choice])
            answer = app.orbitAroundStarAnswerToValueList[app.questionNumber][indexOfAns]
            tempList.append(answer)    
        app.orbitAroundStarUserAnswerList.append(tempList)

class GravitationalAttractionQuestion(Question):
    def enterAnswer(self, app):
        indexOfAns = app.gravitationalAttractionAnswerList[app.questionNumber].index(app.selectedChoice)
        answer = app.gravitationalAttractionAnswerToValueList[app.questionNumber][indexOfAns]
        app.gravitationalAttractionUserAnswerList.append(answer)

class ElectricalAttractionQuestion(Question):
    def enterAnswer(self, app):
        indexOfAns = app.electricalAttractionAnswerList[app.questionNumber].index(app.selectedChoice)
        answer = app.electricalAttractionAnswerToValueList[app.questionNumber][indexOfAns]
        app.electricalAttractionUserAnswerList.append(answer)
        

def title_onAppStart(app):
    app.mouseX = 0
    app.mouseY = 0
    app.width = 1700
    app.height = 890
    app.fOffsetX = 0
    app.fOffsetY = 0
    app.mouseX = 0
    app.mouseY = 0
    app.name = ''
    app.nameList = []
    app.attractionMessage = ''
    app.futurePrediction = ''
    app.selectedChoice = ""
    app.selectedChoiceList = []
    app.questionNumber = 0
    app.currentPlayer = 0
    app.enterPlayerNamesButton = ScreenButton(app, app.width/4, (app.height/4), app.width/2, app.height/2, "pink", "names", setActiveScreen, label="Start Love Test!", labelSize=50)
    app.nextButton = AppButton(app, app.width*(7/8), 13*app.height/16, app.width/8, app.height/8, "green", nextQ, label="Next Question!", labelSize=20)
    app.againButton = ScreenButton(app, app.width/4,app.height/4,app.width/2,app.height/2, "pink", "test", setActiveScreen, label='Click Me!', labelSize=50)
    app.orbitAroundStarQuestionList = ["What is your career/education?","What are your interests/hobbies/frequent activites?","On a scale of 0-5, how often do you interact with sports?","On a scale of 0-5, how often do you interact with Video Games?","On a scale of 0-5, how often do you interact with Cooking?","On a scale of 0-5, how often do you engage in Arts/Crafts?","On a scale of 0-5, how often do you watch shows?"]
    app.orbitAroundStarAnswerList = [["a. Natural Sciences", "b. Engineering", "c. Humanities", "d. Art/Music/Drama", "e. Computer Science", "f. Business"],["a. Sports","b. Video Games","c. Cooking","d. Arts/Crafts", "e. Watching Shows"],["a. 5","b. 4","c. 3","d. 2","e. 1","f. 0"], ["a. 5","b. 4","c. 3","d. 2","e. 1","f. 0"], ["a. 5","b. 4","c. 3","d. 2","e. 1","f. 0"], ["a. 5","b. 4","c. 3","d. 2","e. 1","f. 0"], ["a. 5","b. 4","c. 3","d. 2","e. 1","f. 0"]]
    app.orbitAroundStarUserAnswerList = []
    app.orbitAroundStarAnswerToValueList = [["a","b","c",'d','e','f'],['a','b','c','d','e'],[5,4,3,2,1,0],[5,4,3,2,1,0],[5,4,3,2,1,0],[5,4,3,2,1,0],[5,4,3,2,1,0]]
    #app.gravitationalAttractionQuestionList = [f"How often does {app.nameList[1]} work out?",f"What is {app.nameList[1]}'s influence in the fabric of society?", "How often do you two meet?", "How far do you two live from one another?"]
    app.gravitationalAttractionAnswerList = [["a. Abs for days!", "b. Enough to tone", "c. Healthy amount", "d. Less than they should", "e. Never"],["a. Gee! What a person!", "b. Wow! A world changer in the making!", "c. Just a regular ol' person", "d. They don't volunteer or give to charity. Ever.", "e. Ummm, they barely exist"],
                                             ["a. Gosh, barely","b. Every week... in class :(","c. Every week for lunch!","d. Almost everyday!","e. Every. Single. Day"], ["a. They live sooo far away", "b. They live in another state", "c. Same city!","d. Same block!", "e. We're practically superimposed!"]]
    app.gravitationalAttractionUserAnswerList = []
    app.gravitationalAttractionAnswerToValueList = [[83.7,63.7,43.7,33.7,23.7],[5,4,3,2,1],[83.7,63.7,43.7,33.7,23.7],[5,4,3,2,1]]
    #app.electricalAttractionQuestionList = [f"How does {app.nameList[1]} make you feel?",f"How do you think you make {app.nameList[1]} feel?"]
    app.electricalAttractionAnswerList = [["a. Absolutely grossed out","b. Annoyed","c. Indifferent, and a little hungry", "d. Fluttery", "e. In LOVE!"], ["a. Absolutely grossed out","b. Annoyed","c. Indifferent, and a little hungry", "d. Fluttery", "e. In LOVE!"]]
    app.electricalAttractionUserAnswerList = []
    app.electricalAttractionAnswerToValueList = [[(-5.3)*(10**16),(-2.3)*(10**12), 0, (2.3)*(10**12), (5.3)*(10**16)], [(-5.3)*(10**16),(-2.3)*(10**12), 0, (2.3)*(10**12), (5.3)*(10**16)]]
    app.stageList = ["Orbit Around Star", "Gravitational Attraction", "Electrical Attraction"]
    app.currentStage = 0
    app.player1TotalAnswerList = []
    app.player2TotalAnswerList = []
    #app.question1 = OrbitAroundStarQuestion(app, "What is your career/education?", ["a. Natural Sciences", "b. Engineering", "c. Humanities", "d. art/music/drama", "e. Computer Science", "f. Business"])
    #app.question2 = GravitationalAttractionQuestion(app, "What is the influence of the other entity in the fabric of society?", ["a. Gee! What a person!", "b. Wow! A world changer in the making!", "c. Just a regular ol' person", "d. They don't volunteer or give to charity. Ever.", "e. Ummm, they barely exist"])
    app.currentQuestion = OrbitAroundStarQuestion(app, app.orbitAroundStarQuestionList[0], app.orbitAroundStarAnswerList[0])
    #app.heartImage = CMUImage(Image.open('sprites/heartspace.png'))
#https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/5f361c20-87a0-47f4-9217-383117f5371c/d6kyaku-765a9fd1-25ed-4c69-98aa-ae64316a0d77.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzVmMzYxYzIwLTg3YTAtNDdmNC05MjE3LTM4MzExN2Y1MzcxY1wvZDZreWFrdS03NjVhOWZkMS0yNWVkLTRjNjktOThhYS1hZTY0MzE2YTBkNzcucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.uL3esdSErbee255BgUUsvJJ0MS8aNODQs8VSAVYNKMg
def title_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill="black")
    #drawImage(app.heartImage, app.width/4, (app.height/4)*(1/2))
    app.enterPlayerNamesButton.draw()

def title_onMouseMove(app, mouseX, mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY

def title_onMousePress(app, mouseX, mouseY):
    app.enterPlayerNamesButton.checkClick(app)

def names_onAppStart(app):
    pass

def names_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill="pink")
    if len(app.nameList) == 0:
        drawLabel("Player 1's Name:", app.width/2, app.height/3, size=50)
        drawLabel(app.name, app.width/2, app.height/2, size=50)
    elif len(app.nameList) == 1:
        drawLabel("Player 2's Name:", app.width/2, app.height/3, size=50)
        drawLabel(app.name, app.width/2, app.height/2, size=50)

def names_onKeyPress(app, key):
    if (key == 'space' or (key == 'shift' and key == 'space')) and len(app.name) > 0:
        app.name = app.name + ' '
    elif key == 'backspace' and len(app.name) > 0:
        app.name = app.name[:-1]
    elif key == 'enter' and len(app.name) > 0 and len(app.nameList) == 0:
        app.nameList.append(app.name)
        app.name = ''
    elif key == 'enter' and len(app.name) > 0 and len(app.nameList) == 1:
        app.nameList.append(app.name)
        app.name = ''
        app.gravitationalAttractionQuestionList = [f"How often does {app.nameList[1]} work out?",f"What is {app.nameList[1]}'s influence in the fabric of society?", "How often do you two meet?", "How far do you two live from one another?"]
        app.electricalAttractionQuestionList = [f"How does {app.nameList[1]} make you feel?",f"How do you think you make {app.nameList[1]} feel?"]
        setActiveScreen("test")
    elif key.isalpha() == True:
        app.name += key

def test_onAppStart(app):
    pass

def test_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill="pink")
    drawLabel(f'{app.nameList[app.currentPlayer]}', app.width/16, app.height/16, fill='red', size=30)
    app.currentQuestion.draw(app)
    #for choice in range(len(app.questionTest.answers)):
        #drawLine(0, app.height*(11/64)+((choice*4+1)*(app.height*(1/32))), app.width, app.height*(11/64)+((choice*4+1)*(app.height*(1/32))))
        #drawLine(0, app.height*(11/64)+((choice*4+4)*(app.height*(1/32))), app.width, app.height*(11/64)+((choice*4+4)*(app.height*(1/32))))
    if app.selectedChoice != "" or app.selectedChoiceList != []:
        app.nextButton.draw()

def test_onMouseMove(app, mouseX, mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY

def test_onMousePress(app, mouseX, mouseY):
    app.currentQuestion.checkClick(app)
    if app.selectedChoice != "" or app.selectedChoiceList != []:
        app.nextButton.checkClick(app)
    

def nextQ(app):
    app.currentQuestion.enterAnswer(app)
    if app.questionNumber + 1 <= len(app.orbitAroundStarQuestionList) - 1 and app.currentStage == 0:
        app.questionNumber += 1
    elif app.questionNumber + 1 <= len(app.gravitationalAttractionQuestionList) - 1 and app.currentStage == 1:
        app.questionNumber += 1
    elif app.questionNumber + 1 <= len(app.electricalAttractionQuestionList) - 1 and app.currentStage == 2:
        app.questionNumber += 1
    elif app.currentStage + 1 <= len(app.stageList) - 1:
        app.questionNumber = 0
        app.currentStage += 1
    elif app.currentPlayer == 0:
        app.currentStage = 0
        app.questionNumber = 0
        app.player1TotalAnswerList.append(app.orbitAroundStarUserAnswerList)
        app.player1TotalAnswerList.append(app.gravitationalAttractionUserAnswerList)
        app.player1TotalAnswerList.append(app.electricalAttractionUserAnswerList)
        app.gravitationalAttractionQuestionList = [f"How often does {app.nameList[0]} work out?",f"What is {app.nameList[0]}'s influence in the fabric of society?", "How often do you two meet?", "How far do you two live from one another?"]
        app.electricalAttractionQuestionList = [f"How does {app.nameList[0]} make you feel?",f"How do you think you make {app.nameList[0]} feel?"]
        app.orbitAroundStarUserAnswerList = []
        app.gravitationalAttractionUserAnswerList = []
        app.electricalAttractionUserAnswerList = []
        app.currentPlayer = 1
        setActiveScreen("switchPlayer")
    elif app.currentPlayer == 1:
        app.player2TotalAnswerList.append(app.orbitAroundStarUserAnswerList)
        app.player2TotalAnswerList.append(app.gravitationalAttractionUserAnswerList)
        app.player2TotalAnswerList.append(app.electricalAttractionUserAnswerList)
        app.orbitAroundStarUserAnswerList = []
        app.gravitationalAttractionUserAnswerList = []
        app.electricalAttractionUserAnswerList = []
        print(app.player1TotalAnswerList, app.player2TotalAnswerList)
        calculate(app)
        setActiveScreen("end")
    else:
        print("error")
    app.selectedChoice = ""
    app.selectedChoiceList = []
    if app.currentStage == 0:
        if app.questionNumber == 1:
            app.currentQuestion = SpecialQuestion(app, app.orbitAroundStarQuestionList[app.questionNumber], app.orbitAroundStarAnswerList[app.questionNumber])
        else:
            app.currentQuestion = OrbitAroundStarQuestion(app, app.orbitAroundStarQuestionList[app.questionNumber], app.orbitAroundStarAnswerList[app.questionNumber])
    elif app.currentStage == 1:
        app.currentQuestion = GravitationalAttractionQuestion(app, app.gravitationalAttractionQuestionList[app.questionNumber], app.gravitationalAttractionAnswerList[app.questionNumber])
    elif app.currentStage == 2:
        app.currentQuestion = ElectricalAttractionQuestion(app, app.electricalAttractionQuestionList[app.questionNumber], app.electricalAttractionAnswerList[app.questionNumber])

def switchPlayer_onAppStart(app):
    pass

def switchPlayer_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill='Black')
    drawLabel(f"Okay, it's {app.nameList[1]}'s turn now!", app.width/2, app.height/8, size=50, fill='white')
    app.againButton.draw()

def switchPlayer_onMouseMove(app,mouseX,mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY

def switchPlayer_onMousePress(app,mouseX,mouseY):
    app.againButton.checkClick(app)

def end_onAppStart(app):
    pass

def end_redrawAll(app):
    #need restart function
    drawRect(0,0,app.width,app.height,fill="black")
    i=-3
    j=2
    drawLabel("Attraction:", app.width/2, (app.height/2)+app.height*((i-1)/16), size=40, fill='red')
    drawLabel("Future Predictions", app.width/2, (app.height/2)+app.height*((j-1)/16), size=40, fill='red')
    for message in app.attractionMessage:
        drawLabel(message, app.width/2, (app.height/2)+app.height*(i/16), size=40, fill='white')
        i+=1
    for message in app.futurePrediction:
        drawLabel(message, app.width/2, (app.height/2)+app.height*(j/16), size=40, fill='white')
        j+=1

def calculate(app):
    #star mass
    p1StarMassQ1 = app.player1TotalAnswerList[0][0]
    p2StarMassQ1 = app.player2TotalAnswerList[0][0]
    if p1StarMassQ1 == p2StarMassQ1:
        starMassQ1 = 8.8
    elif ((p1StarMassQ1 == 'a' and p2StarMassQ1 == 'b') or
        (p1StarMassQ1 == 'b' and p2StarMassQ1 == 'a') or
        (p1StarMassQ1 == 'a' and p2StarMassQ1 == 'e') or
        (p1StarMassQ1 == 'e' and p2StarMassQ1 == 'a') or
        (p1StarMassQ1 == 'b' and p2StarMassQ1 == 'e') or
        (p1StarMassQ1 == 'e' and p2StarMassQ1 == 'b') or
        (p1StarMassQ1 == 'c' and p2StarMassQ1 == 'd') or
        (p1StarMassQ1 == 'd' and p2StarMassQ1 == 'c') or
        (p1StarMassQ1 == 'c' and p2StarMassQ1 == 'f') or
        (p1StarMassQ1 == 'f' and p2StarMassQ1 == 'c')):
            starMassQ1 = 5.8
    else:
        starMassQ1 = 2.8
    p1StarMassQ2 = app.player1TotalAnswerList[0][1]
    p2StarMassQ2 = app.player2TotalAnswerList[0][1]
    res = 0
    for ans in p1StarMassQ2:
        if ans in p2StarMassQ2:
            res += 1
    starMassQ2 = res
    #getting star mass from questions
    starMass = (starMassQ1) * 10**(10+4*(starMassQ2))
    
    #semi-major axis
    p1choiceA = app.player1TotalAnswerList[0][2]
    p1choiceB = app.player1TotalAnswerList[0][3]
    p1choiceC = app.player1TotalAnswerList[0][4]
    p1choiceD = app.player1TotalAnswerList[0][5]
    p1choiceE = app.player1TotalAnswerList[0][6]
    p2choiceA = app.player2TotalAnswerList[0][2]
    p2choiceB = app.player2TotalAnswerList[0][3]
    p2choiceC = app.player2TotalAnswerList[0][4]
    p2choiceD = app.player2TotalAnswerList[0][5]
    p2choiceE = app.player2TotalAnswerList[0][6]
    p1a = ((p1choiceA+p1choiceB+p1choiceC+p1choiceD+p1choiceE)/5)*(10**8)
    p2a = ((p2choiceA+p2choiceB+p2choiceC+p2choiceD+p2choiceE)/5)*(10**8)


    #period
    G = 6.67*10**(-11)
    p1period = ((4*(math.pi**2)*(p1a**3))/(G*(starMass)))**0.5
    p2period = ((4*(math.pi**2)*(p2a**3))/(G*(starMass)))**0.5

################################################################################

    #mass
    p1MassQ1 = app.player1TotalAnswerList[1][0]
    p2MassQ1 = app.player2TotalAnswerList[1][0]
    p1MassQ2 = app.player1TotalAnswerList[1][1]
    p2MassQ2 = app.player2TotalAnswerList[1][1]
    m = p2MassQ1 * 10**(10+(5*p2MassQ2))
    M = p1MassQ1 * 10**(10+(5*p1MassQ2))

    #radius
    p1RadiusQ1 = app.player1TotalAnswerList[1][2]
    p2RadiusQ1 = app.player2TotalAnswerList[1][2]
    p1RadiusQ2 = app.player1TotalAnswerList[1][3]
    p2RadiusQ2 = app.player2TotalAnswerList[1][3]
    p1r = p1RadiusQ1*10**(10+2*p1RadiusQ2)
    p2r = p2RadiusQ1*10**(10+2*p2RadiusQ2)
    r = (p1r+p2r)/2

    #gravitational attraction force
    Fg = G*M*m/(r**2)

################################################################################

    #gravitational star force
    p1Fgs = G*starMass*m/p1a**2
    p2Fgs = G*starMass*m/p2a**2

    #velocity of orbit:******
    p1escape = False
    p1v = (p1Fgs*(p1a)/m)**0.5
    p1escapev = ((2*G*starMass)/p1a)**0.5
    if p1v > p1escapev:
        p1escape = True
    p2escape = False
    p2v = (p2Fgs*(p2a)/M)**0.5
    p2escapev = ((2*G*starMass)/p2a)**0.5
    if p2v > p2escapev:
        p2escape = True

################################################################################

    #charge
    p1ChargeQ1 = app.player1TotalAnswerList[2][0]
    p2ChargeQ1 = app.player2TotalAnswerList[2][0]
    p1ChargeQ2 = app.player1TotalAnswerList[2][1]
    p2ChargeQ2 = app.player2TotalAnswerList[2][1]
    q = (p1ChargeQ1+p2ChargeQ2)/2
    Q = (p1ChargeQ2+p2ChargeQ1)/2

    #electric force
    k = 8.99*10**(9)
    Fe = k*(Q*q/r**2)

################################################################################

    #net force
    Fn = Fg + Fe

################################################################################
    #calculation of attraction
    maxGForce = (G*(83.7*10**25)**2)/(7.3*10**12)**2
    maxEForce = (k*(5.3*10**12)**2)/(7.3*10**12)**2
    maxForce = maxGForce + maxEForce
    minGForce = (G*(23*10**16)**2)/(87.3*10**20)**2
    minEForce = (k*((-5.3)*10**16)**2)/(87.3*10**20)**2
    minForce = minGForce + minEForce
    rangeGForce = maxGForce - minGForce
    rangeEForce = maxEForce - minEForce
    rangeForce = maxForce - minForce
    intervalGForce = rangeGForce//3
    intervalEForce = rangeEForce//3
    intervalForce = rangeForce//3
    if Fg<(minGForce+intervalGForce):  
        gScore = 1
    elif Fg<(minGForce+2*intervalGForce):  
        gScore = 2
    else:
        gScore = 3
    if Fe<(minEForce+intervalEForce):  
        eScore = 1 
    elif Fe<(minEForce+2*intervalEForce):  
        eScore = 2
    else:
        eScore = 3
    if Fn<(minForce+intervalForce):  
        nScore = 1 
    elif Fn<(minForce+2*intervalForce):  
        nScore = 2
    else:
        nScore = 3


    # gPercentage = ((Fg-minGForce)/(maxGForce-minGForce))*(100**18)
    # ePercentage = ((Fe-minEForce)/(maxEForce-minEForce))*(100**12)
    # totalPercentage = ((Fn-minForce)/(maxForce-minForce))*(100**18)
    if nScore == 1:
        witty = "Go take a meteor shower because your love life stinks"
    elif nScore == 2:
        witty = "Love is strong with the galaxy far, far away"
    elif nScore == 3:
        witty = "Star-crossed lovers!"
    else:
        witty = "robust"

    app.attractionMessage = [f"The gravitational attraction between you two is level {gScore}.", 
    f"The electric attraction between you two is level {eScore}.", 
    f"Therefore, the net attraction is level {nScore}!",
    f"{witty}"]

    #velocity of orbit:******
    p1escape = False
    p1v = (p1Fgs*(p1a)/m)**0.5
    p1escapev = ((2*G*starMass)/p1a)**0.5
    if p1v > p1escapev:
        p1escape = True
    p2escape = False
    p2v = (p2Fgs*(p2a)/M)**0.5
    p2escapev = ((2*G*starMass)/p2a)**0.5
    if p2v > p2escapev:
        p2escape = True

    #future predictions
    if p1escape and p2escape:
        escapePrediction = f"It's not meant to be. You two will most likely be saying bye forever soon!"
    elif  p1escape and not p2escape:
        escapePrediction = f"Be careful, {app.nameList[0]} is likely to escape orbit."
    elif  not p1escape and p2escape:
        escapePrediction = f"Be careful, {app.nameList[1]} is likely to escape orbit."
    else:
        escapePrediction = f"It's meant to be! You'll be together for a long time."

    if p1period > p2period:
        periodPrediction = f"It seems like {app.nameList[1]} will be running to see {app.nameList[0]}."
    elif p2period > p1period:
        periodPrediction = f"It seems like {app.nameList[0]} will be running to see {app.nameList[1]}."
    else:
        periodPrediction = "It seems like you two race to see each other!"

    app.futurePrediction = [f"{escapePrediction}", f"{periodPrediction}"]

def main():
    runAppWithScreens("title")

main()