/*
const firebaseConfig = {
    apiKey: "AIzaSyCRbK_hk8dqKrFaCUGlnvkYvty37ZYWtFE",
    authDomain: "healthcareproject-5f7a1.firebaseapp.com",
    projectId: "healthcareproject-5f7a1",
    storageBucket: "healthcareproject-5f7a1.appspot.com",
    messagingSenderId: "984010313232",
    appId: "1:984010313232:web:2ac6f9af234075641c8495",
    measurementId: "G-NZZ0R1BMQT"
  };

  firebase.initializeApp(firebaseConfig);
  const db = firebase.database();
  var ROOM= $('#room').val() 
  var username= $('#username').val() 

 */ 
let countries=[
    'abdominal pain','abnormal menstruation','acidity',
    'acute liver failure','altered sensorium','anxiety',
    'back pain','belly pain','blackheads','bladder discomfort',
    'blister','blood in sputum','bloody stool','blurred and distorted vision','breathlessness','brittle nails','bruising','burning micturition','chest pain','chills','cold hands and feets','coma','congestion','constipation','continuous feel of urine','continuous sneezing','cough','cramps','dark urine','dehydration','depression','diarrhoea','dischromic  patches','distention of abdomen','dizziness','drying and tingling lips','enlarged thyroid','excessive hunger','extra marital contacts','family history','fast heart rate','fatigue','fluid overload','foul smell of urine','headache','high fever','hip joint pain','history of alcohol consumption','increased appetite','indigestion','inflammatory nails','internal itching','irregular sugar level','irritability','irritation in anus','itching','joint pain','knee pain','lack of concentration','lethargy','loss of appetite','loss of balance','loss of smell','malaise','mild fever','mood swings','movement stiffness','mucoid sputum','muscle pain','muscle wasting','muscle weakness','nausea','neck pain','nodal skin eruptions','obesity','pain behind the eyes','pain during bowel movements','pain in anal region','painful walking','palpitations','passage of gases','patches in throat','phlegm','polyuria','prominent veins on calf','puffy face and eyes','pus filled pimples','receiving blood transfusion','receiving unsterile injections','red sore around nose','red spots over body','redness of eyes','restlessness','runny nose','rusty sputum','scurring','shivering','silver like dusting','sinus pressure','skin peeling','skin rash','slurred speech','small dents in nails','spinning movements','spotting  urination','stiff neck','stomach bleeding','stomach pain','sunken eyes','sweating','swelled lymph nodes','swelling joints','swelling of stomach','swollen blood vessels','swollen extremeties','swollen legs','throat irritation','toxic look (typhos)','ulcers on tongue','unsteadiness','visual disturbances','vomiting','watering from eyes','weakness in limbs','weakness of one body side','weight gain',
    'weight loss','yellow crust ooze','yellow urine','yellowing of eyes','yellowish skin',
];
 
/*
const countriesElement=document.querySelector('#country-list');
const countriesinputElement=document.querySelector('#country-input');
fetchCountry(countriesElement);
addlistner(countriesElement,countriesinputElement)
*/

function fetchCountry(countriesElement){
      
    loadData(countries,countriesElement)

}
function print(str){
    console.log(str)
} 

function loadData(data,element){
if(data){
    element.innerHTML="";
    let innerElement="";
    data.forEach((item)=>{
        innerElement+='<li>'+item+'</li>';
    });
    element.innerHTML=innerElement;

}
}
function filterdata(data,search){
return  data.filter((x)=> x.toLowerCase().includes(search.toLowerCase()));
}



function addlistner(countriesElement,countriesinputElement){
    countriesinputElement.addEventListener("input",function(){
        const filtereddata=filterdata(countries,countriesinputElement.value);
        loadData(filtereddata,countriesElement);
        });
}


function print(str){
    console.log(str)
} 

