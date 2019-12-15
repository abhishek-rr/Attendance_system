from django.db.models import Q
from attendance.models import attendance
from datetime import timedelta,datetime
import plotly.offline as py
import plotly.graph_objs as go

def totalatt(subj_para,Class_para):
    time_list=[]
    q=(Q(subject=subj_para)&Q(Class=Class_para))
    att_list=attendance.objects.filter(q).values_list('date_time',flat=True)
    for time in att_list:
        time=time-timedelta(seconds=time.second,minutes=time.minute)
        if time not in time_list:
            time_list.append(time)
    return len(time_list)
    
def piechart(stud_pro):
    labels=[]
    values=[]
    c=0
    Absent_value=0
    for sub in stud_pro.subject.all():
        labels.append(str(sub))
        q=(Q(subject=sub)&Q(student=stud_pro.user_id))
        att=attendance.objects.filter(q).count()
        att_total=totalatt(sub,stud_pro.Class)
        Absent_value+=att_total-att
        values.append(att)
        c=c+1
    colors_list=['#06858C', '#45C48B','#323741','#FFD039','#F47942']
    colors=[]
    for i in range(c):
        colors.append(colors_list[i])
    labels.append("ABSENT")
    values.append(Absent_value)
    colors.append
    trace = go.Pie(labels=labels,values=values,textfont=dict(size=20),marker=dict(colors=colors,line=dict(color='#000000', width=2)),showlegend=False)
    return py.plot([trace],include_plotlyjs=False,output_type="div",config={'show_link':False})  
    
def bar_graph(dat):
    
    x = []
    y = []
    y2 = []
    for sub in dat:
        x.append(str(sub[0]))
        y2.append(sub[1])
        y.append(sub[2])
    trace1 = go.Bar(x=x,y=y,text="Total Attendance",marker=dict(color='rgb(158,202,225)',line=dict(color='rgb(8,48,107)',width=1.5),),opacity=0.6)
    trace2 = go.Bar(x=x,y=y2,text="Attendance",marker=dict(color='rgb(58,200,225)',line=dict(color='rgb(8,48,107)',width=1.5),),opacity=0.6)
    data = [trace1,trace2]
    return py.plot(data,include_plotlyjs=False,output_type="div",config={'show_link':False})