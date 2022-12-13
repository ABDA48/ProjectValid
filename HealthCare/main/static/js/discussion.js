
/*
 $('.slots').on('click','#slotsearch',function(event){
      $('#id_slot').val($(this).html())
    })
    $('#slotsearch').click(function (event) {
      date=$('#date').val()
      print(date)
      mydata={
         'date':date
      }
      print(mydata)
      $('.slot-btn').remove()
      $('#id_submit').remove()
      $.ajax({
         method:'POST',
         url:'slots',
         data:mydata,
         
         success:(response)=>{
           print(response['data']['slots'])
           var slotes=response['data']['slots']
           for (var s of slotes){
            var btn='<span  id="slotsearch" class="btn btn-light slot-btn">'+s+'</span>';
             $('.slots').append(btn)
           }
         $('form').append("<button id='id_submit'  type= 'submit' class='btn btn-primary' >Submit</button>")
          
         }
      })

    })
*/
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
$(document).ready(function(){
    function print(params) {
      console.log(params)
    }

    function sendChatMessage(e,username,ROOM) {
      e.preventDefault();
      
      // get values to be submitted
      const timestamp = Date.now();
      // -------->message input
  
      var message=$('#message').val();
      $('#message').val("");
  
      // create db collection and send in the data
      db.ref("message/Room/"+ROOM+"/"+ timestamp).set({
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

    listenMessage(ROOM,username)
   $('#forsend').click((e)=>{
     sendChatMessage(e,username,ROOM)
   })
   
})

 
 