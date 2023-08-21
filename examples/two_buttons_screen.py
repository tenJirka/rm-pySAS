from rm_pySAS import *

# Create object representing current scene on display
scene = Scene()

# Add text label to current scene on coordinates x = 500, y = 400, weight = 100 and height = 50
# Text of the label is "Testing scene", font size is 40 and text is alight to center
# All last three parameters are optional
scene.add(Label(500, 400, 100, 50, "Testing scene", fontSize=40, justify="center"))

# Add exit button to current scene with id=exit
# When no fontSize or justify is specified, it assume last value given from previous
# widgets or default SAS will be used.
scene.add(Button(300, 800, 100, 50 , "Exit", id="exit"))

# Create second button, that will do anything.
scene.add(Button(800, 800, 100, 50, "Button that does nothing", id="button"))

# Creating event loops tha will end only when exit button is clicked
while(True):
    scene.display()

    # scene.input represent output from SAS and is actually scripts input
    # It's list of id of widget interacted with and, if exists, value entered.

    # When exit button is pressed, the cycle will break.
    if scene.input[0] == "exit":
        break