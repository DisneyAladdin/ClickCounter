from pynput import mouse
import wx
import time
import threading

class Singleton:
    _unique_instance = None
    elapsed_time = 0
    click_count = -1
    active_state = False
    
    @classmethod
    def get_instance(cls):
        if not cls._unique_instance:
            cls._unique_instance = cls()
            
        return cls._unique_instance
    def set_time(self,time):
        self.elapsed_time = time
        #print("set_time = {}".format(self.elapsed_time))

    def count_increment(self):
        self.click_count += 1
        print(self.click_count)

class AppFrame(wx.Frame):
    start_time = time.time()
    current_count = 0
    thread = None
    def __init__(self):
        wx.Frame.__init__( self, None, title="click count",size=(250, 100))
        frame = wx.Frame(None, -1, "click count")
        self.SetTransparent(255)
        self.start_time = time.time()
        main_panel = wx.Panel(self)
        date_time = wx.DateTime.Now()
        self.label_1 = wx.StaticText(main_panel, label="elapsed", pos=(20, 10))
        self.label_2 = wx.StaticText(main_panel, label="time:{0}".format(0) + "[sec]", pos=(20,10))
        self.label_3 = wx.StaticText(main_panel, label="click_count", pos=(20, 10))
        self.label_4 = wx.StaticText(main_panel, label="count:{0}".format(0), pos=(20,10))
        

        button_1 = wx.Button(main_panel, wx.ID_ANY, 'Start')
        button_2 = wx.Button(main_panel, wx.ID_ANY, 'Stop')
        
        button_1.Bind(wx.EVT_BUTTON, self.start)
        button_2.Bind(wx.EVT_BUTTON, self.stop)

        layout = wx.GridSizer(rows=3, cols=2, gap=(2, 2))
        layout.Add(self.label_1, 0, wx.GROW)
        layout.Add(self.label_2, 0, wx.GROW)
        layout.Add(self.label_3, 0, wx.GROW)
        layout.Add(self.label_4, 0, wx.GROW)
        layout.Add(button_1, 0, wx.GROW)
        layout.Add(button_2, 0, wx.GROW)
        
        main_panel.SetSizer(layout)

    
    def initialize(self):
        self.start_time = time.time()
        object = Singleton.get_instance()
        object.click_count = -1
        object.elapsed_time = 0
        object.active_state = False
        self.label_2.SetLabel("time:{0}".format(0) + "[sec]")
        
        
    def start(self,event):
        self.initialize()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update)
        self.timer.Start(1000)
        object = Singleton.get_instance()
        object.active_state = True
        if self.thread == None:
            self.thread = threading.Thread(target=click_liten)
            self.thread.start()
        
    def stop(self,event):
        self.timer.Stop()
        
    def update(self, event):
        current_label = self.label_2.GetLabel()
        new_time = time.time()
        delta = new_time - self.start_time
        delta = int(delta)
        object = Singleton.get_instance()
        object.set_time(delta)
        self.label_2.SetLabel("time:{0}".format(delta) + "[sec]")
        
        new_count = object.click_count
        if self.current_count != new_count:
            self.current_count = new_count
            self.label_4.SetLabel("count:{0}".format(new_count))
            
def on_click(x, y, button, pressed):
    print('{0} at {1}'.format('Pressed' if pressed else 'Released',(int(x), int(y))))
    if not pressed:
    ##    Stop listener
        object = Singleton.get_instance()
        object.count_increment()
    #    return False
def click_liten():
    object = Singleton.get_instance()
    while(True):
        if(object.active_state == False):
            break
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
        

def make_view():
    app = wx.App(False)
    frame = AppFrame().Show(True)
    app.MainLoop()

#object = Singleton.get_instance()
#while(True):
    
##    if(object.active_state == False):
#        break
#    with mouse.Listener(on_click=on_click) as listener:
        #print("tes")
#        listener.join()

make_view()
