//Global variablr
var base64data
//Take permission to record audio and then send stream
navigator.mediaDevices.getUserMedia({audio:true})
      .then(stream => {handlerFunction(stream)
                       });

//Function to handle the input stream
          function handlerFunction(stream) {
            //Stores the stream
            window.rec = new MediaRecorder(stream);
            //Task when recording starts
            rec.onstart = e =>{

                totalaudio = [];
           
            }
            
            //Task when audio is inputted into the stream
            rec.ondataavailable = e => {
             
              //Add data to the audio buffer
              totalaudio.push(e.data);
                       
            }
            

            //Task when audio is stopped
            rec.onstop = e =>{
              //Print length of buffer
              console.log(totalaudio.length)
              //Create blob of the new audio
              let blob = new Blob(totalaudio);
              //Send blob to the backend
              sendData(blob)
              //recordedAudio.src = URL.createObjectURL(blob);
              //recordedAudio.controls=true;
              //recordedAudio.autoplay=false;

            }
            //Interval function to interrupt the recording every 5 seconds. 
            setInterval(function(){
              //If the recording has started, interrupt.
              if(rec.state == "recording"){

                rec.stop()
                totalaudio = []
                rec.start()

              }
              //6000 as it is always a second less = 5000ms
            }, 6000);
            
           }
                 
           
           
          //POST data out      
          async function sendData(data) {
            //console.log("Inside sendData")
            //console.log(data instanceof Blob)
             console.log(data)
             //Upload the blob to a file reader
             var reader = new FileReader();
             reader.readAsDataURL(data); 
             //Converting it to a base64 string. 
             reader.onload = function() {
                  base64data = reader.result.split(',')[1];                
                 
             }
              message = "file1"
              //Using fetch to post data to backend. 
              let response = await fetch("/index1", {
                
                method: "POST",
                headers: {
                
                         'Content-Type': 'application/json',
                
                          },
                body: JSON.stringify({message:base64data})
                  //body: JSON.stringify({message:"Hi there!"})
                });
              var result = await response.json();
              
              var pred = document.getElementById("prediction");
              var element = document.getElementById("container1");
              

              // Add an event listener
              pred.addEventListener("Trigger", function(e) {
                //console.log(e.detail); // Prints "Example of an event"
                pred.style.color = e.detail.Textcolor;
                pred.innerHTML = "Cough";
                element.style.display ="block";

              });

              // Create the event
              var event = new CustomEvent("Trigger", { "detail": {
                message : "You Coughed!",
                Textcolor : "red" } });
              
              if (result.label === "coughing"){
                pred.dispatchEvent(event);
              }
              else{
                pred.style.color = "black";
                pred.innerHTML ="Predictions";
                element.style.display = "none";
              }
            }

         // When start button is clicked. 
        record.onclick = e => {

          console.log('Start:I was clicked')
          record.disabled = true;
          record.style.backgroundColor = "blue"
          stopRecord.disabled=false;
          audioChunks = [];
          rec.start();

        }

        //When stop button is clicked.
        stopRecord.onclick = e => {

          console.log("Stop:I was clicked")
          record.disabled = false;
          stop.disabled=true;
          record.style.backgroundColor = "red"
          rec.stop();
        
        }
