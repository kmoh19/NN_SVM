import math
import random
 
class unit():
    def __init__(self,value,grad):
        self.value=value
        self.grad=grad
 
class multiplyGate():
    def __init__(self,u0,u1):
        self.u0=u0
        self.u1=u1
   
    def forward(self,u0,u1):
        self.u0=u0
        self.u1=u1
        self.utop= unit(self.u0.value * self.u1.value,0.0)
        return self.utop
   
    def backward(self):
        self.u0.grad +=self.u1.value * self.utop.grad
        self.u1.grad +=self.u0.value * self.utop.grad
        #print self.u0.grad
        #print self.u1.grad
        return None
   
class addGate():
    def __init__(self,u0,u1):
        self.u0=u0
        self.u1=u1
   
    def forward(self,u0,u1):
        self.u0=u0
        self.u1=u1
        self.utop= unit(self.u0.value + self.u1.value,0.0)
        return self.utop
   
    def backward(self):
        self.u0.grad +=1 * self.utop.grad
        self.u1.grad +=1 * self.utop.grad
        #print self.u0.grad
        #print self.u1.grad
        return None
       
##===================##=================##================##=====================##=================##=================================
class Circuit():
   
    def __init__(self,a,b,c,x,y):# redundant just did it to gel with gate class defs
        self.mulg0 = multiplyGate(a,x)
        self.mulg1 = multiplyGate(b,y)
        self.addg0 = addGate(self.mulg0.forward(a,x),self.mulg1.forward(b,y))
        self.addg1 = addGate(self.addg0.forward(self.mulg0.forward(a,x),self.mulg1.forward(b,y)),c)
   
    def forward(self,x,y,a,b,c):
        self.ax= self.mulg0.forward(a,x)
        self.by= self.mulg1.forward(b,y)
        self.axpby=self.addg0.forward(self.ax,self.by)
        self.axpbypc=self.addg1.forward(self.axpby,c)
        return self.axpbypc
   
    def backward(self,gradient_top):
        self.axpbypc.grad=gradient_top
        self.addg1.backward()
        self.addg0.backward()
        self.mulg1.backward()
        self.mulg0.backward()
        return None
 
 
class SVM():
 
   
    def __init__(self):
        self.a= unit(1.0,0.0)
        self.b= unit(-2.0,0.0)
        self.c= unit(-1.0,0.0)
        self.x=unit(1.0,0.0)
        self.y=unit(1.0,0.0)
        self.circuit=Circuit(self.a,self.b,self.c,self.x,self.y)
       
    
    
        
    def forward(self,x,y):
        self.unit_out=self.circuit.forward(x,y,self.a,self.b,self.c)
        return self.unit_out
   
    def backward(self,label):
        self.a.grad=0.0
        self.b.grad=0.0
        self.c.grad=0.0
       
        pull=0
       
        if label==1 and self.unit_out.value < 1:
            pull=1
           
        if label==-1 and self.unit_out.value > -1:
            pull=-1
           
        #regularize
        self.circuit.backward(pull)
       
        self.a.grad += -self.a.value
        self.b.grad += -self.b.value
       
        return None
   
    def learnFrom(self,x,y,label):
        self.forward(x,y)
        self.backward(label)
        self.parameterUpdate()
        return None
   
    def parameterUpdate(self):
        step_size=0.01
        self.a.value +=step_size*self.a.grad
        self.b.value +=step_size*self.b.grad
        self.c.value +=step_size*self.c.grad
        return None
                    
 
data=[[1.2,0.7],[-0.3,-0.5],[3.0,0.1],[-0.1,-1.0],[-1.0,1.1],[2.1,-3]]
labels=[1,-1,1,-1,-1,1]
 
svm=SVM()
 
def evalTrainingAccuracy():
    num_correct=0
    for idx,i in enumerate(data):
        x= unit(i[0],0.0)
        y= unit(i[1],0.0)
        true_label=labels[idx]
       
        tt=svm.forward(x,y).value
        if svm.forward(x,y).value>0:
            predicted_label=1
        else:
            predicted_label=-1
       
        if  predicted_label==true_label:
            num_correct +=1
           
    return float(num_correct)/len(data)
 
 
 
 
#learning loop
 
for itr in range(1,600):
    i=int(math.floor(random.random()*len(data)))
    x= unit(data[i][0],0.0)
    y= unit(data[i][1],0.0)
    label=labels[i]
   
    svm.learnFrom(x,y,label)
    if itr % 25==0:
        print 'training accuracy at iter ' + str(itr) + ': ' + str(evalTrainingAccuracy())
        
        
        