function showresutl(disease,percentage){
    var msg= '<p><span class="text-primary qa"  style="font-weight: bold;text-transform: capitalize;">'+disease+'</span> at rate of :<span class="text-success">'+percentage+'%</span></p>';
   return msg;
}
function leftmessage(message) {
    var lmessage='<div class="msg right-msg">'+
    '<div class="msg-img"></div>'+
'<div class="msg-bubble">'+
  '<div class="msg-info">'+
    '<div class="msg-info-name">Sajad</div>'+
    '<div class="msg-info-time">12:46</div>'+
  '</div>'+
  '<div class="msg-text">'+
  message+
  '</div>'+
'</div>'+
'</div>';
return lmessage;
}
function rightmessage(message) {
    var rmessage='<div class="msg left-msg">'+
    '<div class="msg-img"></div>'+
      
    '<div class="msg-bubble">'+
    '<div class="msg-info">'+
    '<div class="msg-info-name">BOT</div>'+
    '<div class="msg-info-time">12:45</div>'+
    '</div>'+
      
    '<div class="msg-text">'+
    message+
             '</div> </div> </div>';
    return rmessage;
}



function yesno(){
  var btnyesno='<div style="margin: 20px;"><button id="yes" class="btn btn-success" value="yes">YES </button>'
 + '<button id="no" class="btn btn-danger" value="yes">NO </button></div>';
 return btnyesno;
}
function btnaccess(){
    var ccess=' <div  style="margin:20px">'
    +'<button id="dprediction" class="btn btn-success" value="disease prediction">Disease Prediction </button>'
    +'<button id="appointment" class="btn btn-info" value="disease prediction">Doctor appointment </button>'
    +'<button id="calldoctor" class="btn btn-danger" value="disease prediction">Call Doctor </button></div>'
return ccess;
}
function asksymptom(){
    var htmlsymptom ='<div><h3>Choose which symptom do you have</h3><div class="row" >'+
      '<div class="col-sm-6 card"  style="margin:10px;"><div class="contain">'+
      '<input type="text" class="autocomplete-input" placeholder="Search symptoms" name="country" id="country-input">'+
      '<ul class="autocomplete-list" id="country-list"></ul> </div></div>'+
      '<div class="col-sm-4"><div class="symptom"> <h3>Symptoms</h3>'+
        '<ul id="symptom-disease"> </ul><input type="button" class="btn btn-primary" value="Predict" id="send-symptom">'+
       '</div></div> </div><div class="question"></div><div class="result"></div></div>';

       return htmlsymptom;
}
/*====================AJAX START=======================*/
$(document).ready(function(){
    var symptoms=""
    $('main').on('click','#country-list li',function(event){
        $('#symptom-disease').append('<li value="sympto">'+event.target.innerHTML+'</li>')
         
       });
   
      
   
       $(' main ').on('click','#symptom-disease li',function(){
           $(this).fadeOut(500);
       })
    
       $('main').on('click','#send-symptom',function(){
        $('#symptom-disease li').each(function(){
            print($(this).text());
            var n=$(this).text()
            symptoms+=n+","
            
        })
        mydata={
            'symptom':symptoms
        }
        sendSymptoms(mydata)

       })

function sendSymptoms(mydata){
    $.ajax({
        url:'sendSymptoms',
        data:mydata,
        method:'POST',
        success:(response)=>{
            
             res=response['data']['res']
             if(res['statut']!='accepted'){
             curentSymptom=res['curentSymptom']
             Question=res['question']
             var Len=Question.length
             var i=0
             var qa='<h3 class="qa">Quetion for accurate result</h3><br>'
             var btnnext='<button class="qa btn btn-primary" type="submit" id="next">next</button>'
            var btnfinish='<button  class="qa" btn btn-info type="submit" id="finish">finish</button>'
           
           
            var questionHtml=""
             var questionHtmls=[]
             
             Question.forEach((item)=>{
                item.forEach((sympt)=>{
                     questionHtml+='<span class="text-dark"style="text-transform:capitalize;margin:10px">'+sympt.replace("_"," ")+'</span>'+'<input width="20px"  class="bg-primary"  type="checkbox" name="question" id="label" value='+sympt+'><br>';

                })
                questionHtmls.push(questionHtml);
                questionHtml=""
             })
             $('.question').append(qa);
             $('.question').append('<div class="qa">'+questionHtmls[0]+'</div>');
             $('.question').append(btnnext);
             var sy=''
            $('.question').on('click','button',function(event){
              
            
                
                var msq =$("input[type='checkbox']:checked");
                for(var m of msq){
                    print(m.value)
                    sy+=m.value+","
                 }
                
                $('.qa').remove()
                i++;
                print(i);
                $('.question').append(qa);
                $('.question').append('<div class="qa">'+questionHtmls[i]+'</div>');
                if(i<Len-1){
                   $('.question').append(btnnext);
                }else{
                   $('.question').append(btnfinish);
                }
                if (event.target.id=='finish'){
                    i=0
                    $('.question').html("")
                    var sympt=curentSymptom+","+sy;
                    print(sympt);
                    dmydata={
                        'symptom':sympt
                    }
                    $.ajax({
                        url:'sendSymptoms',
                        data:dmydata,
                        method:'POST',
                        success:(response)=>{
                           var res=response['data']['res']
                           print(res['diseaselist'])
                           print(res['percentage'])
                           $('.result').append('<h3 class="qa"> Your disease is</h3>');
                           var disease=res['diseaselist']
                           var persentager=res['percentage']
                           
                               $('.result').append(showresutl(disease[0],persentager[0])) 
                               sendMessage(disease[0])
                           
                        }
                    })


                }
               
               
            
            
             
            
            })
        }else{
            $('.result').append('<h3> Your disease is</h3>');
            var disease=res['diseaselist']
            var persentager=res['percentage']
            $('.result').append(showresutl(disease[0],persentager[0])) 
            sendMessage(disease[0])
        } 
             
        }

    })
}

function sendMessage(msg){
    var csrf=$("input[name=csrfmiddlewaretoken]").val(); 
    var mdata={
        csrfmiddlewaretoken:csrf,
        'message':msg,
    }
    var lmessage=leftmessage(msg);
    $('#ma').append(lmessage);
    $("#ma").animate({
        scrollTop: $("#ma").get(0).scrollHeight
    }, 300);
    $('#message').val("");
    $.ajax({
        url:'chatbotsend',
        data:mdata,
        method:'POST',
        success:function (response){
            console.log(response)
            var result=response['data']['res'];
            var pos=response['data']['position']
            if (result=='notknowing'){
              $('#ma').append(asksymptom());
              const countriesElement=document.querySelector('#country-list');
              const countriesinputElement=document.querySelector('#country-input');
             fetchCountry(countriesElement);
            addlistner(countriesElement,countriesinputElement)
            }else{
                var res=rightmessage(result);
                $('#ma').append(res);  
                if(pos==1){
                   $('#ma').append(btnaccess())
                }    
                if (pos==2){
                   $('#ma').append(yesno())
                }
            }
             
       
        }
    })
  }


  function appointment(msg){
    mydata={
        'msg':msg
    }
    var form='<div class="forform" style="width:400px;margin:auto" ><h6>Make an appointment</h6><form method="POST" actions=disease/prediction/appointment>'+
'<p>Disease :<input type="text" name="disease" class="form-control" maxlength="20" required id="id_disease"></p>'+
'<p>Age :<input type="text" name="age" class="form-control" maxlength="20" required id="id_age"></p>'+
'<p>Date :<input type="date" name="date" class="form-control" id="date"></p>'+
'<input type="hidden"  name="slot" maxlength="20" required="" id="id_slot" style="user-select: auto;"/>'+
'</form>'+'<button   id="slotsearch" class="btn btn-primary">Search slots</button><div class="slots">'+ '</div></div>'
$('main').append(form)
        
  }

  function searchSlotes(date){
    
    mydata={
        'date':date
    }
    print(mydata)
    $('.slot-btn').remove()
    $('#id_submit').remove()
    $.ajax({
        url:'slots',
        method:'POST',
        data:mydata,
        success:(response)=>{
            console.log(response['data'])
            if(response['data']['slots']==''){
                print('no slot left')
                $('.slots').append('<span>no slot left</span>')
            }else{
                var slotes=response['data']['slots']
                for (var s of slotes){
                 var btn='<span  id="slotsearch" class="btn btn-light slot-btn">'+s+'</span>';
                  $('.slots').append(btn)
                }
              $('.forform').append("<button id='id_submit'  type= 'submit' class='btn btn-primary' >Submit</button>")
             
            }
             
        }


     })
  }
function submitAppointment(disease,age,date,slot){
    mydata={
      'disease':disease,
      'age':age,
       'date':date,
       'slot':slot 
    }
    print(mydata)
    $.ajax({
        url:'appointment',
        method:'POST',
        data:mydata,
        success:(response)=>{
            rightmessage(response['data']['res'])
        
        }
    })
}

function chat(msg){
    mydata={
        'msg':msg,
    }
    print(mydata)
    $.ajax({
        url:'chat',
        method:'POST',
        data:mydata,
        success:(response)=>{
            data=response['data']
            var val=data['id']+'/'+data['patientid']+'-'+data['patUsername']+'-'+data['docUsername']
            var app='<button id="doctor" class="btn btn-light" value='+val+'>'+response['data']['doctorname']+'</button>';
            $('main').append('<p>'+app+'</p>')  
        }
    })
}

function sendChatMessage(e,username,ROOM) {
    e.preventDefault();
  
    // get values to be submitted
    const timestamp = Date.now();
    // -------->message input

    var message=$('#message').val();
    $('#message').val("");

    // create db collection and send in the data
    db.ref(ROOM+"/"+ timestamp).set({
      username,
      message,
    });
  }
  function listenMessage(r,username){
    const room='message/Room/'
    const fetchChat = db.ref(room+r);
    print('listening-->')
    print(room+r)


    fetchChat.on("child_added", function (snapshot) {
        const messages = snapshot.val();
        /*
        const message = `<li class=${
          username === messages.username ? "sent" : "receive"
        }><span>${messages.username}: </span>${messages.message}</li>`;
        // append the message on the page
        document.getElementById("messages").innerHTML += message;
        */
        if(username===messages.username){
            print(messages)
            var rm=leftmessage(messages.message)
            $('#ma').append(rm);
        $("#ma").animate({
            scrollTop: $("#ma").get(0).scrollHeight
        }, 300);

        }else{
            var lfm=rightmessage(messages.message);
            $('#ma').append(lfm);
            $("#ma").animate({
                scrollTop: $("#ma").get(0).scrollHeight
            }, 300);
    
        }

      });
  }


  
    $('#forsend').click(function (event) {
        var message=$('#message').val();
        sendMessage(message);
       // sendChatMessage(event,username,ROOM)
       
    });
    $('main').on('click','button',function(event){
        var id = $(event.target).attr('id');
        if(id=='dprediction'){
            sendMessage('Disease Prediction');
        }else if(id=='appointment'){
            appointment('appoitment')
        }else if(id=='chatdoctor'){
            chat('chat');
        }else if(id=='yes'){
            sendMessage('yes');
        }else if(id=='no'){

        }else if(id=='slotsearch'){
            searchSlotes($('#date').val())
        }else if(id=='id_submit'){
            disease=$('#id_disease').val()
            age=$('#id_age').val()
            date=$('#date').val()
            slot=$('#id_slot').val()
            submitAppointment(disease,age,date,slot)
        }else if(id=='doctor'){
        var d='message/Room/'+$(this).val()
        var da=d.split('-')
        var room=da[0]
        var patientUsername=da[1]
        var doctorUsername=da[2]
        ROOM=room;
        username=patientUsername;
        print(ROOM)
        print(username)
       
        }
     })
     $('main').on('click','#slotsearch',function(event){
        $('#slotsearch').addClass('btn-primary')
        $('#id_slot').val($(this).html())
      })


 

    
})







  