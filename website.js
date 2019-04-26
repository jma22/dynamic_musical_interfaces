$('#record').on('click', function(){
    $.ajax({type: "POST",
            url: "/sandbox/sc/kvfrans/dynamic_musical_interfaces/recording.py",
            data : { recording : 1 },
            success: function(result){
    $("h1").html(result);
  }});})

$('#stop').on('click', function(){
$.ajax({type: "POST",
        url: "/sandbox/sc/kvfrans/dynamic_musical_interfaces/recording.py",
        data : { recording : 0 },
        success: function(result){
$("h1").html(result);
}});})
