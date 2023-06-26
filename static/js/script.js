$(document).ready(function () {
    var recording = false;
    var recordingTimer;
    var recordings = [];

    $('#start-recording-button').click(function () {
        $.ajax({
        url: '/start_recording',
        type: 'POST',
        data: JSON.stringify({recording: true}),
        contentType: 'application/json;charset=UTF-8'
    });
        // if (!recording) {
        //     recording = true;
        //     recordings = [];
        //     $.ajax({
        //         url: '/start_recording',
        //         method: 'POST'
        //     });
        //     recordingTimer = setInterval(function () {
        //         $.ajax({
        //             url: '/video_stream1',
        //             method: 'GET',
        //             cache: false
        //         }).done(function (data) {
        //             var img = $('<img />', {
        //                 src: URL.createObjectURL(data),
        //                 alt: 'Video 1'
        //             });
        //             $('#video1').empty().append(img);
        //         });
        //         $.ajax({
        //             url: '/video_stream1',
        //             method: 'GET',
        //             cache: false
        //         }).done(function (data) {
        //             var img = $('<img />', {
        //                 src: URL.createObjectURL(data),
        //                 alt: 'Video 2'
        //             });
        //             $('#video2').empty().append(img);
        //         });
        //         $.ajax({
        //             url: '/video_stream1',
        //             method: 'GET',
        //             cache: false
        //         }).done(function (data) {
        //             var img = $('<img />', {
        //                 src: URL.createObjectURL(data),
        //                 alt: 'Video 3'
        //             });
        //             $('#video3').empty().append(img);
        //         });
        //         if (recording) {
        //             $.ajax({
        //                 url: '/video_stream1',
        //                 method: 'GET',
        //                 cache: false,
        //                 responseType: 'arraybuffer'
        //             }).done(function (data) {
        //                 recordings.push(new Uint8Array(data));
        //             });
        //         }
        //     }, 100);
        // }
    })
    ;

    $('#stop-recording-button').click(function () {
        $.ajax({
        url: '/stop_recording',
        type: 'POST',
        data: JSON.stringify({recording: false}),
        contentType: 'application/json;charset=UTF-8'
    });
        // if (recording) {
        //     recording = false;
        //     clearInterval(recordingTimer);
        //     var blob = new Blob(recordings, {type: 'video/avi'});
        //     var url = URL.createObjectURL(blob);
        //     var a = $('<a />', {
        //         href: url,
        //         download: 'record_' + new Date().getTime() + '.avi'
        //     });
        //     a.appendTo('body');
        //     // a[0].click();
        //     a.remove();
        // }
    });
});