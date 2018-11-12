# Copyright (c) 2017 Ultimaker B.V.
# This example is released under the terms of the AGPLv3 or higher.

import os.path
from PyQt5.QtCore import QUrl #To find the QML for the dialogue window.
from PyQt5.QtQml import QQmlComponent, QQmlContext #To create the dialogue window.

from UM.Application import Application #To listen to the event of creating the main window, and get the QML engine.
from UM.Extension import Extension #The PluginObject we're going to extend.
from UM.Logger import Logger #Adding messages to the log.
from UM.PluginRegistry import PluginRegistry #Getting the location of Hello.qml.


from UM.Message import Message
from UM.Scene.Selection import Selection
from .CalculateOrientationJob import CalculateOrientationJob

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("ConailsExampleExtension")





class ConailsExampleExtension(Extension): #Extension inherits from PluginObject, and provides some useful helper functions for adding an item to the application menu.
    ##  Creates an instance of this extension. This is basically the starting
    #   point of your code.
    #
    #   This is called by the register() function in __init__.py, which gets
    #   called during plug-in loading. That all happens before the splash screen
    #   even appears, so this code needs to be efficient. Also, be aware, that
    #   many things have not been loaded yet at this point.  
    def __init__(self):
        super().__init__()
        #A typical use of this constructor is to register some function to be
        #called upon some event in Uranium, or to add a menu item. In this case,
        #we will do both.


        ## Creating a menu item. ##
        #An extension can add several menu items. They all get placed under one header. This sets the title of that header.
        self.setMenuName("Conails Example Extension")

        #We'll add one item that says hello to the user.
        self.addMenuItem("Say hello", self.sayHello) #When the user clicks the menu item, the sayHello function is called.
        self.addMenuItem("conail Say hello", self.sayHello)
        self.addMenuItem("conail 2 Say hello", self.sayHello)
        self.addMenuItem("conails Calculate fast optimal printing orientation", self.doExtendedAutoOrientiation)
        # self.addMenuItem("conails Calculate extended optimal printing orie  ntation")

        self._message = None
        
        #Lazy-load the window. Create it when we first want to say hello.
        self.hello_window = None

        ## Reacting to an event. ##
        Application.getInstance().mainWindowChanged.connect(self.logMessage) #When the main window is created, log a message.

    ##  Creates a small dialogue window that says hello to the user.
    def sayHello(self):
        if not self.hello_window: #Don't create more than one.
            self.hello_window = self._createDialogue()
        self.hello_window.show()



    def doFastAutoOrientation(self):
        self.doAutoOrientation(False) 
         
    def doExtendedAutoOrientiation(self):
        #self.doAutoOrientation(True)
        self.data
        ##self._message = Message(i18n_catalog.i18nc("@info:status", "No objects selected to orient."))
        ##self._message.show()

    def doAutoOrientation(self, extended_mode):
        # If we still had a message open from last time, hide it.
        if self._message:
            self._message.hide()

        selected_nodes = Selection.getAllSelectedObjects()
        if len(selected_nodes) == 0:
            self._message = Message(i18n_catalog.i18nc("@info:status", "No objects selected to orient."))
            self._message.show()
            return

        self._message = Message(i18n_catalog.i18nc("@info:status", "Calculating optimal orientation"), 0, False, -1)
        self._message.show()

        job = CalculateOrientationJob(selected_nodes, extended_mode = extended_mode, message = self._message)
        job.finished.connect(self._onFinished)
        job.start()

    def _onFinished(self, job):
        if self._message:
            self._message.hide()









    ##  Adds a message to the log, as an example of how to listen to events.
    def logMessage(self):
        Logger.log("i", "This is an example log message.")

    ##  Creates a modal dialogue.
    def _createDialogue(self):
        #Create a QML component from the Hello.qml file.
        qml_file_path = os.path.join(PluginRegistry.getInstance().getPluginPath(self.getPluginId()), "Hello.qml")
        component = Application.getInstance().createQmlComponent(qml_file_path)

        return component