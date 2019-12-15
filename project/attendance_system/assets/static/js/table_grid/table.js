var inital_data=[];
var changes_index=[];

//$('.attribute').prop('contenteditable',true);

var get_header=function(){
    
    var headers=[];
    
    $('table th').each(function(index,item){
        headers[index]=$(item).html();
    });
    
    return headers;
}

var chang=function(){
    
   $('.attribute').each(function(index,item){
        if($(item).html()=='P')
        $(item).css('background-color','#94FF94');
        else if($(item).html()=='A')
        $(item).css('background-color','#FF9494');
        else
        $(item).css('background-color','#AAAA00');
            
   });
}

var get_data=function(){
    
    var data=[];
    
    $('table tr').each(function(index,item){
        var row=[];
        $('td',$(item)).each(function(INDEX,ITEM){
            row[INDEX]=$(ITEM).html();
        }) ;
        data[index]=row;
    });

    return data;
}


var write_header=function(headers){
    
    $('table th').each(function(index,item){
        $(item).html(headers[index]);
    });
}


var write_data=function(data){
    
    $('table tr').each(function(index,item){
        var row=data[index];
        $('td',$(item)).each(function(INDEX,ITEM){
            $(ITEM).html(row[INDEX]);
            if(row[INDEX]=='P')
             $(ITEM).css('background-color','#94FF94');
            else if(row[INDEX]=='A')
             $(ITEM).css('background-color','#FF9494');
                
        }) ;
    });

}

$('.attribute').click(function(){
    var T = $(this);
   if(T.html()=='P')
   {
       T.html('A');
       T.css('background-color','#FF9494')
       //$.post('attendance/delete/',{})
   }
   else
   {
       T.html('P');
       T.css('background-color','#94FF94')
   }
});



inital_data=get_data();

$('#ajax_submit').click(function(event){
   event.stopImmediatePropagation();
   var date = $('.date').val();
   var Class = $('#class').find(':selected').val();
   var subject = $('#subject').find(':selected').val();
   console.log(date);
   console.log(Class);
   
   $.post('/attendance/fetch/',{date:date , Class:Class , subject:subject},function(table,status){
       //var data = $.parseJSON(data)
      // write_header(data.headers)
       //write_data(data.data);
       //console.log(data);
      $('#TgridHolder').empty();
      $('#TgridHolder').html(table);
      chang();
   });
   
   
});

$('.attribute').click(function(){
    var Tj= $(this);
    var id=Tj.attr('id');
    var array=id.split("_");
    var text = Tj.html();
    var Class = $('#class').find(':selected').val();
    var subject = $('#subject').find(':selected').val();
    console.log('attendance/update/'+array[0]+'/'+array[1]+'/')
    console.log(text);
    
    $.post('/attendance/update/',{rollno:array[0],date:array[1],status:text,Class:Class,subject:subject},function(data,status){
        console.log(data)
    });
        
});