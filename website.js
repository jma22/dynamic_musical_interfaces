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

$('#list li').click(function(){
        $(this).css('background-color','rgb(47, 235, 131)')
        $('#list li').not(this).css('background-color','#FFDFA6')
})
        


function changeUrl(url) {
    document.getElementsByName('iFrameName')[0].src = url;
}
