from .models import teacherprofile
from User.models import User
from attendance.models import attendance
from datetime import datetime,timedelta
from calendar import monthrange
from django.db.models import Q
from classes.models import classes
from subject.models import subject
import plotly.offline as py
import plotly.graph_objs as go
from django.utils import timezone
from student.models import studentprofile

# date-->'yyyy-mm-dd'
# period-->'week','month','day'
def draw_time_histogram(date,period,Class,semester):
    dt=datetime.strptime(date,"%Y-%m-%d")
    if period=='day':
       q=Q(date_time__gte = dt) & Q(date_time__lt=dt+timedelta(days=1))
    if period=='week':
        start=dt-timedelta(days = (dt.weekday()+1)%7)
        end=start+timedelta(days=6)
        print(start)
        q=Q(date_time__gte = start) & Q(date_time__lte = end)
    elif period=='month':
        start=datetime(dt.year,dt.month,1)
        end=start+timedelta(days=monthrange(dt.year,dt.month)[1]-1)
        q=Q(date_time__gte = start) & Q(date_time__lte = end)
    if Class != 0:
        q=q  & Q(Class=Class)
    lis=attendance.objects.filter(q)
    x=[]
    for item in lis:
        x.append(item.subject_id)
    x=list(set(x))
    y=[lis.filter(subject=sub).count() for sub in x]
    subjects=[ subject.objects.filter(pk=id).values_list('name',flat=True)[0] for id in x]
    trace1=go.Bar(x=subjects, y=y,name=period+"ily Total",width=0.2,marker=dict(
        color='rgb(200,255,00)',
        line=dict(
            color='rgb(00,255,00)',
            width=4,
        )
    ),
    opacity=1
    )
    data=[trace1]
    if Class !=0:
        clas=str(classes.objects.filter(pk=Class)[0])
    else:
        clas="Total"
    layout=go.Layout(title=period+" wise "+ clas +"  Attendance",
                    xaxis=dict(title="Subjects",),
                    yaxis=dict(title="Total Students Attended",),)
    figure=go.Figure(data=data,layout=layout)
    return py.plot(figure,include_plotlyjs=False,output_type="div",config={'showLink':False})
    
def defaulter(date,period,Class,semester):
    list_stu = studentprofile.objects.filter(Class=Class).values_list('user_id',flat=True)
    print(list_stu)
    dt=datetime.strptime(date,"%Y-%m-%d")
    if period=='day':
       q=Q(date_time__gte = dt) & Q(date_time__lt=dt+timedelta(days=1))
    if period=='week':
        start=dt-timedelta(days = (dt.weekday()+1)%7)
        end=start+timedelta(days=6)
        print(start)
        q=Q(date_time__gte = start) & Q(date_time__lte = end)
    elif period=='month':
        start=datetime(dt.year,dt.month,1)
        end=start+timedelta(days=monthrange(dt.year,dt.month)[1]-1)
        q=Q(date_time__gte = start) & Q(date_time__lte = end)
    if Class != 0:
        q=q  & Q(Class=Class)
    atten = attendance.objects.filter(q).values_list('student',flat=True)
    print(atten)
    defaulter=[]
    for stu in list_stu:
        if stu not in atten:
            defaulter.append(stu)
            
    def_roll=[studentprofile.objects.filter(user_id=id).values_list('roll_no',flat=True)[0] for id in defaulter]
    return def_roll


def totalatt(subject,Class):
    #subID=subject.objects.filter(name_iexact = subject).values_list('id',flat=True)[0]
    #ClassID = classes.objects.filter()
    temp_time_list=[]
    q=Q(subject=subject) & Q(Class=Class)
    lis_atten = attendance.objects.filter(q).values_list('date_time',flat=True)
    for time in lis_atten:
        time=time-timedelta(seconds=time.second,minutes=time.minute)
        if time not in temp_time_list:
            temp_time_list.append(time)
            
    return len(temp_time_list)
    
def searcher(name,stype,Class,is_HOD):
    names=name.split()
    if stype=='1':
        if len(names) == 2:
            q=Q(first_name__iexact=names[0]) & Q(last_name__iexact=names[1]) & Q(is_student=True)
        else:
            q=(Q(first_name__iexact=names[0]) | Q(last_name__iexact=names[0])) & Q(is_student=True)
        lis_stu=User.objects.filter(q).values_list('studentprofile',flat=True)
    else:
        q=Q(roll_no__iexact=names[0])
        lis_stu=studentprofile.objects.filter(q).values_list('user_id',flat=True)
    print(lis_stu)
    cont_list=[]
    subj = subject.objects.all().values_list('id',flat=True)
    for id in lis_stu:
        classe = studentprofile.objects.filter(user_id=id).values_list('Class',flat=True)[0]
        if Class==classe or is_HOD:
            cont=[(attendance.objects.filter(student_id=id,subject=sub,Class=classe).count(),
                                totalatt(sub,classe),
                                subject.objects.filter(id=sub).values_list('name',flat=True)[0],
                                round((attendance.objects.filter(student_id=id,subject=sub,Class=classe).count()/(totalatt(sub,classe)+0.00001))*100),)
                                for sub in subj]
            cont=[cont,studentprofile.objects.get(user_id=id)]
            cont_list.append(cont)
            
    return cont_list
    
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
    return py.plot(data, filename='grouped-bar-direct-labels',include_plotlyjs=False,output_type="div",config={'show_link':False})
    

    