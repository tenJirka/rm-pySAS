import subprocess

# List if problem letters that have some problems to show in current version of simple
PROBLEM_LETTERS = "ěščřžýáíéúů"
# Current version of this module is trying to prevent SAS from crash by doing some edits
# to texts displayed on screen and adding "." after letters that wont render without it.



# Widgets

class Label():
    """
    Represents label and is parent class for all text based widgets.
    If fontSize or justify is specified, adds them before occurrence of this label.
    """

    def __init__(self, x: int, y: int, w: int, h:int, text="", id="", fontSize=None, justify=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = diacriticsRepair(text)
        self.id = id
        self.fontSize = fontSize
        self.justify = justify

    def toStr(self, type: str) -> str:
        """
        Universal function for all child classes. Translate object to strings that will be passed to SAS
        """

        tempId = self.id
        if tempId != "":
            tempId=":" + self.id
        tempText = self.text
        if tempText != "":
            tempText = " " + self.text
        toReturn = type + tempId + " " + str(self.x) + " " + str(self.y) + " " + str(self.w) + " " + str(self.h) + tempText
        if type == "paragraph" or type == "textarea":
            toReturn = "[" + toReturn + "]"
        if self.fontSize != None:
            toReturn = str(FontSize(self.fontSize)) + "\n" + toReturn
        if self.justify != None:
            toReturn = str(Justify(self.justify)) + "\n" + toReturn
        return toReturn
    
    def __str__(self):
        return self.toStr("label")

class Paragraph(Label):
    """
    Class representing paragraph. Inherits everything from Label class.
    """

    def __str__(self):
        return self.toStr("paragraph")

class Button(Label):
    """
    Class representing button. Inherits everything from Label class.
    """

    def __str__(self):
        return self.toStr("button")

class TextInput(Label):
    """
    Class representing textinput. Inherits everything from Label class.
    """

    def __str__(self):
        return self.toStr("textinput")

class TextArea(Label):
    """
    Class representing textarea. Inherits everything from Label class.
    """

    def __str__(self):
        return self.toStr("textarea")

class Image():
    """
    Class representing image. Need path to image source.
    """

    def __init__(self, x: int, y: int, w: int, h: int, path: str, id: str):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        i = 0
        self.path = path
        self.id = id

    def __str__(self):
        tempId = self.id
        if tempId != "":
            tempId=":" + self.id
        toReturn = "image" + tempId + " " + str(self.x) + " " + str(self.y) + " " + str(self.w) + " " + str(self.h) + " " + self.path
        return toReturn

class Range():
    """
    Class representing range. Needs min, max, and value that will be displayed as default.
    """
    
    def __init__(self, x: int, y: int, w: int, h:int, min: int, max: int, value: int, id: str):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.min = min
        self.max = max
        self.value = value
        self.id = id

    def __str__(self):
        tempId = self.id
        if tempId != "":
            tempId=":" + self.id
        toReturn = "range" + tempId + " " + str(self.x) + " " + str(self.y) + " " + str(self.w) + " " + str(self.h) + " " + \
                   str(self.min) + " " + str(self.max) + " " + str(self.value)
        return toReturn


# Directives

class FontSize():
    """
    Specifies font size for all text based widgets that follow until next FontSize().
    """

    def __init__(self, size):
        self.size = size
    def __str__(self):
        return "@fontsize " + str(self.size)

class Justify():
    """
    Specifies font alignment for all text based widgets that follow until next Justify().
    Possible input: "left", "right", "center"
    """

    def __init__(self, justify):
        self.justify = justify
    def __str__(self):
        return "@justify " + str(self.justify)

class Timeout():
    """
     Specifies time in secs that SAS will wait until exit.
    """
    def __init__(self, timeout):
        self.timeout = timeout
    def __str__(self):
        return "@timeout " + str(self.timeout)

class NoClear():
    """
    When used, SAS will not clear the display between render.
    """
    def __str__(self):
        return "@noclear"


# Helper functions

def diacriticsRepair(text: str) -> str:
    """
    This functions take care of problem that make some diacritics letters disappear or make SAS crash
    """

    if text == "":
        return ""
    i = 0
    for letter in text:
        if letter in PROBLEM_LETTERS.upper():
            if i != 0:
                text = text[0:i] + letter.lower() + text[i+1:]
            else:
                text = letter.lower() + text[i+1:]
        i = i + 1
    if text[-1] in PROBLEM_LETTERS:
        text = text + "."
    return text


def parseOutput(output):
    """
    Parses output of SAS and return lists which contain id and text input, when exists.
    """

    if output[:9] == "selected:":
        button = output[10:]
        if button[-1].isspace():
            button = button[:-1]
        return [button, None]
    elif output[:6] == "input:" or output[:6] == "range:":
        name, input = output[7:].split(" : ", 1)
        if input[-1].isspace():
            input = input[:-1]
        return [name, input]

def passToSimple(input, encoding="utf-8", simplePath = "/opt/bin/simple"):
    """
    Passes all widgets to simple to render and then takes care of its output. Return list from parseOutput()
    """

    if type(input) is str:
        toPass == input
    elif type(input) is list:
        toPass = "\n".join(map(str, input))
    else:
        toPass = str(input)
    print(toPass)
    result = subprocess.run(['''echo "''' + toPass + '''" | ''' + simplePath], stdout=subprocess.PIPE, shell=True, text=True, encoding=encoding)
    output = str(result.stdout)
    return parseOutput(output)


# Interface class

class Scene():
    """
    One for all class that represent one scene, that should be displayed. Contains all widgets that will be passed to simple.
    """

    def __init__(self, noClear = False, timeOut=None, simplePath = "/opt/bin/simple", encoding="utf-8") -> None:
        self.widgets = []
        self.input = []
        self.simplePath = simplePath
        self.encoding = encoding
        if noClear:
            self.widgets.append(NoClear())
        if timeOut:
            self.widgets.append(Timeout(timeOut))
    
    def add(self, toDisplay):
        """
        Will add widget or lists of widgets to the scene.
        """

        if type(toDisplay) is list:
            self.widgets = self.widgets + toDisplay
        else:
            self.widgets.append(toDisplay)

    def display(self):
        """
        Pass all widgets to the SAS and then save the output to input variable.
        """

        self.input = passToSimple(self.widgets, simplePath=self.simplePath, encoding=self.encoding)
    
    def remove(self, id):
        """
        Searches for widget specified by id and than removes it from list of widgets.
        """        

        tmpWidget = None
        for widget in self.widgets:
            if hasattr(widget, "id"):
                if widget.id == id:
                    tmpWidget = widget
                    break
        if tmpWidget != None:
            self.widgets.remove(tmpWidget)