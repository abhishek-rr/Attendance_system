class err():
    e=""
    link=""
    
    def __init__(self,*args,**kwargs):
        if kwargs["e"] and kwargs["link"]:
            self.e=kwargs["e"]
            self.link=kwargs["link"]
        else:
            pass