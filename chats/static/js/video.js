let myVideoStream;
// let myId;
// var videoGrid = document.getElementById('videoDiv')
// var myvideo = document.createElement('video');
// myvideo.muted = true;
// const peerConnections = {}
navigator.mediaDevices.getUserMedia({
    video: true,
    audio: true
}).then((stream) => {
    myVideoStream = stream;
}).catch(err => {
    alert(err.message)
})
// function close_window() {
//     if (confirm("end call?")) {
//         close();
//     }
// }



// const startWebCam = () =>{
//  if (navigator.mediaDevices.getUserMedia) {
//   navigator.mediaDevices.getUserMedia({ video: true })
//   .then(stream => video.srcObject = stream).catch(error => console.log(error));
//  }
// }
// startWebCam();

// const StopWebCam = ()=>{
//   let stream = video.srcObject;
//   let tracks = stream.getTracks();
//   tracks.forEach(track => track.stop());
//   video.srcObject = null;
// }    

const video = document.getElementById("localVideo");
const muteButton = document.getElementById("muteButton");
const stopVideo = document.getElementById('stopVideo');
// Boolean check = false
let check = 0,checkAudio = 0;

function stop(){
    console.log("Reached here")
    myVideoStream.getVideoTracks()[0].enabled = false;
        let stream = video.srcObject;
        console.log("Got stream: " + stream);
        let tracks = stream.getTracks();
        console.log("Got tracks: "+tracks);
        tracks.forEach(track => track.stop());
        video.srcObject = null;
        html = `<i class="fas fa-video-slash" onclick="startStop();"></i>`;
        stopVideo.classList.toggle("background__red");
        stopVideo.innerHTML = html;
        return 1;
}


function start(){
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => video.srcObject = stream).catch(error => console.log(error));
    }
    myVideoStream.getVideoTracks()[0].enabled = true;
    html = `<i class="fas fa-video" onclick="startStop();"></i>`;
    stopVideo.classList.toggle("background__red");
    stopVideo.innerHTML = html;
    return 0;
}

function startStop(){
    // check == false;
    if(check == 0){
        check = stop();
    }
    else{
        check = start();
    }
}


function mute(){
    myVideoStream.getAudioTracks()[0].enabled = false;
    html = `<i class="fas fa-microphone-slash" onclick="muteUnmute();"></i>`;
    muteButton.classList.toggle("background__red");
    muteButton.innerHTML = html;
    return 1;
}

function unmute(){
    myVideoStream.getAudioTracks()[0].enabled = true;
    html = `<i class="fas fa-microphone" onclick="muteUnmute();"></i>`;
    muteButton.classList.toggle("background__red");
    muteButton.innerHTML = html;
    return 0;
}

function muteUnmute(){
    if(checkAudio == 0){
        checkAudio = mute();
    }
    else{
        checkAudio = unmute();
    }
}



function close_window() {
    if (confirm("Close Window?")) {
      window.close();
    }
  }


function invite(){
    prompt("Copy this link and send it to people you want to meet with",window.location.href);
}

// const inviteButton = document.querySelector("#inviteButton");
// const muteButton = document.querySelector("#muteButton");
// const stopVideo = document.querySelector("#stopVideo");
// muteButton.addEventListener("click", () => {
//     const enabled = myVideoStream.getAudioTracks()[0].enabled;
//     if (enabled) {
//         myVideoStream.getAudioTracks()[0].enabled = false;
//         html = `<i class="fas fa-microphone-slash"></i>`;
//         muteButton.classList.toggle("background__red");
//         muteButton.innerHTML = html;
//     } else {
//         myVideoStream.getAudioTracks()[0].enabled = true;
//         html = `<i class="fas fa-microphone"></i>`;
//         muteButton.classList.toggle("background__red");
//         muteButton.innerHTML = html;
//     }
// });

// stopVideo.addEventListener("click", () => {
//     const enabled = myVideoStream.getVideoTracks()[0].enabled;
//     if (enabled) {
//         myVideoStream.getVideoTracks()[0].enabled = false;
//         html = `<i class="fas fa-video-slash"></i>`;
//         stopVideo.classList.toggle("background__red");
//         stopVideo.innerHTML = html;
//     } else {
//         myVideoStream.getVideoTracks()[0].enabled = true;
//         html = `<i class="fas fa-video"></i>`;
//         stopVideo.classList.toggle("background__red");
//         stopVideo.innerHTML = html;
//     }
// });

// inviteButton.addEventListener("click", (e) => {
//     prompt(
//         "Copy this link and send it to people you want to meet with",
//         window.location.href
//     );
// });

// const server = require('http').Server(app);
// const io = require('socket.io')(server);

// server.listen(4000, () => {
//             console.log("Server running on port 4000");
//         );