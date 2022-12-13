let countries=[
    'abdominal pain','abnormal menstruation','acidity',
    'acute liver failure','altered sensorium','anxiety',
    'back pain','belly pain','blackheads','bladder discomfort',
    'blister','blood in sputum','bloody stool','blurred and distorted vision','breathlessness','brittle nails','bruising','burning micturition','chest pain','chills','cold hands and feets','coma','congestion','constipation','continuous feel of urine','continuous sneezing','cough','cramps','dark urine','dehydration','depression','diarrhoea','dischromic  patches','distention of abdomen','dizziness','drying and tingling lips','enlarged thyroid','excessive hunger','extra marital contacts','family history','fast heart rate','fatigue','fluid overload','foul smell of urine','headache','high fever','hip joint pain','history of alcohol consumption','increased appetite','indigestion','inflammatory nails','internal itching','irregular sugar level','irritability','irritation in anus','itching','joint pain','knee pain','lack of concentration','lethargy','loss of appetite','loss of balance','loss of smell','malaise','mild fever','mood swings','movement stiffness','mucoid sputum','muscle pain','muscle wasting','muscle weakness','nausea','neck pain','nodal skin eruptions','obesity','pain behind the eyes','pain during bowel movements','pain in anal region','painful walking','palpitations','passage of gases','patches in throat','phlegm','polyuria','prominent veins on calf','puffy face and eyes','pus filled pimples','receiving blood transfusion','receiving unsterile injections','red sore around nose','red spots over body','redness of eyes','restlessness','runny nose','rusty sputum','scurring','shivering','silver like dusting','sinus pressure','skin peeling','skin rash','slurred speech','small dents in nails','spinning movements','spotting  urination','stiff neck','stomach bleeding','stomach pain','sunken eyes','sweating','swelled lymph nodes','swelling joints','swelling of stomach','swollen blood vessels','swollen extremeties','swollen legs','throat irritation','toxic look (typhos)','ulcers on tongue','unsteadiness','visual disturbances','vomiting','watering from eyes','weakness in limbs','weakness of one body side','weight gain',
    'weight loss','yellow crust ooze','yellow urine','yellowing of eyes','yellowish skin',
];
 
let symptoms=""
const countriesElement=document.querySelector('#country-list');
const countriesinputElement=document.querySelector('#country-input');
const countriesbtn=document.querySelector('#add-btn');
const symptomdisease=document.querySelector('#symptom-disease'); 
const sendsymptom=document.querySelector('#send-symptom'); 

function fetchCountry(){
      
        loadData(countries,countriesElement)
    
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
fetchCountry();

 

countriesinputElement.addEventListener("input",function(){
    const filtereddata=filterdata(countries,countriesinputElement.value);
    loadData(filtereddata,countriesElement);
});
/*countriesbtn.addEventListener('click',function(){
  
    let child = document.createElement('li');
    child.innerHTML=countriesinputElement.value;
    symptoms+=countriesinputElement.value+","
    
    symptomdisease.appendChild(child);
})
*/
function print(str){
    console.log(str)
} 

function showresutl(disease,percentage){
    var msg= '<p><span class="text-primary qa"  style="font-weight: bold;text-transform: capitalize;">'+disease+'</span> at rate of :<span class="text-success">'+percentage+'%</span></p>';
   return msg;
}
$(document).ready(function(){
    var symptoms=""
    $('#country-list').on('click','li',function(event){
     $('#symptom-disease').append('<li value="sympto">'+event.target.innerHTML+'</li>')
      
    });

   

    $('#symptom-disease').on('click','li',function(){
        $(this).fadeOut(500);
    })
     



    $('#send-symptom').click(function(){
        $('#symptom-disease li').each(function(){
            print($(this).text());
            var n=$(this).text()
            symptoms+=n+","
            
        })
        mydata={
            'symptom':symptoms
        }
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
                               for(var i=0;i<disease.length;i++){
                                   $('.result').append(showresutl(disease[i],persentager[i])) 
                               }
                            }
                        })

   
                    }
                   
                   
                
                
                 
                
                })
            }else{
                $('.result').append('<h3> Your disease is</h3>');
                var disease=res['diseaselist']
                var persentager=res['percentage']
                for(var i=0;i<disease.length;i++){
                    $('.result').append(showresutl(disease[i],persentager[i])) 
                }
            } 
                 
            }

        })
        
    })
 
});



 


