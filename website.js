$('#record').on('click', function(){
    $.ajax({type: "POST",
            url: "/sandbox/sc/jma22/testfinal/recording.py",
            data : { recording : 'true' },
            success: function(result){
    $("h1").html(result);
  }});})

$('#stop').on('click', function(){
$.ajax({type: "POST",
        url: "/sandbox/sc/jma22/testfinal/recording.py",
        data : { recording : 'false' },
        success: function(result){
$("h1").html(result);
}});})