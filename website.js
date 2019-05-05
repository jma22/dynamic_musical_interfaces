$('#record').on('click', function(){
    $.ajax({type: "GET",
            url: "/sandbox/sc/kvfrans/dynamic_musical_interfaces/music_database.py?recording=1",
            success: function(result){
    $("#status").html(result);
  }});})

$('#stop').on('click', function(){
$.ajax({type: "GET",
        url: "/sandbox/sc/kvfrans/dynamic_musical_interfaces/music_database.py?recording=0",
        success: function(result){
$("#status").html("Status:" + result);
}});})


function changeUrl(url) {
    document.getElementsByName('iFrameName')[0].src = url;
}
